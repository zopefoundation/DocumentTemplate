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

# BBB imports for former C implementation.
from DocumentTemplate._DocumentTemplate import (  # NOQA
    DictInstance,
    InstanceDict,
    join_unicode,
    render_blocks,
    safe_callable,
    TemplateDict,
)

import warnings
warnings.warn('cDocumentTemplate is deprecated, use '
              '_DocumentTemplate instead.', DeprecationWarning)
