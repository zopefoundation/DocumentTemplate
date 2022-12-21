import unittest

from DocumentTemplate.DT_Util import ParseError


class DT_If_Tests(unittest.TestCase):
    """Functional testing ..DT_If.If."""

    @property
    def doc_class(self):
        from DocumentTemplate.DT_HTML import HTML
        return HTML

    def test_DT_If_if_else(self):
        """ Test if and else """
        html = self.doc_class(
            '<dtml-if foo>'
            'Found it'
            '<dtml-else>'
            'No items available'
            '</dtml-if>')

        self.assertEqual(html(foo=None), 'No items available')
        self.assertEqual(html(foo=1), 'Found it')

    def test_DT_If_if_elif_else(self):
        """ Test if and else """
        html = self.doc_class(
            '<dtml-if foo>'
            'Found it'
            '<dtml-elif bar>'
            'Found bar'
            '<dtml-else>'
            'No items available'
            '</dtml-if>')

        self.assertEqual(html(foo=None, bar=None), 'No items available')
        self.assertEqual(html(foo=1), 'Found it')
        self.assertEqual(html(bar=1), 'Found bar')

    def test_DT_If_if_elif_else_expression(self):
        """ Test if and else """
        html = self.doc_class(
            '<dtml-if "foo == 1">'
            'Foo is 1'
            '<dtml-elif "foo > 1">'
            'Foo > 1'
            '<dtml-else>'
            'Foo undefined or < 1'
            '</dtml-if>')

        self.assertEqual(html(foo=0), 'Foo undefined or < 1')
        self.assertEqual(html(foo=1), 'Foo is 1')
        self.assertEqual(html(foo=10), 'Foo > 1')

    def test_DT_If_too_many_else(self):
        """ Only one else clause allowed """
        html = self.doc_class(
            '<dtml-if foo>'
            'Found it'
            '<dtml-else>'
            'No items available'
            '<dtml-else>'
            'Still no items available'
            '</dtml-if>')
        with self.assertRaisesRegex(ParseError, '^more than one else tag'):
            html(foo=None)

    def test_DT_If_undefined_variable_is_false(self):
        """ If the test variable does not exist it is considered False """
        html = self.doc_class(
            '<dtml-if foo>'
            'Found it'
            '<dtml-else>'
            'No items available'
            '</dtml-if>')

        self.assertEqual(html(), 'No items available')


class DT_Unless_Tests(unittest.TestCase):
    """Functional testing ..DT_If.Unless."""

    @property
    def doc_class(self):
        from DocumentTemplate.DT_HTML import HTML
        return HTML

    def test_DT_Unless(self):
        """ Test simple unless """
        html = self.doc_class(
            '<dtml-unless foo>'
            'Foo not true'
            '</dtml-unless>')

        self.assertEqual(html(foo=None), 'Foo not true')
        self.assertFalse(html(foo=1))

    def test_DT_Unless_expression(self):
        """ Test simple unless """
        html = self.doc_class(
            '<dtml-unless "foo == 1">'
            'Foo not 1'
            '</dtml-unless>')

        self.assertEqual(html(foo=0), 'Foo not 1')
        self.assertFalse(html(foo=1))

    def test_DT_IUnless_no_else(self):
        """ Only one else clause allowed """
        html = self.doc_class(
            '<dtml-unless foo>'
            'Foo not true'
            '<dtml-else>'
            'Foo is true'
            '</dtml-unless>')

        with self.assertRaisesRegex(ParseError, '^unexpected end tag'):
            html(foo=None)

    def test_DT_IUnless_undefined_variable_is_false(self):
        """ If the test variable does not exist it is considered False """
        html = self.doc_class(
            '<dtml-unless foo>'
            'Foo not true'
            '</dtml-unless>')

        self.assertEqual(html(), 'Foo not true')
