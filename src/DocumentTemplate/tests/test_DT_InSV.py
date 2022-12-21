import re
import string
import unittest


SEQUENCE = tuple(string.ascii_letters)


class sequence_variables_Tests(unittest.TestCase):

    def _makeOne(self, *args, **kw):
        from DocumentTemplate.DT_InSV import sequence_variables
        return sequence_variables(*args, **kw)

    def test_initialization_defaults(self):
        sv = self._makeOne()

        self.assertEqual(len(sv), 1)
        self.assertEqual(sv.number(0), 1)
        self.assertTrue(sv.even(2))
        self.assertFalse(sv.even(1))
        self.assertFalse(sv.odd(2))
        self.assertTrue(sv.odd(1))
        self.assertEqual(sv.letter(0), 'a')
        self.assertEqual(sv.Letter(0), 'A')
        self.assertEqual(sv.roman(0), 'i')
        self.assertEqual(sv.Roman(0), 'I')
        self.assertRaises(TypeError, sv.key, 0)
        self.assertRaises(TypeError, sv.item, 0)
        self.assertRaises(TypeError, sv.value, 0, '')
        self.assertEqual(sv.first('foo'), 1)
        self.assertRaises(KeyError, sv.last, 'foo')
        self.assertRaises(TypeError, sv.length, 'foo')
        self.assertRaises(KeyError, sv.query, 'foo')
        self.assertRaises(KeyError, sv.statistics, 'foo', 'bar')
        self.assertRaises(KeyError, sv.next_batches, suffix='foo', key='bar')
        self.assertEqual(sv.next_batches(), ())
        self.assertRaises(KeyError, sv.previous_batches,
                          suffix='foo', key='bar')
        self.assertEqual(sv.previous_batches(), ())
        self.assertRaises(KeyError, sv.__getitem__, 'foo')

    def test__setitem__getitem__(self):
        sv = self._makeOne(alt_prefix='prf')

        sv['foo'] = 1
        self.assertEqual(sv['foo'], 1)
        self.assertEqual(sv['prf_foo'], 1)

        # Special case for keys starting with ``sequence-``
        sv['sequence-foo'] = 1
        self.assertEqual(sv['sequence-foo'], 1)
        self.assertEqual(sv['prf_foo'], 1)
        self.assertRaises(KeyError, sv.__getitem__, 'prf_sequence-foo')

    def test_alt_prefix(self):
        sv = self._makeOne(alt_prefix='prf')

        self.assertEqual(sv.alt_prefix, 'prf_')

    def test_length(self):
        sv = self._makeOne(items=(1, 2, 3))

        self.assertEqual(sv.length('ignored'), 3)

    def test_query(self):
        start_re = re.compile(r'^foo')

        sv = self._makeOne(start_name_re=start_re, query_string='foo=bar')
        self.assertEqual(sv.query('ignored'), '?foo=bar&')

        sv = self._makeOne(start_name_re=start_re, query_string='?foo=bar')
        self.assertEqual(sv.query('ignored'), '?foo=bar&')

        sv = self._makeOne(start_name_re=start_re, query_string='&foo=bar')
        self.assertEqual(sv.query('ignored'), '?foo=bar&')

        sv = self._makeOne(start_name_re=start_re, query_string='foo=bar&')
        self.assertEqual(sv.query('ignored'), '?foo=bar&')

        sv = self._makeOne(start_name_re=start_re, query_string='?&')
        self.assertEqual(sv.query('ignored'), '?')

    def test_Roman(self):
        # Method converts index from zero-based to 1-based first by adding 1!
        sv = self._makeOne()

        self.assertEqual(sv.Roman(1), 'II')

    def test_roman(self):
        # Method converts index from zero-based to 1-based first by adding 1!
        sv = self._makeOne()

        self.assertEqual(sv.roman(1), 'ii')


class opt_Tests(unittest.TestCase):
    """ The opt function calculates batch values

    The inputs are the batch start, end, size, the number of allowed orphans
    and the batched sequence itself. The return value is a tuple with the
    calculated start, end and size.
    """

    def _makeOne(self, *args):
        from DocumentTemplate.DT_InSV import opt
        return opt(*args)

    def test_opt(self):
        self.assertEqual(self._makeOne(1, 20, 10, 1, SEQUENCE), (1, 20, 10))

        # No size given
        # Resets size to sequence length
        self.assertEqual(self._makeOne(1, 20, 0, 1, SEQUENCE), (1, 20, 20))

        # No start given
        # Resets start and end to the last <size> elements of the sequence
        self.assertEqual(self._makeOne(0, 20, 10, 1, SEQUENCE), (11, 20, 10))

        # No end given
        # Resets end to start plus size
        self.assertEqual(self._makeOne(1, 0, 10, 1, SEQUENCE), (1, 10, 10))

        # Start beyond sequence size, reset start to sequence length
        self.assertEqual(self._makeOne(80, 90, 10, 1, SEQUENCE), (52, 90, 10))

        # End beyond sequence size
        self.assertEqual(self._makeOne(1, 80, 10, 1, SEQUENCE), (1, 80, 10))

        # No start given and end beyond sequence size
        # Resets start and end to the last <size> elements of the sequence
        self.assertEqual(self._makeOne(0, 80, 10, 1, SEQUENCE), (43, 52, 10))

        # End < start
        # Resets end to match start
        self.assertEqual(self._makeOne(10, 1, 10, 1, SEQUENCE), (10, 10, 10))

        # No start and no end given
        # Resets start to 1 and end to start plus size
        self.assertEqual(self._makeOne(0, 0, 10, 1, SEQUENCE), (1, 10, 10))

        # No start and no end given and size > sequence length
        # Resets start to 1 and end to sequence length
        self.assertEqual(self._makeOne(0, 0, 90, 1, SEQUENCE), (1, 52, 90))

        # Nothing given
        # Uses default values
        self.assertEqual(self._makeOne(0, 0, 0, 0, SEQUENCE), (1, 7, 7))
