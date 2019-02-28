import unittest

from DocumentTemplate.DT_Util import ParseError


class DummySection(object):
    blocks = ['dummy']


class Dummy(object):
    """Dummy with attribute"""

    def __init__(self, name, number=0, _callable=0):
        self.name = name
        self.number = number
        self._callable = _callable

    @property
    def maybe_callable(self):
        return self._callable


class TestIn(unittest.TestCase):
    """Testing ..DT_In.InClass."""

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

    def assertRaisesRegex(self, *args, **kw):
        try:
            # available from Python 3.2
            return unittest.TestCase.assertRaisesRegex(self, *args, **kw)
        except AttributeError:
            # only available till Python 3.7
            return unittest.TestCase.assertRaisesRegexp(self, *args, **kw)

    @property
    def doc_class(self):
        from DocumentTemplate.DT_HTML import HTML
        return HTML

    def test_DT_In__InClass____init__1(self):
        """It only allows alphanumeric + `_` characters in prefix."""
        sequence = ['a', 'b', 'c']
        html = self.doc_class(
            '<dtml-in seq prefix="te/_st">'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '</dtml-in>')
        with self.assertRaisesRegex(ParseError, '^prefix is not a simple '):
            html(seq=sequence)

    def test_DT_In__InClass____init__2(self):
        """It only allows one else block."""
        html = self.doc_class(
            '<dtml-in seq>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '<dtml-else>'
            'No items available'
            '</dtml-in>')
        res = html(seq=[])
        expected = 'No items available'
        self.assertEqual(res, expected)

        html = self.doc_class(
            '<dtml-in seq>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '<dtml-else>'
            'No items available'
            '<dtml-else>'
            'Still no items available'
            '</dtml-in>')
        with self.assertRaisesRegex(ParseError, '^too many else blocks'):
            html(seq=[])

    def test_DT_In__InClass____init__3(self):
        """It restricts certain args to batch processing."""
        batch_args = ('orphan', 'overlap', 'previous', 'next')
        template = (
            '<dtml-in seq {arg}>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '</dtml-in>')

        for arg in batch_args:
            html = self.doc_class(template.format(arg=arg))
            error_msg = 'The {arg} attribute was used'.format(arg=arg)
            with self.assertRaisesRegex(ParseError, error_msg):
                html(seq=['a', 'b'])

    def test_DT_In__InClass____init__4(self):
        """It does not allow strings as sequence.."""
        html = self.doc_class(
            '<dtml-in seq>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '</dtml-in>')
        with self.assertRaisesRegex(ValueError, 'Strings are not allowed as'):
            html(seq="Foo")

    def test_DT_In__InClass____init__5(self):
        """It allows `sequence-item` as sort key resulting in default sort."""
        html = self.doc_class(
            '<dtml-in seq sort=sequence-item>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '</dtml-in>')
        res = html(seq=['c', 'a', 'b'])
        expected = (
            'Item 1: a'
            'Item 2: b'
            'Item 3: c')
        self.assertEqual(res, expected)

    def test_DT_In__InClass__renderwob__01(self):
        """It does not allow strings as sequence."""
        html = self.doc_class(
            '<dtml-in seq>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '</dtml-in>')
        with self.assertRaisesRegex(ValueError, 'Strings are not allowed as'):
            html(seq="Foo")

    def test_DT_In__InClass__renderwob__02(self):
        """It can handle an empty sequence including else."""
        html = self.doc_class(
            'This is in:'
            '<dtml-in seq>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '</dtml-in>'
            'This is else:'
            '<dtml-in seq>'
            'Part <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '<dtml-else>'
            'no items'
            '</dtml-in>')
        res = html(seq=[])
        expected = (
            'This is in:'
            'This is else:'
            'no items')
        self.assertEqual(res, expected)

    def test_DT_In__InClass__renderwob__03(self):
        """It allows expressions as sequence."""
        html = self.doc_class(
            '<dtml-in expr="range(2)">'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '</dtml-in>')
        res = html()
        expected = (
            'Item 1: 0'
            'Item 2: 1')
        self.assertEqual(res, expected)

    def test_DT_In__InClass__renderwob__04(self):
        """It allows to simply sort a sequence."""
        seq = [Dummy('alberta'), Dummy('berta'), Dummy('barnie')]
        html = self.doc_class(
            '<dtml-in seq sort=name>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-var-name>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = (
            'Item 1: alberta'
            'Item 2: barnie'
            'Item 3: berta')
        self.assertEqual(res, expected)
        # Also with sort expression

        def s_expr():
            return "name"

        html = self.doc_class(
            '<dtml-in seq sort_expr="s_expr()">'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-var-name>'
            '</dtml-in>')
        res = html(seq=seq, s_expr=s_expr)
        expected = (
            'Item 1: alberta'
            'Item 2: barnie'
            'Item 3: berta')
        self.assertEqual(res, expected)

    def test_DT_In__InClass__renderwob__05(self):
        """It allows to reverse sort a sequence."""
        seq = [Dummy('alberta'), Dummy('berta'), Dummy('barnie')]
        html = self.doc_class(
            '<dtml-in seq sort=name reverse>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-var-name>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = (
            'Item 1: berta'
            'Item 2: barnie'
            'Item 3: alberta')
        self.assertEqual(res, expected)
        # Also with reverse expression
        html = self.doc_class(
            '<dtml-in seq sort=name/cmp reverse_expr="1==1">'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-var-name>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = (
            'Item 1: berta'
            'Item 2: barnie'
            'Item 3: alberta')
        self.assertEqual(res, expected)

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

    def test_DT_In__InClass__renderwob__08(self):
        """It can iterate over list of tuples."""
        seq = [('alberta', 3), ('ylberta', 1), ('barnie', 2)]
        html = self.doc_class(
            '<dtml-in seq>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = (
            'Item 1: 3'
            'Item 2: 1'
            'Item 3: 2')
        self.assertEqual(res, expected)
        # also sorted
        html = self.doc_class(
            '<dtml-in seq sort>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = (
            'Item 1: 3'
            'Item 2: 2'
            'Item 3: 1')
        self.assertEqual(res, expected)

    def test_DT_In__InClass__renderwob__09(self):
        """It can also contain callables as values."""
        # It catches errors and treats those as smallest
        seq = [
            Dummy('alberta', _callable=lambda: 3),
            Dummy('ylberta', _callable=lambda: 0),
            Dummy('barnie', _callable=lambda: [][2]),
        ]
        html = self.doc_class(
            '<dtml-in seq sort=maybe_callable/cmp>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-var-name>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = (
            'Item 1: barnie'
            'Item 2: ylberta'
            'Item 3: alberta')
        self.assertEqual(res, expected)

    def test_DT_In__InClass__renderwb__01(self):
        """It does not allow strings as sequence in batch mode."""
        html = self.doc_class(
            '<dtml-in seq size=1>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '</dtml-in>')
        with self.assertRaisesRegex(ValueError, 'Strings are not allowed as'):
            html(seq="Foo")

    def test_DT_In__InClass__renderwb__02(self):
        """It can handle an empty sequence including else."""
        html = self.doc_class(
            'This is in:'
            '<dtml-in seq size=1>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '</dtml-in>'
            'This is else:'
            '<dtml-in seq size=1>'
            'Part <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '<dtml-else>'
            'no items'
            '</dtml-in>')
        res = html(seq=[])
        expected = (
            'This is in:'
            'This is else:'
            'no items')
        self.assertEqual(res, expected)

    def test_DT_In__InClass__renderwb__03(self):
        """It allows expressions as sequence."""
        html = self.doc_class(
            '<dtml-in expr="range(2)" size=1>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '</dtml-in>')
        res = html()
        expected = ('Item 1: 0')
        self.assertEqual(res, expected)

    def test_DT_In__InClass__renderwb__04(self):
        """It allows to simply sort a sequence."""
        seq = [Dummy('alberta'), Dummy('berta'), Dummy('barnie')]
        html = self.doc_class(
            '<dtml-in seq sort=name start=1>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-var-name>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = (
            'Item 1: alberta'
            'Item 2: barnie'
            'Item 3: berta')
        self.assertEqual(res, expected)
        # Also with sort expression

        def s_expr():
            return "name"

        html = self.doc_class(
            '<dtml-in seq sort_expr="s_expr()" start=1>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-var-name>'
            '</dtml-in>')
        res = html(seq=seq, s_expr=s_expr)
        expected = (
            'Item 1: alberta'
            'Item 2: barnie'
            'Item 3: berta')
        self.assertEqual(res, expected)

    def test_DT_In__InClass__renderwb__05(self):
        """It allows to reverse sort a sequence."""
        seq = [Dummy('alberta'), Dummy('berta'), Dummy('barnie')]
        html = self.doc_class(
            '<dtml-in seq sort=name reverse start=1>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-var-name>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = (
            'Item 1: berta'
            'Item 2: barnie'
            'Item 3: alberta')
        self.assertEqual(res, expected)
        # Also with reverse expression
        html = self.doc_class(
            '<dtml-in seq sort=name reverse_expr="1==1" start=1>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-var-name>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = (
            'Item 1: berta'
            'Item 2: barnie'
            'Item 3: alberta')
        self.assertEqual(res, expected)

    def test_DT_In__InClass__renderwb__06(self):
        """It can access previous and next batch of a sequence."""
        seq = [Dummy('alberta'), Dummy('berta'), Dummy('barnie')]
        html = self.doc_class(
            '<dtml-in seq sort=name start=2 previous size=1>'
            'Prev index: <dtml-var previous-sequence-start-number> '
            '</dtml-in>'
            '<dtml-in seq sort=name start=2 next size=1>'
            'Next index: <dtml-var next-sequence-start-number>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = ('Prev index: 1 '
                    'Next index: 3')
        self.assertEqual(res, expected)
        # Also with else clauses for edges of the sequence
        html = self.doc_class(
            '<dtml-in seq sort=name start=1 previous size=1>'
            'Prev index: <dtml-var previous-sequence-start-number> '
            '<dtml-else>'
            'No prev '
            '</dtml-in>'
            '<dtml-in seq sort=name start=3 next size=1>'
            'Next index: <dtml-var next-sequence-start-number>'
            '<dtml-else>'
            'No next'
            '</dtml-in>')
        res = html(seq=seq)
        expected = ('No prev '
                    'No next')
        self.assertEqual(res, expected)
        # or it renders nothing if no else is given
        html = self.doc_class(
            '<dtml-in seq sort=name start=1 previous size=1>'
            'Prev index: <dtml-var previous-sequence-start-number> '
            '</dtml-in>'
            '<dtml-in seq sort=name start=3 next size=1>'
            'Next index: <dtml-var next-sequence-start-number>'
            '</dtml-in>')
        res = html(seq=seq)
        expected = ''
        self.assertEqual(res, expected)

    def test_DT_In__make_sortfunction__1(self):
        """It allows two slashes at maximum in sort expression."""
        seq = [Dummy('alberta'), Dummy('berta'), Dummy('barnie')]
        html = self.doc_class(
            '<dtml-in seq sort=name/cmp/asc/wrong>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '</dtml-in>')
        error_msg = 'sort option must contain no more than 2 slashes'
        with self.assertRaisesRegex(SyntaxError, error_msg):
            html(seq=seq)

    def test_DT_In__make_sortfunction__2(self):
        """It allows only asc and desc as sort order in sort expression."""
        seq = [Dummy('alberta'), Dummy('berta'), Dummy('barnie')]
        html = self.doc_class(
            '<dtml-in seq sort=name/cmp/wrong>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-item>'
            '</dtml-in>')
        error_msg = 'sort oder must be either ASC or DESC'
        with self.assertRaisesRegex(SyntaxError, error_msg):
            html(seq=seq)

    def test_DT_In__make_sortfunction__3(self):
        """It can use a local function for comparison."""
        def local_cmp(a, b):
            return (a > b) - (a < b)

        seq = [Dummy('alberta'), Dummy('berta'), Dummy('barnie')]
        html = self.doc_class(
            '<dtml-in seq sort=name/local_cmp/desc>'
            'Item <dtml-var sequence-number>: '
            '<dtml-var sequence-var-name>'
            '</dtml-in>')
        res = html(seq=seq, local_cmp=local_cmp)
        expected = (
            'Item 1: berta'
            'Item 2: barnie'
            'Item 3: alberta')
        self.assertEqual(res, expected)
