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

from ExtensionClass import Base
from DocumentTemplate._DocumentTemplate import TemplateDict


class DummyDocTemp(object):

    def __init__(self, name, temp=True):
        self.name = name
        self.isDocTemp = temp

    def __call__(self, *args):
        return ('doctemp', self.name, args)


class DummyNamespace(object):

    isDocTemp = True

    def __init__(self, name):
        self.name = name

    def __render_with_namespace__(self, *args):
        return ('namespace', self.name, args)


class TestTemplateDict(unittest.TestCase):

    def test_extensionclass(self):
        self.assertTrue(issubclass(TemplateDict, Base))
        self.assertTrue(isinstance(TemplateDict(), Base))
        self.assertFalse(hasattr(TemplateDict, '__of__'))

    def test_empty(self):
        td = TemplateDict()
        self.assertEqual(len(td), 0)
        self.assertEqual(td.level, 0)
        self.assertRaises(AttributeError, getattr, td, 'foo')
        self.assertFalse(td.has_key('foo'))  # NOQA
        self.assertFalse('foo' in td)
        self.assertFalse(td.has_key('level'))  # NOQA
        self.assertFalse('level' in td)
        self.assertRaises(KeyError, td.getitem, 0)
        self.assertFalse(0 in td)
        with self.assertRaises(KeyError):
            td['foo']
        self.assertTrue(td() is None)

    def test_level(self):
        td = TemplateDict()
        td.level = 10
        self.assertEqual(td.level, 10)

    def test_push_pop(self):
        td = TemplateDict()
        td._push('foo')
        td._push('bar')
        self.assertEqual(len(td), 6)
        self.assertEqual(td[0], 'b')
        self.assertEqual(td[:], 'bar')
        self.assertEqual(td.getitem(-1), 'r')
        self.assertTrue(td() is None)
        self.assertEqual(td._pop(1), 'bar')
        self.assertEqual(len(td), 3)
        self.assertEqual(td[:], 'foo')

    def test_attr(self):
        td = TemplateDict()
        td.foo = 1
        td.bar = 2
        td.baz = None
        self.assertEqual(len(td), 0)
        self.assertRaises(KeyError, td.getitem, 0)
        self.assertFalse(td.has_key('foo'))  # NOQA
        self.assertFalse('foo' in td)
        self.assertEqual(td.foo, 1)
        self.assertEqual(td.bar, 2)
        self.assertEqual(td.baz, None)

    def test_call(self):
        td = TemplateDict()
        result = td({'one': 1}, two=2)
        self.assertTrue(isinstance(result, tuple))
        self.assertEqual(len(result), 1)
        inst = result[0]
        self.assertEqual(type(inst).__name__, 'DictInstance')
        self.assertEqual(inst.one, 1)
        self.assertEqual(inst.two, 2)
        self.assertRaises(AttributeError, getattr, inst, 'three')
        self.assertFalse(isinstance(inst, Base))

    def test_stack(self):
        td = TemplateDict()
        td._push({'one': 1, 'two': 2})
        td._push(object())
        td._push({'two': 22, 'three': 3})
        td._push({'four': None})
        self.assertTrue('three' in td)
        self.assertEqual(td.getitem('three'), 3)
        self.assertTrue('two' in td)
        self.assertEqual(td.getitem('two'), 22)
        self.assertRaises(TypeError, td.__contains__, 'one')
        self.assertRaises(TypeError, td.getitem, 'one')
        self.assertTrue('four' in td)
        self.assertEqual(td.getitem('four'), None)

    def test_callable_doctemp(self):
        td = TemplateDict()
        td._push({'zero': DummyDocTemp('zero', False)})
        td._push({'one': DummyDocTemp('one'), 'two': 2})
        td._push({'two': DummyDocTemp('two'), 'three': 3})
        self.assertEqual(td['three'], 3)
        self.assertEqual(td['two'], ('doctemp', 'two', (None, td)))
        self.assertEqual(td['one'], ('doctemp', 'one', (None, td)))
        self.assertEqual(td['zero'], ('doctemp', 'zero', ()))

    def test_callable_namespace(self):
        td = TemplateDict()
        td._push({'one': DummyNamespace('one')})
        self.assertEqual(td['one'], ('namespace', 'one', (td, )))
