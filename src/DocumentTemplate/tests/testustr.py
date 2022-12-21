##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""ustr unit tests.
"""

import unittest


class force_str:
    # A class whose string representation is not always a plain string:

    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s


class Foo(str):
    pass


class Bar(str):
    pass


class RequestLike:
    def __str__(self):
        return "RequestLike"

    args = ()  # to confuse `ustr._exception_str`


class UnicodeTests(unittest.TestCase):

    def test_bare_string_literall(self):
        from DocumentTemplate.ustr import ustr
        a = ustr('hello')
        self.assertEqual(a, 'hello')

    def test_with_force_str(self):
        from DocumentTemplate.ustr import ustr
        a = ustr(force_str('hello'))
        self.assertEqual(a, 'hello')

    def test_RequestLike(self):
        from DocumentTemplate.ustr import ustr
        self.assertEqual(ustr(RequestLike()), "RequestLike")

    def test_with_non_ascii_char(self):
        from DocumentTemplate.ustr import ustr
        a = ustr(chr(200))
        self.assertEqual(a, chr(200))

    def test_with_force_str_non_ascii_char(self):
        from DocumentTemplate.ustr import ustr
        a = ustr(force_str(chr(200)))
        self.assertEqual(a, chr(200))

    def test_with_int(self):
        from DocumentTemplate.ustr import ustr
        a = ustr(22)
        self.assertEqual(a, '22')

    def test_with_list(self):
        from DocumentTemplate.ustr import ustr
        a = ustr([1, 2, 3])
        self.assertEqual(a, '[1, 2, 3]')

    def test_w_str_literal(self):
        from DocumentTemplate.ustr import ustr
        a = ustr('hello')
        self.assertEqual(a, 'hello')

    def test_w_force_str_str_literal(self):
        from DocumentTemplate.ustr import ustr
        a = ustr(force_str('hello'))
        self.assertEqual(a, 'hello')

    def test_w_chr(self):
        from DocumentTemplate.ustr import ustr
        a = ustr(chr(200))
        self.assertEqual(a, chr(200))

    def test_w_force_str_chr(self):
        from DocumentTemplate.ustr import ustr
        a = ustr(force_str(chr(200)))
        self.assertEqual(a, chr(200))

    def test_w_chr_in_exception(self):
        from DocumentTemplate.ustr import ustr
        a = ustr(ValueError(chr(200)))
        self.assertEqual(a, chr(200))

    def testCustomStrings(self):
        from DocumentTemplate.ustr import ustr
        a = ustr(Foo('foo'))
        self.assertEqual(type(a), Foo)
        a = ustr(Bar('bar'))
        self.assertEqual(type(a), Bar)
