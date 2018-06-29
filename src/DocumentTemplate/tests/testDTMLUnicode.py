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

import six

if six.PY3:
    unichr = chr


class force_str(object):
    # A class whose string representation is not always a plain string:

    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s


class DTMLUnicodeTests(unittest.TestCase):
    def setUp(self):
        import DocumentTemplate as dt
        self._encoding = dt.DEFAULT_ENCODING
        dt.DEFAULT_ENCODING = "utf-8"

    def tearDown(self):
        import DocumentTemplate as dt
        dt.DEFAULT_ENCODING = self._encoding

    def _get_doc_class(self):
        from DocumentTemplate.DT_HTML import HTML
        return HTML
    doc_class = property(_get_doc_class,)

    def testAA(self):
        html = self.doc_class('<dtml-var a><dtml-var b>')
        expected = 'helloworld'
        res = html(a='hello', b='world')
        self.assertEqual(res, expected)

    def testUU(self):
        html = self.doc_class('<dtml-var a><dtml-var b>')
        expected = u'helloworld'
        res = html(a=u'hello', b=u'world')
        self.assertEqual(res, expected)

    def testAU(self):
        html = self.doc_class('<dtml-var a><dtml-var b>')
        expected = u'helloworld'
        res = html(a='hello', b=u'world')
        self.assertEqual(res, expected)

    def testAB(self):
        html = self.doc_class('<dtml-var a><dtml-var b>')
        expected = 'hello\xc8'
        res = html(a='hello', b='\xc8')
        self.assertEqual(res, expected)

    def testUB(self):
        html = self.doc_class('<dtml-var a><dtml-var b>')
        expected = u'hello\xc8'
        res = html(a=u'hello', b='\xc3\x88')
        self.assertEqual(res, expected)

    def testUB2(self):
        html = self.doc_class('<dtml-var a><dtml-var b>')
        expected = u'\u07d0\xc8'
        res = html(a=unichr(2000), b='\xc3\x88')
        self.assertEqual(res, expected)

    def testUnicodeStr(self):
        html = self.doc_class('<dtml-var a><dtml-var b>')
        expected = u'\u07d0\xc8'
        res = html(a=force_str(unichr(2000)), b='\xc3\x88')
        self.assertEqual(res, expected)

    def testUqB(self):
        html = self.doc_class('<dtml-var a html_quote><dtml-var b>')
        expected = u'he&gt;llo\xc8'
        res = html(a=u'he>llo', b='\xc3\x88')
        self.assertEqual(res, expected)

    def testSize(self):
        if six.PY3:
            html = self.doc_class('<dtml-var "_.chr(200)*4" size=2>')
            expected = '\xc3\x88' * 2 + '...'
        else:
            html = self.doc_class('<dtml-var "_.unichr(200)*4" size=2>')
            expected = unichr(200) * 2 + '...'
        res = html()
        self.assertEqual(res, expected)
