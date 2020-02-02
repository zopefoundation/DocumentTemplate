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

import warnings

# BBB imports for former C implementation.
# BBB DocumentTemplate 4.0
from ._DocumentTemplate import DictInstance
from ._DocumentTemplate import InstanceDict
from ._DocumentTemplate import TemplateDict
from ._DocumentTemplate import join_unicode
from ._DocumentTemplate import render_blocks
from ._DocumentTemplate import safe_callable


warnings.warn('The cDocumentTemplate module is deprecated and will be '
              'removed in DocumentTemplate 4. Use _DocumentTemplate instead.',
              DeprecationWarning)
