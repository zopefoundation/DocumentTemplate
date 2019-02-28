import unittest
import Acquisition


class Item(Acquisition.Implicit):
    """Class modelling the here necessary parts of OFS.SimpleItem."""

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return '<Item id={0.id!r}>'.format(self)

    def method1(self):
        pass


class InstanceDictTests(unittest.TestCase):
    """Testing .._DocumentTemplate.InstanceDict."""

    def test_getitem(self):
        # The acquisition chain of the object a got method is bound to
        # does not contain the InstanceDict instance itself.

        # This is a test for the fix of the regression described in
        # https://github.com/zopefoundation/Zope/issues/292

        from DocumentTemplate.DT_Util import InstanceDict

        inst = Item('a').__of__(Item('b'))
        i_dict = InstanceDict(inst, {}, getattr)

        for element in Acquisition.aq_chain(i_dict['method1'].__self__):
            self.assertNotIsInstance(element, InstanceDict)

    def test_getitem_2(self):
        # It does not break the acquisition chain of stored objects.

        from DocumentTemplate.DT_Util import InstanceDict

        main = Item('main')
        main.sub = Item('sub')
        side = Item('side')
        side.here = Item('here')

        path = side.here.__of__(main)
        i_dict = InstanceDict(path, {}, getattr)
        self.assertEqual(main.sub, i_dict['sub'])
