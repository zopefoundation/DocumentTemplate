##############################################################################
#
# Copyright (c) 2008 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Tests for functions and classes in DT_Var.
"""

import unittest

import six


class TestNewlineToBr(unittest.TestCase):

    def test_newline_to_br(self):
        """
        newline_to_br should work identically with either DOS-style or
        Unix-style newlines.
        """
        from DocumentTemplate import DT_Var
        text = '''\

line one
line two

line three
'''
        self.assertEqual(
            DT_Var.newline_to_br(text),
            '''\
<br />
line one<br />
line two<br />
<br />
line three<br />
''')

        dos = text.replace('\n', '\r\n')
        self.assertEqual(DT_Var.newline_to_br(text), DT_Var.newline_to_br(dos))

    def test_newline_to_br_tainted(self):
        from DocumentTemplate import DT_Var
        text = '''\

<li>line one</li>
<li>line two</li>
'''

        from AccessControl.tainted import TaintedString
        tainted = TaintedString(text)
        self.assertEqual(
            DT_Var.newline_to_br(tainted),
            '''\
<br />
&lt;li&gt;line one&lt;/li&gt;<br />
&lt;li&gt;line two&lt;/li&gt;<br />
''')


class TestUrlQuoting(unittest.TestCase):

    def test_url_quoting(self):
        from DocumentTemplate.DT_Var import url_quote
        from DocumentTemplate.DT_Var import url_unquote
        unicode_value = u'G\xfcnther M\xfcller'
        quoted_unicode_value = u'G%C3%BCnther%20M%C3%BCller'
        utf8_value = unicode_value.encode('UTF-8')
        quoted_utf8_value = b'G%C3%BCnther%20M%C3%BCller'

        self.assertEqual(url_quote(unicode_value), quoted_unicode_value)
        self.assertEqual(url_quote(utf8_value), quoted_utf8_value)

        self.assertEqual(url_unquote(quoted_unicode_value), unicode_value)
        self.assertEqual(url_unquote(quoted_utf8_value), utf8_value)

    def test_url_quoting_plus(self):
        from DocumentTemplate.DT_Var import url_quote_plus
        from DocumentTemplate.DT_Var import url_unquote_plus
        unicode_value = u'G\xfcnther M\xfcller'
        quoted_unicode_value = u'G%C3%BCnther+M%C3%BCller'
        utf8_value = unicode_value.encode('UTF-8')
        quoted_utf8_value = b'G%C3%BCnther+M%C3%BCller'

        self.assertEqual(url_quote_plus(unicode_value), quoted_unicode_value)
        self.assertEqual(url_quote_plus(utf8_value), quoted_utf8_value)

        self.assertEqual(
            url_unquote_plus(quoted_unicode_value), unicode_value)
        self.assertEqual(
            url_unquote_plus(quoted_utf8_value), utf8_value)

    def test_sql_quote(self):
        from DocumentTemplate.DT_Var import sql_quote
        self.assertEqual(sql_quote(u""), u"")
        self.assertEqual(sql_quote(u"a"), u"a")
        self.assertEqual(sql_quote(b"a"), u"a")

        self.assertEqual(sql_quote(u"Can't"), u"Can''t")
        self.assertEqual(sql_quote(u"Can\'t"), u"Can''t")
        # SyntaxError on Python 3.
        # self.assertEqual(sql_quote(ur"Can\'t"), u"Can\\\\''t")

        self.assertEqual(sql_quote(u"Can\\ I?"), u"Can\\ I?")
        # SyntaxError on Python 3.
        # self.assertEqual(sql_quote(ur"Can\ I?"), u"Can\\\\ I?")

        self.assertEqual(
            sql_quote(u'Just say "Hello"'), u'Just say "Hello"')

        self.assertEqual(
            sql_quote(u'Hello\x00World'), u'HelloWorld')
        self.assertEqual(
            sql_quote(u'\x00Hello\x00\x00World\x00'), u'HelloWorld')

        self.assertEqual(
            sql_quote(u'\x00Hello\x00\x00World\x00'), u'HelloWorld')

        self.assertEqual(u"\xea".encode("utf-8"), b"\xc3\xaa")
        if six.PY3:
            self.assertEqual(sql_quote(b"\xc3\xaa'"), u"\xea''")
            self.assertEqual(sql_quote(u"\xea'"), u"\xea''")
        else:
            self.assertEqual(sql_quote(b"\xc3\xaa'"), b"\xc3\xaa''")
            self.assertEqual(sql_quote(u"\xea'"), b"\xc3\xaa''")

        self.assertEqual(
            sql_quote(b"carriage\rreturn"), u"carriagereturn")
        self.assertEqual(
            sql_quote(u"carriage\rreturn"), u"carriagereturn")
        self.assertEqual(sql_quote(u"line\nbreak"), u"line\nbreak")
        self.assertEqual(sql_quote(u"tab\t"), u"tab\t")
