import unittest


class InstanceDictTests(unittest.TestCase):
    """Testing .._DocumentTemplate.InstanceDict."""

    def test_getitem(self):
        # The acquisition chain of the object a got method is bound to
        # does not contain the InstanceDict instance itself.

        # This is a test for the fix of the regression described in
        # https://github.com/zopefoundation/Zope/issues/292

        from DocumentTemplate.DT_Util import InstanceDict
        import Acquisition

        class Item(Acquisition.Implicit):
            """Class modelling the here necessary parts of OFS.SimpleItem."""

            def __init__(self, id):
                self.id = id

            def __repr__(self):
                return '<Item id={0.id!r}>'.format(self)

            def method1(self):
                pass

        inst = Item('a').__of__(Item('b'))
        i_dict = InstanceDict(inst, {}, getattr)

        for element in Acquisition.aq_chain(i_dict['method1'].__self__):
            self.assertNotIsInstance(element, InstanceDict)
