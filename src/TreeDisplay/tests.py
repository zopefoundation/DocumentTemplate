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


class FakeResponse:

    def setCookie(self, name, value):
        setattr(self, name, value)


class DummyContent:

    def __init__(self, id):
        self.id = id

    def tpId(self):
        return self.id


class DummyFolder:

    def tpValues(self):
        return [DummyContent('id1'),
                DummyContent('id2')]


class TestTreeTag(unittest.TestCase):

    @property
    def doc_class(self):
        from DocumentTemplate.DT_HTML import HTML
        return HTML

    def _render(self, text, **kw):
        html = self.doc_class(text)
        return html(URL='/', RESPONSE=FakeResponse(), **kw)

    def test_instantiation_empty(self):
        res = self._render('<dtml-tree fldr></dtml-tree>', fldr=1)
        self.assertEqual(res, '<table cellspacing="0">\n</table>\n')

    def test_instantiation(self):
        res = self._render('<dtml-tree fldr></dtml-tree>', fldr=DummyFolder())
        self.assertEqual(res, EMPTY_TREE)

    def test_encode_decode_seq(self):
        state = [['AAAAAAAAAAE=', [['AAAAAAAAAAY=']]]]
        self.assertEqual(TreeTag.decode_seq(TreeTag.encode_seq(state)), state)


EMPTY_TREE = """\
<table cellspacing="0">
<tr>
<td width="16" style="white-space: nowrap"></td>
<td valign="top" align="left"></td>
</tr>
<tr>
<td width="16" style="white-space: nowrap"></td>
<td valign="top" align="left"></td>
</tr>
</table>
"""
