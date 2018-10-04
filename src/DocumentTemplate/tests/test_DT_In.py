import unittest

from DocumentTemplate.DT_Util import ParseError


class DummySection(object):
    blocks = ['dummy']


class TestIn(unittest.TestCase):
    """Testing ..DT_in.InClass."""

    def _getTargetClass(self):
        from DocumentTemplate.DT_In import InClass
        return InClass

    def _makeOne(self, *args):
        blocks = [('in', ' '.join(args), DummySection())]
        return self._getTargetClass()(blocks)

    def test_sort_sequence(self):
        """It does not break on duplicate sort keys at a list of dicts."""
        stmt = self._makeOne('seq', 'mapping', 'sort=key')
        seq = [
            {'key': 'c', 'data': '3'},
            {'key': 'a', 'data': '1'},
            {'key': 'b', 'data': '2'},
            {'key': 'a', 'data': '2'},
        ]
        result = stmt.sort_sequence(seq, 'key')
        self.assertEqual([
            {'key': 'a', 'data': '1'},
            {'key': 'a', 'data': '2'},
            {'key': 'b', 'data': '2'},
            {'key': 'c', 'data': '3'},
        ], result)


class DT_In_Tests(unittest.TestCase):
    """Functional testing ..DT_In.InClass."""

    def _get_doc_class(self):
        from DocumentTemplate.DT_HTML import HTML
        return HTML

    doc_class = property(_get_doc_class,)

    def test_DT_In__InClass____init__1(self):
        """It only allows alphanumeric + `_` characters in prefix."""
        sequence = ['a', 'b', 'c']
        html = self.doc_class(
            '<dtml-in seq prefix="te/_st">'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '</dtml-in>')
        with self.assertRaisesRegexp(ParseError, '^prefix is not a simple '):
                html(seq=sequence)