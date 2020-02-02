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

import warnings

from ._DocumentTemplate import DictInstance
from ._DocumentTemplate import InstanceDict
from ._DocumentTemplate import TemplateDict
from ._DocumentTemplate import join_unicode
from ._DocumentTemplate import render_blocks
from ._DocumentTemplate import safe_callable


warnings.warn('pDocumentTemplate is not longer in active use. '
              'It remains only as an implementation reference.',
              DeprecationWarning)  # pragma: nocover
