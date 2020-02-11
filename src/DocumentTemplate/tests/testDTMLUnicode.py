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
"""Document Template Tests
"""
import unittest


class force_str:
    # A class whose string representation is not always a plain string:

    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s


class DTMLUnicodeTests(unittest.TestCase):
    recode_to = "latin-1"
    encoding_arg = None

    def _get_doc_class(self):
        from DocumentTemplate.DT_HTML import HTML

        def make(*args):
            doc = HTML(*args, encoding=self.encoding_arg)
            # Need to cheat here because the mewning of passing
            # None as encoding has changed, it will be UTF-8 then
            if self.encoding_arg != doc.encoding:
                doc.encoding = self.encoding_arg
            return doc

        return make
    doc_class = property(_get_doc_class,)

    def _recode(self, string):
        if isinstance(string, bytes):
            string = string.decode('UTF-8')
        return string.encode(self.recode_to)

    def testAA(self):
        html = self.doc_class('<dtml-var a><dtml-var b>')
        expected = 'helloworld'
        res = html(a='hello', b='world')
        self.assertEqual(res, expected)

    def testUU(self):
        html = self.doc_class('<dtml-var a><dtml-var b>')
        expected = 'helloworld'
        res = html(a='hello', b='world')
        self.assertEqual(res, expected)

    def testAU(self):
        html = self.doc_class('<dtml-var a><dtml-var b>')
        expected = 'helloworld'
        res = html(a='hello', b='world')
        self.assertEqual(res, expected)

    def testAB(self):
        html = self.doc_class('<dtml-var a><dtml-var b>')
        expected = 'hello\xc8'
        res = html(a='hello', b=self._recode(b'\xc3\x88'))
        self.assertEqual(res, expected)

    def testUB(self):
        html = self.doc_class('<dtml-var a><dtml-var b>')
        expected = 'hello\xc8'
        res = html(a='hello', b=self._recode(b'\xc3\x88'))
        self.assertEqual(res, expected)

    def testUB2(self):
        html = self.doc_class('<dtml-var a><dtml-var b>')
        expected = '\u07d0\xc8'
        res = html(a=chr(2000), b=self._recode(b'\xc3\x88'))
        self.assertEqual(res, expected)

    def testUnicodeStr(self):
        html = self.doc_class('<dtml-var a><dtml-var b>')
        expected = '\u07d0\xc8'
        res = html(a=force_str(chr(2000)), b=self._recode(b'\xc3\x88'))
        self.assertEqual(res, expected)

    def testUqB(self):
        html = self.doc_class('<dtml-var a html_quote><dtml-var b>')
        expected = 'he&gt;llo\xc8'
        res = html(a='he>llo', b=self._recode(b'\xc3\x88'))
        self.assertEqual(res, expected)

    def testSize(self):
        html = self.doc_class('<dtml-var "_.chr(200)*4" size=2>')
        expected = chr(200) * 2 + '...'
        res = html()
        self.assertEqual(res, expected)


class DTMLUnicodeTestsUTF8(DTMLUnicodeTests):
    recode_to = "utf-8"
    encoding_arg = "utf-8"


class DTMLUnicodeTestsModuleGlobal(DTMLUnicodeTests):
    encoding = "utf-8"
    recode_to = "utf-8"

    def setUp(self):
        import DocumentTemplate as dt
        self._default_encoding = dt.OLD_DEFAULT_ENCODING
        dt.OLD_DEFAULT_ENCODING = self.encoding

    def tearDown(self):
        import DocumentTemplate as dt
        dt.OLD_DEFAULT_ENCODING = self._default_encoding
