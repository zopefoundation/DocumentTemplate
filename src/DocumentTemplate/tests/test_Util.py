from unittest import TestCase

from ..DT_Util import SequenceFromIter
from ..DT_Util import sequence_ensure_subscription
from ..DT_Util import sequence_supports_subscription


class SequenceTests(TestCase):
    def test_supports_str(self):
        self.assertTrue(sequence_supports_subscription(""))

    def test_supports_sequence(self):
        self.assertTrue(sequence_supports_subscription([]))
        self.assertTrue(sequence_supports_subscription([0]))

    def test_supports_mapping(self):
        self.assertFalse(sequence_supports_subscription({}))
        self.assertFalse(sequence_supports_subscription({0: 0}))
        self.assertFalse(sequence_supports_subscription({0: 0, None: None}))

    def test_supports_iter(self):
        self.assertFalse(sequence_supports_subscription((i for i in range(0))))
        self.assertFalse(sequence_supports_subscription((i for i in range(1))))

    def test_supports_SequenceFromIter(self):
        S = SequenceFromIter
        self.assertTrue(
            sequence_supports_subscription(S((i for i in range(0)))))
        self.assertTrue(
            sequence_supports_subscription(S((i for i in range(1)))))

    def test_supports_RuntimeError(self):
        # check that ``ZTUtils.Lazy.Lazy`` is recognized
        class RTSequence(list):
            def __getitem__(self, idx):
                if not isinstance(idx, int):
                    raise RuntimeError

        s = RTSequence(i for i in range(0))
        self.assertTrue(sequence_supports_subscription(s))
        s = RTSequence(i for i in range(2))
        self.assertTrue(sequence_supports_subscription(s))

    def test_ensure_sequence(self):
        s = []
        self.assertIs(s, sequence_ensure_subscription(s))

    def test_ensure_iter(self):
        self.assertIsInstance(
            sequence_ensure_subscription(i for i in range(0)),
            SequenceFromIter)

    def test_FromIter(self):
        S = SequenceFromIter
        with self.assertRaises(IndexError):
            S(i for i in range(0))[0]
        s = S(i for i in range(2))
        with self.assertRaises(IndexError):
            s[-1]
        self.assertEqual(s[0], 0)
        self.assertEqual(s[0], 0)  # ensure nothing bad happens
        self.assertEqual(s[1], 1)
        with self.assertRaises(IndexError):
            s[2]
        self.assertEqual(list(s), [0, 1])
        self.assertEqual(len(s), 2)
        self.assertEqual(len(S(i for i in range(2))), 2)
