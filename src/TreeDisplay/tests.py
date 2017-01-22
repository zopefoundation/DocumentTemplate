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

import unittest

from TreeDisplay import TreeTag


class TestTreeTag(unittest.TestCase):

    def test_encode_decode_seq(self):
        state = [['AAAAAAAAAAE=', [['AAAAAAAAAAY=']]]]
        self.assertEqual(TreeTag.decode_seq(TreeTag.encode_seq(state)), state)
