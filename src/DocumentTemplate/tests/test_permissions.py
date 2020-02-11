import unittest

from ..permissions import change_dtml_documents
from ..permissions import change_dtml_methods


class PermissionsTest(unittest.TestCase):
    """Stupid test to make sure the module can be imported.

    It is actually imported by Zope in OFS.DTMLDocument.
    """

    def test_permissions(self):
        self.assertEqual(change_dtml_documents, 'Change DTML Documents')
        self.assertEqual(change_dtml_methods, 'Change DTML Methods')
