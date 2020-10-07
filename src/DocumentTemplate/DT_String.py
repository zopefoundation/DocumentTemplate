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

import os
import re
from threading import Lock

from AccessControl.class_init import InitializeClass
from AccessControl.SecurityInfo import ClassSecurityInfo

import DocumentTemplate as _dt

from ._DocumentTemplate import InstanceDict
from ._DocumentTemplate import TemplateDict
from ._DocumentTemplate import render_blocks
from .DT_Return import DTReturn
from .DT_Return import ReturnTag
from .DT_Util import ParseError
from .DT_Var import Call
from .DT_Var import Comment
from .DT_Var import Var


_marker = []  # Create a new marker object.
COOKLOCK = Lock()


class String:
    """Document templates defined from strings.

    Document template strings use an extended form of python string
    formatting.  To insert a named value, simply include text of the
    form: '%(name)x', where 'name' is the name of the value and 'x' is
    a format specification, such as '12.2d'.

    To intrduce a block such as an 'if' or an 'in' or a block continuation,
    such as an 'else', use '[' as the format specification.  To
    terminate a block, ise ']' as the format specification, as in::

      %(in results)[
        %(name)s
      %(in results)]

    """

    isDocTemp = 1

    security = ClassSecurityInfo()

    # Document Templates masquerade as functions:
    class func_code:
        pass

    security.declarePrivate('__code__')  # NOQA: D001
    __code__ = func_code = func_code()
    __code__.co_varnames = 'self', 'REQUEST'
    __code__.co_argcount = 2

    security.declarePrivate('__defaults__')  # NOQA: D001
    security.declarePrivate('func_defaults')  # NOQA: D001
    __defaults__ = func_defaults = ()

    @security.private
    def errQuote(self, s):
        return s

    @security.private
    def parse_error(self, mess, tag, text, start):
        raise ParseError(
            "{}, for tag {}, on line {} of {}".format(
                mess, self.errQuote(tag), len(text[:start].split('\n')),
                self.errQuote(self.__name__)))

    security.declarePrivate('commands')  # NOQA: D001
    commands = {
        'var': Var,
        'call': Call,
        'in': ('in', 'DT_In', 'In'),
        'with': ('with', 'DT_With', 'With'),
        'if': ('if', 'DT_If', 'If'),
        'unless': ('unless', 'DT_If', 'Unless'),
        'else': ('else', 'DT_If', 'Else'),
        'comment': Comment,
        'raise': ('raise', 'DT_Raise', 'Raise'),
        'try': ('try', 'DT_Try', 'Try'),
        'let': ('let', 'DT_Let', 'Let'),
        'return': ReturnTag,
    }

    @security.private
    def SubTemplate(self, name):
        return String('', __name__=name)

    @security.private
    def tagre(self):
        return re.compile(
            '%\\('                                  # beginning
            '(?P<name>[a-zA-Z0-9_/.-]+)'              # tag name
            '('
            '[\000- ]+'                             # space after tag name
            '(?P<args>([^\\)"]+("[^"]*")?)*)'         # arguments
            ')?'
            '\\)(?P<fmt>[0-9]*[.]?[0-9]*[a-z]|[]![])',  # end
            re.I)

    @security.private
    def _parseTag(self, match_ob, command=None, sargs='', tt=type(())):
        tag, args, command, coname = self.parseTag(match_ob, command, sargs)
        if type(command) is tt:
            cname, module, name = command
            d = {}
            try:
                exec('from {} import {}'.format(module, name), d)
            except ImportError:
                exec('from DocumentTemplate.{} import {}'.format(
                    module, name), d)
            command = d[name]
            self.commands[cname] = command
        return tag, args, command, coname

    @security.private
    def parseTag(self, match_ob, command=None, sargs=''):
        """Parse a tag using an already matched re

        Return: tag, args, command, coname

        where: tag is the tag,
               args is the tag's argument string,
               command is a corresponding command info structure if the
                  tag is a start tag, or None otherwise, and
               coname is the name of a continue tag (e.g. else)
                 or None otherwise
        """
        tag, name, args, fmt = match_ob.group(0, 'name', 'args', 'fmt')
        args = args and args.strip() or ''

        if fmt == ']':
            if not command or name != command.name:
                raise ParseError('unexpected end tag', tag)
            return tag, args, None, None
        elif fmt == '[' or fmt == '!':
            if command and name in command.blockContinuations:
                if name == 'else' and args:
                    # Waaaaaah! Have to special case else because of
                    # old else start tag usage. Waaaaaaah!
                    l_ = len(args)
                    if not (args == sargs or  # NOQA: W504
                            args == sargs[:l_] and  # NOQA: W504
                            sargs[l_:l_ + 1] in ' \t\n'):
                        return tag, args, self.commands[name], None

                return tag, args, None, name

            try:
                return tag, args, self.commands[name], None
            except KeyError:
                raise ParseError('Unexpected tag', tag)
        else:
            # Var command
            args = args and ("{} {}".format(name, args)) or name
            return tag, args, Var, None

    @security.private
    def varExtra(self, match_ob):
        return match_ob.group('fmt')

    @security.private
    def parse(self, text, start=0, result=None, tagre=None):
        if result is None:
            result = []
        if tagre is None:
            tagre = self.tagre()
        mo = tagre.search(text, start)
        while mo:
            l_ = mo.start(0)

            try:
                tag, args, command, coname = self._parseTag(mo)
            except ParseError as m:
                self.parse_error(m.args[0], m.args[1], text, l_)

            s = text[start:l_]
            if s:
                result.append(s)
            start = l_ + len(tag)

            if hasattr(command, 'blockContinuations'):
                start = self.parse_block(text, start, result, tagre,
                                         tag, l_, args, command)
            else:
                try:
                    if command is Var:
                        r = command(args, self.varExtra(mo))
                    else:
                        r = command(args)
                    if hasattr(r, 'simple_form'):
                        r = r.simple_form
                    result.append(r)
                except ParseError as m:
                    self.parse_error(m.args[0], tag, text, l_)

            mo = tagre.search(text, start)

        text = text[start:]
        if text:
            result.append(text)
        return result

    @security.private
    def skip_eol(self, text, start, eol=re.compile('[ \t]*\n')):
        # if block open is followed by newline, then skip past newline
        mo = eol.match(text, start)
        if mo is not None:
            start = start + mo.end(0) - mo.start(0)

        return start

    @security.private
    def parse_block(self, text, start, result, tagre,
                    stag, sloc, sargs, scommand):

        start = self.skip_eol(text, start)

        # If this is an older object without encoding set we use the old
        # pre-Zope 4 default.
        encoding = getattr(self, 'encoding', _dt.OLD_DEFAULT_ENCODING)
        blocks = []
        tname = scommand.name
        sname = stag
        sstart = start
        sa = sargs
        while 1:

            mo = tagre.search(text, start)
            if mo is None:
                self.parse_error('No closing tag', stag, text, sloc)
            l_ = mo.start(0)

            try:
                tag, args, command, coname = self._parseTag(mo, scommand, sa)
            except ParseError as m:
                self.parse_error(m.args[0], m.args[1], text, l_)

            if command:
                start = l_ + len(tag)
                if hasattr(command, 'blockContinuations'):
                    # New open tag.  Need to find closing tag.
                    start = self.parse_close(text, start, tagre, tag, l_,
                                             command, args)
            else:
                # Either a continuation tag or an end tag
                section = self.SubTemplate(sname)
                section._v_blocks = section.blocks = self.parse(
                    text[:l_], sstart)
                section._v_cooked = None
                blocks.append((tname, sargs, section))

                start = self.skip_eol(text, l_ + len(tag))

                if coname:
                    tname = coname
                    sname = tag
                    sargs = args
                    sstart = start
                else:
                    try:
                        r = scommand(blocks, encoding=encoding)
                        if hasattr(r, 'simple_form'):
                            r = r.simple_form
                        result.append(r)
                    except ParseError as m:
                        self.parse_error(m.args[0], stag, text, l_)

                    return start

    @security.private
    def parse_close(self, text, start, tagre, stag, sloc, scommand, sa):
        while 1:
            mo = tagre.search(text, start)
            if mo is None:
                self.parse_error('No closing tag', stag, text, sloc)
            l_ = mo.start(0)

            try:
                tag, args, command, coname = self._parseTag(mo, scommand, sa)
            except ParseError as m:
                self.parse_error(m.args[0], m.args[1], text, l_)

            start = l_ + len(tag)
            if command:
                if hasattr(command, 'blockContinuations'):
                    # New open tag.  Need to find closing tag.
                    start = self.parse_close(text, start, tagre, tag, l_,
                                             command, args)
            elif not coname:
                return start

    security.declarePrivate('shared_globals')  # NOQA: D001
    shared_globals = {}

    def __init__(self, source_string='', mapping=None, __name__='<string>',
                 encoding=None, **vars):
        """Create a document template from a string.

        The optional parameter, 'mapping', may be used to provide a
        mapping object containing defaults for values to be inserted.
        """
        self.raw = source_string
        # For newly created objects, if no encoding is passed in we use the
        # ZPublisher default
        self.encoding = encoding or _dt.NEW_DEFAULT_ENCODING
        self.initvars(mapping, vars)
        self.setName(__name__)

    def name(self):
        return self.__name__

    id = name

    @security.private
    def setName(self, v):
        self.__dict__['__name__'] = v

    @security.private
    def default(self, name=None, **kw):
        """Change or query default values in a document template.

        If a name is specified, the value of the named default value
        before the operation is returned.

        Keyword arguments are used to provide default values.
        """
        if name:
            name = self.globals[name]
        for key in kw.keys():
            self.globals[key] = kw[key]
        return name

    @security.private
    def var(self, name=None, **kw):
        """Change or query a variable in a document template.

        If a name is specified, the value of the named variable before
        the operation is returned.

        Keyword arguments are used to provide variable values.
        """
        if name:
            name = self._vars[name]
        for key in kw.keys():
            self._vars[key] = kw[key]
        return name

    @security.private
    def munge(self, source_string=None, mapping=None, **vars):
        """Change the text or default values for a document template."""
        if mapping is not None or vars:
            self.initvars(mapping, vars)
        if source_string is not None:
            self.raw = source_string
        self.cook()

    @security.private
    def manage_edit(self, data, REQUEST=None):
        self.munge(data)

    @security.private
    def read_raw(self, raw=None):
        return self.raw

    @security.private
    def read(self, raw=None):
        return self.read_raw()

    @security.private
    def cook(self):
        with COOKLOCK:
            self._v_blocks = self.parse(self.read())
            self._v_cooked = None

    @security.private
    def initvars(self, globals, vars):
        if globals:
            for k in globals.keys():
                if k[:1] != '_' and k not in vars:
                    vars[k] = globals[k]
        self.globals = vars
        self._vars = {}

    @security.private
    def ZDocumentTemplate_beforeRender(self, md, default):
        return default

    @security.private
    def ZDocumentTemplate_afterRender(self, md, result):
        pass

    def __call__(self, client=None, mapping={}, **kw):
        """Generate a document from a document template.

        The document will be generated by inserting values into the
        format string specified when the document template was
        created.  Values are inserted using standard python named
        string formats.

        The optional argument 'client' is used to specify a object
        containing values to be looked up.  Values will be looked up
        using getattr, so inheritence of values is supported.  Note
        that names beginning with '_' will not be looked up from the
        client.

        The optional argument, 'mapping' is used to specify a mapping
        object containing values to be inserted.

        Values to be inserted may also be specified using keyword
        arguments.

        Values will be inserted from one of several sources.  The
        sources, in the order in which they are consulted, are:

          o  Keyword arguments,

          o  The 'client' argument,

          o  The 'mapping' argument,

          o  The keyword arguments provided when the object was
             created, and

          o  The 'mapping' argument provided when the template was
             created.

        """
        encoding = getattr(self, 'encoding', None)

        if mapping is None:
            mapping = {}
        if hasattr(mapping, 'taintWrapper'):
            mapping = mapping.taintWrapper()

        if not hasattr(self, '_v_cooked'):
            try:
                changed = self.__changed__()
            except Exception:
                changed = 1
            self.cook()
            if not changed:
                self.__changed__(0)

        pushed = None
        try:
            # Support Python 1.5.2, but work better in 2.1
            if mapping.__class__ is TemplateDict or \
               isinstance(mapping, TemplateDict):
                pushed = 0
        except Exception:
            pass

        globals = self.globals
        if pushed is not None:
            # We were passed a TemplateDict, so we must be a sub-template
            md = mapping
            push = md._push
            if globals:
                push(self.globals)
                pushed = pushed + 1
        else:
            md = TemplateDict()
            push = md._push
            shared_globals = self.shared_globals
            if shared_globals:
                push(shared_globals)
            if globals:
                push(globals)
            if mapping:
                push(mapping)
            md.guarded_getattr = self.guarded_getattr
            md.guarded_getitem = self.guarded_getitem
            if client is not None:
                if isinstance(client, tuple):
                    md.this = client[-1]
                else:
                    md.this = client
            pushed = 0

        level = md.level
        if level > 200:
            raise SystemError('infinite recursion in document template')
        md.level = level + 1

        if client is not None:
            if isinstance(client, tuple):
                # if client is a tuple, it represents a "path" of clients
                # which should be pushed onto the md in order.
                for ob in client:
                    push(InstanceDict(ob, md))  # Circ. Ref. 8-|
                    pushed = pushed + 1
            else:
                # otherwise its just a normal client object.
                push(InstanceDict(client, md))  # Circ. Ref. 8-|
                pushed = pushed + 1

        if self._vars:
            push(self._vars)
            pushed = pushed + 1

        if kw:
            push(kw)
            pushed = pushed + 1

        try:
            value = self.ZDocumentTemplate_beforeRender(md, _marker)
            if value is _marker:
                try:
                    result = render_blocks(self._v_blocks, md,
                                           encoding=encoding)
                except DTReturn as v:
                    result = v.v
                self.ZDocumentTemplate_afterRender(md, result)
                return result
            else:
                return value
        finally:
            if pushed:
                md._pop(pushed)  # Get rid of circular reference!
            md.level = level  # Restore previous level

    guarded_getattr = None
    guarded_getitem = None

    def __str__(self):
        return self.read()

    def __getstate__(self, _special=('_v_', '_p_')):
        # Waaa, we need _v_ behavior but we may not subclass Persistent
        d = {}
        for k, v in self.__dict__.items():
            if k[:3] in _special:
                continue
            d[k] = v
        return d


InitializeClass(String)


class FileMixin:
    # Mix-in class to abstract certain file-related attributes
    edited_source = ''

    security = ClassSecurityInfo()

    def __init__(self, file_name='', mapping=None, __name__='', **vars):
        """Create a document template based on a named file.

        The optional parameter, 'mapping', may be used to provide a
        mapping object containing defaults for values to be inserted.
        """
        self.raw = file_name
        self.initvars(mapping, vars)
        self.setName(__name__ or file_name)

    @security.private
    def read_raw(self):
        if self.edited_source:
            return self.edited_source
        if not os.path.exists(self.raw):
            print('file not found: %s' % self.raw)

        if self.raw:
            with open(self.raw, 'r') as fd:
                raw = fd.read()
            return raw
        return ''


InitializeClass(FileMixin)


class File(FileMixin, String):
    """Document templates read from files.

    If the object is pickled, the file name, rather
    than the file contents is pickled.  When the object is
    unpickled, then the file will be re-read to obtain the string.
    Note that the file will not be read until the document
    template is used the first time.
    """
    security = ClassSecurityInfo()

    @security.private
    def manage_edit(self, data):
        raise TypeError('cannot edit files')


InitializeClass(File)
