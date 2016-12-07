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

from cStringIO import StringIO
import pickle
import unittest

from TreeDisplay.TreeTag import (
    MiniUnpickler,
)


class _junk_class(object):
    pass


class TestMiniPickle(unittest.TestCase):

    def _should_succeed(self, x, binary=1):
        if x != MiniUnpickler(StringIO(pickle.dumps(x, binary))).load():
            raise ValueError(x)

    def _should_fail(self, x, binary=1):
        try:
            MiniUnpickler(StringIO(pickle.dumps(x, binary))).load()
            raise ValueError(x)
        except pickle.UnpicklingError as e:
            if e[0] != 'Refused':
                raise ValueError(x)

    def test_mini_pickle(self):
        self._should_succeed('hello')
        self._should_succeed(1)
        self._should_succeed(1.0)
        self._should_succeed((1, 2, 3))
        self._should_succeed([1, 2, 3])
        self._should_succeed({1: 2, 3: 4})
        self._should_fail(open)
        self._should_fail(_junk_class)
        self._should_fail(_junk_class())
