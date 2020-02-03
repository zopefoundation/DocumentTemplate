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

import sys

from zope.sequencesort.ssort import SortBy
from zope.sequencesort.ssort import SortEx
from zope.sequencesort.ssort import make_sortfunctions
from zope.sequencesort.ssort import nocase
from zope.sequencesort.ssort import sort


# only if locale is already imported
if 'locale' in sys.modules:
    from zope.sequencesort.ssort import strcoll_nocase
del sys


__allow_access_to_unprotected_subobjects__ = 1
