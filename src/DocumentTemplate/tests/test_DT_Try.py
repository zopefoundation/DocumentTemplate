import unittest

from DocumentTemplate.DT_Util import ParseError
from DocumentTemplate.DT_Raise import InvalidErrorTypeExpression


class DT_Try_Tests(unittest.TestCase):
    """Testing ..DT_Try.Try."""

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

    def test_DT_Try__Try____init__1(self):
        """It allows only one else block."""
        html = self.doc_class(
            '<dtml-try>'
            'Variable "name": '
            '<dtml-except>'
            '<dtml-else>'
            '<dtml-var expr="str(100)">'
            '<dtml-else>'
            '<dtml-var expr="str(110)">'
            '</dtml-try>')
        with self.assertRaisesRegex(ParseError, '^No more than one else '):
            html()

    def test_DT_Try__Try____init__2(self):
        """It allows the else block only in last position."""
        html = self.doc_class(
            '<dtml-try>'
            'Variable "name": '
            '<dtml-else>'
            '<dtml-var expr="str(100)">'
            '<dtml-except>'
            '</dtml-try>')
        with self.assertRaisesRegex(
                ParseError, '^The else block should be the last '):
            html()

    def test_DT_Try__Try____init__3(self):
        """It allows no except block with a finally block."""
        html = self.doc_class(
            '<dtml-try>'
            'Variable "name": '
            '<dtml-except>'
            '<dtml-finally>'
            '<dtml-var expr="str(100)">'
            '</dtml-try>')
        with self.assertRaisesRegex(
                ParseError, '^A try..finally combination cannot '):
            html()

    def test_DT_Try__Try____init__4(self):
        """It allows only one default exception handler."""
        html = self.doc_class(
            '<dtml-try>'
            'Variable "name": '
            '<dtml-except>'
            '<dtml-var expr="str(100)">'
            '<dtml-except>'
            '<dtml-var expr="str(110)">'
            '</dtml-try>')
        with self.assertRaisesRegex(
                ParseError, '^Only one default exception handler '):
            html()

    def test_DT_Try__Try__01(self):
        """It renders a try block if no exception occurs."""
        html = self.doc_class(
            '<dtml-try>'
            'Variable "name": '
            '<dtml-var expr="str(100)">'
            '</dtml-try>')
        res = html()
        expected = 'Variable "name": 100'
        self.assertEqual(res, expected)

    def test_DT_Try__Try__02(self):
        """It renders the except block if an exception occurs."""
        html = self.doc_class(
            '<dtml-try>'
            'Variable "name": '
            '<dtml-var expr="not_defined">'
            '<dtml-except>'
            'Exception variable: '
            '<dtml-var expr="str(100)">'
            '</dtml-try>')
        res = html()
        expected = 'Exception variable: 100'
        self.assertEqual(res, expected)

    def test_DT_Try__Try__03(self):
        """It renders the else block if no exception occurs."""
        html = self.doc_class(
            '<dtml-try>'
            'Variable "name": '
            '<dtml-var expr="str(100)"> '
            '<dtml-except>'
            'Exception variable: '
            '<dtml-var expr="str(110)"> '
            '<dtml-else>'
            'Else variable: '
            '<dtml-var expr="str(111)"> '
            '</dtml-try>')
        res = html()
        expected = ('Variable "name": 100 '
                    'Else variable: 111 ')
        self.assertEqual(res, expected)

    def test_DT_Try__Try__04(self):
        """It executes the finally block if no exception occurs."""
        html = self.doc_class(
            '<dtml-call expr="dummy_list.append(110)">'
            '<dtml-try>'
            'Variable "name": '
            '<dtml-var expr="str(100)"> '
            '<dtml-finally>'
            'Finally variable: '
            '<dtml-var expr="str(111)"> '
            '<dtml-call expr="dummy_list.pop(0)">'
            '</dtml-try>')
        dummy_list = [100]

        res = html(dummy_list=dummy_list)
        expected = ('Variable "name": 100 '
                    'Finally variable: 111 ')
        self.assertEqual(res, expected)
        # 100 got removed in the finally block.
        self.assertEqual(dummy_list, [110])

    def test_DT_Try__Try__05(self):
        """It executes the finally block if an exception occurs."""
        html = self.doc_class(
            '<dtml-call expr="dummy_list.append(110)">'
            '<dtml-try>'
            'Variable "name": '
            '<dtml-var expr="not_defined"> '
            '<dtml-finally>'
            'Finally variable: '
            '<dtml-call expr="dummy_list.pop(0)"> '
            '</dtml-try>')
        dummy_list = [100]

        with self.assertRaises(NameError):
            html(dummy_list=dummy_list)
        # 100 got removed in the finally block.
        self.assertEqual(dummy_list, [110])

    def test_DT_Try__Try__06(self):
        """It allows different exception handlers."""
        html = self.doc_class(
            '<dtml-try>'
            'Variable "name": '
            '<dtml-var expr="not_defined">'
            '<dtml-except KeyError>'
            'Exception variable: '
            '<dtml-var expr="str(100)">'
            '<dtml-except NameError>'
            'Exception variable: '
            '<dtml-var expr="str(110)">'
            '</dtml-try>')
        res = html()
        expected = 'Exception variable: 110'
        self.assertEqual(res, expected)

    def test_DT_Try__Try__07(self):
        """It catches errors with handler for base exception."""
        html = self.doc_class(
            '<dtml-try>'
            'Variable "name": '
            '<dtml-raise KeyError></dtml-raise>'
            '<dtml-except NameError>'
            'Exception variable: '
            '<dtml-var expr="str(100)">'
            '<dtml-except LookupError>'
            'Exception variable: '
            '<dtml-var expr="str(110)">'
            '</dtml-try>')
        res = html()
        expected = 'Exception variable: 110'
        self.assertEqual(res, expected)

    def test_DT_Try__Try__08(self):
        """It raises the occurred exception if no exception handler matches."""
        html = self.doc_class(
            '<dtml-try>'
            'Variable "name": '
            '<dtml-var expr="not_defined">'
            '<dtml-except KeyError>'
            'Exception variable: '
            '<dtml-var expr="str(100)">'
            '<dtml-except AttributeError>'
            'Exception variable: '
            '<dtml-var expr="str(110)">'
            '</dtml-try>')
        with self.assertRaises(NameError):
            html()

    def test_DT_Try__Try__09(self):
        """It returns a dtml-return immediately."""
        html = self.doc_class(
            '<dtml-try>'
            'Variable "name": '
            '<dtml-return ret>'
            '<dtml-raise KeyError></dtml-raise>'
            '<dtml-except LookupError>'
            'Exception variable: '
            '<dtml-var expr="str(110)">'
            '</dtml-try>')
        res = html(ret='Return variable: 101')
        expected = 'Return variable: 101'
        self.assertEqual(res, expected)

    def test_DT_Try__Try__10(self):
        """It does not break with strings as exceptions but raises a well

        defined exception in that case."""
        html = self.doc_class(
            '<dtml-try>'
            'Variable "name": '
            '<dtml-raise "FakeError"></dtml-raise>'
            '<dtml-except NameError>'
            'Exception variable: '
            '<dtml-var expr="str(110)">'
            '</dtml-try>')
        with self.assertRaises(InvalidErrorTypeExpression):
            html()
