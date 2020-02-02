##############################################################################
#
# Copyright (c) 2002 Zope Foundation and Contributors.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
"""Package wrapper for Document Template

This wrapper allows the (now many) document template modules to be
segregated in a separate package."""

from .DT_HTML import HTML
from .DT_HTML import HTMLDefault
from .DT_HTML import HTMLFile
from .DT_String import File
from .DT_String import String

# Register the dtml-tree tag
import TreeDisplay

from DocumentTemplate import security  # Side effects!
del security


# This encoding is used for backwards compatibility
OLD_DEFAULT_ENCODING = 'Latin-1'

# This is the new ZPublisher default and will be used on new objects
NEW_DEFAULT_ENCODING = 'UTF-8'
