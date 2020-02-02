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
"""This module is no longer actively used.
"""

from zope.deferredimport import deprecated


# BBB DocumentTemplate 4.0
deprecated(
    'Please import from DocumentTemplate._DocumentTemplate. '
    'This module will go away in DocumentTemplate 4.0.',
    DictInstance='DocumentTemplate._DocumentTemplate:DictInstance',
    InstanceDict='DocumentTemplate._DocumentTemplate:InstanceDict',
    TemplateDict='DocumentTemplate._DocumentTemplate:TemplateDict',
    join_unicode='DocumentTemplate._DocumentTemplate:join_unicode',
    render_blocks='DocumentTemplate._DocumentTemplate:render_blocks',
    safe_callable='DocumentTemplate._DocumentTemplate:safe_callable',
)
