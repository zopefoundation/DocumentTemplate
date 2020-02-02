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

from zope.deferredimport import deprecated


# BBB DocumentTemplate 4.0
deprecated(
    'Please import from zope.sequencesort.ssort. '
    'This module will go away in DocumentTemplate 4.0.',
    SortBy='zope.sequencesort.ssort:SortBy',
    SortEx='zope.sequencesort.ssort:SortEx',
    make_sortfunctions='zope.sequencesort.ssort:make_sortfunctions',
    nocase='zope.sequencesort.ssort:nocase',
    sort='zope.sequencesort.ssort:sort',
)

# only if locale is already imported
if 'locale' in sys.modules:
    # BBB DocumentTemplate 4.0
    deprecated(
        'Please import from zope.sequencesort.ssort. '
        'This module will go away in DocumentTemplate 4.0.',
        strcoll_nocase='zope.sequencesort.ssort:strcoll_nocase',
    )
del sys
