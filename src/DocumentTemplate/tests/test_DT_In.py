import unittest


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
