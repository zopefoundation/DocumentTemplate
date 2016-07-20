##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
'''Document templates with fill-in fields

Document templates provide for creation of textual documents, such as
HTML pages, from template source by inserting data from python objects
and name-spaces.

When a document template is created, a collection of default values to
be inserted may be specified with a mapping object and with keyword
arguments.

A document templated may be called to create a document with values
inserted.  When called, an instance, a mapping object, and keyword
arguments may be specified to provide values to be inserted.  If an
instance is provided, the document template will try to look up values
in the instance using getattr, so inheritence of values is supported.
If an inserted value is a function, method, or class, then an attempt
will be made to call the object to obtain values.  This allows
instance methods to be included in documents.

Document templates masquerade as functions, so the python object
publisher (Bobo) will call templates that are stored as instances of
published objects. Bobo will pass the object the template was found in
and the HTTP request object.

Two source formats are supported:

   Extended Python format strings (EPFS) --
      This format is based on the insertion by name format strings
      of python with additional format characters, '[' and ']' to
      indicate block boundaries.  In addition, parameters may be
      used within formats to control how insertion is done.

      For example:

         %%(date fmt=DayOfWeek upper)s

      causes the contents of variable 'date' to be inserted using
      custom format 'DayOfWeek' and with all lower case letters
      converted to upper case.

   HTML --
      This format uses HTML server-side-include syntax with
      commands for inserting text. Parameters may be included to
      customize the operation of a command.

      For example:

         <!--#var total fmt=12.2f-->

      is used to insert the variable 'total' with the C format
      '12.2f'.

Document templates support conditional and sequence insertion

    Document templates extend python string substitition rules with a
    mechanism that allows conditional insertion of template text and that
    allows sequences to be inserted with element-wise insertion of
    template text.

Access Control

    Document templates provide a basic level of access control by
    preventing access to names beginning with an underscore.
    Additional control may be provided by providing document templates
    with a 'guarded_getattr' and 'guarded_getitem' method.  This would
    typically be done by subclassing one or more of the DocumentTemplate
    classes.

    If provided, the the 'guarded_getattr' method will be called when
    objects are accessed as instance attributes or when they are
    accessed through keyed access in an expression.

Document Templates may be created 4 ways:

    DocumentTemplate.String -- Creates a document templated from a
        string using an extended form of python string formatting.

    DocumentTemplate.File -- Creates a document templated bound to a
        named file using an extended form of python string formatting.
        If the object is pickled, the file name, rather than the file
        contents is pickled.  When the object is unpickled, then the
        file will be re-read to obtain the string.  Note that the file
        will not be read until the document template is used the first
        time.

    DocumentTemplate.HTML -- Creates a document templated from a
        string using HTML server-side-include rather than
        python-format-string syntax.

    DocumentTemplate.HTMLFile -- Creates an HTML document template
        from a named file.

'''

import sys
import types

from ExtensionClass import ExtensionClass

from DocumentTemplate.html_quote import html_quote
from DocumentTemplate.ustr import ustr

if sys.version_info > (3, 0):
    basestring = str
    unicode = str

_marker = object()


def join_unicode(rendered):
    """join a list of plain strings into a single plain string,
    a list of unicode strings into a single unicode strings,
    or a list containing a mix into a single unicode string with
    the plain strings converted from latin-1
    """
    try:
        return ''.join(rendered)
    except UnicodeError:
        # A mix of unicode string and non-ascii plain strings.
        # Fix up the list, treating normal strings as latin-1
        rendered = list(rendered)
        for i in range(len(rendered)):
            if isinstance(rendered[i], str):
                rendered[i] = unicode(rendered[i], 'latin-1')
        return u''.join(rendered)


def render_blocks(blocks, md):
    rendered = []

    render_blocks_(blocks, rendered, md)

    l = len(rendered)
    if l == 0:
        return ''
    elif l == 1:
        return rendered[0]
    return join_unicode(rendered)


def render_blocks_(blocks, rendered, md):
    for block in blocks:
        append = True

        if (isinstance(block, tuple) and
                len(block) > 1 and
                isinstance(block[0], basestring)):

            first_char = block[0][0]
            if first_char == 'v':  # var
                t = block[1]
                if isinstance(t, str):
                    t = md[t]
                else:
                    t = t(md)

                skip_html_quote = 0
                if not isinstance(t, basestring):
                    # This might be a TaintedString object
                    untaintmethod = getattr(t, '__untaint__', None)
                    if untaintmethod is not None:
                        # Quote it
                        t = untaintmethod()
                        skip_html_quote = 1

                if not isinstance(t, basestring):
                    t = ustr(t)

                if (skip_html_quote == 0 and len(block) == 3):
                    # html_quote
                    if isinstance(t, str):
                        if t in ('&', '<', '>', '"'):
                            # string includes html problem characters,
                            # so we cant skip the quoting process
                            skip_html_quote = 0
                        else:
                            skip_html_quote = 1
                    else:
                        # never skip the quoting for unicode strings
                        skip_html_quote = 0

                    if not skip_html_quote:
                        t = html_quote(t)

                block = t

            elif first_char == 'i':  # if
                bs = len(block) - 1  # subtract code
                cache = {}
                md._push(cache)
                try:
                    append = False
                    m = bs - 1
                    icond = 0
                    while icond < m:
                        cond = block[icond + 1]
                        if isinstance(cond, str):
                            # We have to be careful to handle key errors here
                            n = cond
                            try:
                                cond = md[cond]
                            except KeyError as t:
                                if n != t.args[0]:
                                    raise
                                cond = None
                            else:
                                cache[n] = cond
                        else:
                            cond = cond(md)

                        if cond:
                            block = block[icond + 2]
                            if block:
                                render_blocks_(block, rendered, md)
                            m = -1
                            break

                        if icond == m:
                            block = block[icond + 1]
                            if block:
                                render_blocks_(block, rendered, md)

                        icond += 2
                finally:
                    md._pop()

            else:
                raise ValueError(
                    'Invalid DTML command code, %s', block[0])

        elif not isinstance(block, basestring):
            block = block(md)

        if append and block:
            rendered.append(block)


def safe_callable(ob):
    """callable() with a workaround for a problem with ExtensionClasses
    and __call__().
    """
    if hasattr(ob, '__class__'):
        if hasattr(ob, '__call__'):
            return True
        else:
            if type(ob) in (types.ClassType, ExtensionClass):
                return True
            else:
                return False
    return callable(ob)


class InstanceDict(object):
    """"""

    def __init__(self, inst, namespace, guarded_getattr=None):
        self.inst = inst
        self.namespace = namespace
        self.cache = {}
        if guarded_getattr is None:
            self.guarded_getattr = namespace.guarded_getattr
        else:
            self.guarded_getattr = guarded_getattr

    def __repr__(self):
        return 'InstanceDict(%r)' % self.inst

    def __len__(self):
        return 1

    def __setitem__(self, key, value):
        raise TypeError('InstanceDict objects do not support item assignment')

    def __getitem__(self, key):
        value = self.cache.get(key, _marker)
        if value is not _marker:
            return value

        if key[0] == '_':
            if key != '__str__':
                raise KeyError(key)  # Don't divuldge private data
            else:
                return str(self.inst)

        get = self.guarded_getattr
        if get is None:
            get = getattr

        try:
            r = get(self.inst, key)
        except AttributeError:
            raise KeyError(key)

        self.cache[key] = r
        return r


from DocumentTemplate.cDocumentTemplate import (  # NOQA
    TemplateDict,
)
