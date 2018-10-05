import unittest

from DocumentTemplate.DT_Util import ParseError


class DummySection(object):
    blocks = ['dummy']


class Dummy(object):
    """Dummy with attribute"""

    def __init__(self, name, number=0):
        self.name = name
        self.number = number

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

    def test_DT_In__InClass__renderwob__06(self):
        """It allows multisort."""
        seq = [Dummy('alberta', 2), Dummy('alberta', 1), Dummy('barnie', 1)]
        html = self.doc_class(
            '<dtml-in seq sort="name,number">'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-var-name> , <dtml-var sequence-var-number>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = (
            'Item 1: alberta , 1'
            'Item 2: alberta , 2'
            'Item 3: barnie , 1')
        self.assertEqual(res, expected)
        html = self.doc_class(
            '<dtml-in seq sort="number,name">'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-var-name> , <dtml-var sequence-var-number>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = (
            'Item 1: alberta , 1'
            'Item 2: barnie , 1'
            'Item 3: alberta , 2')
        self.assertEqual(res, expected)

    def test_DT_In__InClass__renderwob__07(self):
        """It allows complex multisort. Smoke test."""
        # This test also covers most of `SortBy`.
        seq = [Dummy('alberta', 2), Dummy('alberta', 1), Dummy('barnie', 1)]
        html = self.doc_class(
            '<dtml-in seq sort="name/nocase/asc,number/cmp/desc">'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-var-name> , <dtml-var sequence-var-number>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = (
            'Item 1: alberta , 2'
            'Item 2: alberta , 1'
            'Item 3: barnie , 1')
        self.assertEqual(res, expected)
        # It can sort the other way round
        html = self.doc_class(
            '<dtml-in seq sort="number/cmp/asc,name/strcoll/desc">'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-var-name> , <dtml-var sequence-var-number>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = (
            'Item 1: barnie , 1'
            'Item 2: alberta , 1'
            'Item 3: alberta , 2')
        self.assertEqual(res, expected)
        # It is possible to omit parts of complex sort.
        seq.append(Dummy('alberta', 1))
        html = self.doc_class(
            '<dtml-in seq sort="number,name/strcoll_nocase">'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-var-name> , <dtml-var sequence-var-number>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = (
            'Item 1: alberta , 1'
            'Item 2: alberta , 1'
            'Item 3: barnie , 1'
            'Item 4: alberta , 2')
        self.assertEqual(res, expected)