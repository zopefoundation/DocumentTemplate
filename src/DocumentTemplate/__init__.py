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

import TreeDisplay  # NOQA: F401 Registers the dtml-tree tag
from .DT_HTML import HTML  # NOQA: F401
from .DT_HTML import HTMLDefault  # NOQA: F401
from .DT_HTML import HTMLFile  # NOQA: F401
from .DT_String import File  # NOQA: F401
from .DT_String import String  # NOQA: F401


from . import security  # isort:skip  Side effects!
del security


# This encoding is used for backwards compatibility
OLD_DEFAULT_ENCODING = 'Latin-1'

# This is the new ZPublisher default and will be used on new objects
NEW_DEFAULT_ENCODING = 'UTF-8'
