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

from DocumentTemplate._DocumentTemplate import (  # NOQA
    InstanceDict,
    join_unicode,
    render_blocks,
    safe_callable,
)

import warnings
warnings.warn('pDocumentTemplate is not longer in active use. '
              'It remains only as an implementation reference.',
              DeprecationWarning)


class MultiMapping(object):

    def __init__(self):
        self.dicts = []

    def __getitem__(self, key):
        for d in self.dicts:
            try:
                return d[key]
            except (KeyError, AttributeError):
                # XXX How do we get an AttributeError?
                pass
        raise KeyError(key)

    def push(self, d):
        self.dicts.insert(0, d)

    def pop(self, n=1):
        r = self.dicts[-1]
        del self.dicts[:n]
        return r

    def keys(self):
        kz = []
        for d in self.dicts:
            kz = kz + d.keys()
        return kz


class DictInstance(object):

    def __init__(self, mapping):
        self.__d = mapping

    def __getattr__(self, name):
        try:
            return self.__d[name]
        except KeyError:
            raise AttributeError(name)


class TemplateDict(object):

    level = 0

    def _pop(self, n=1):
        return self.dicts.pop(n)

    def _push(self, d):
        return self.dicts.push(d)

    def __init__(self):
        m = self.dicts = MultiMapping()
        self._pop = m.pop
        self._push = m.push
        try:
            self.keys = m.keys
        except Exception:
            pass

    def __getitem__(self, key, call=1):
        v = self.dicts[key]
        if call:
            if hasattr(v, '__render_with_namespace__'):
                return v.__render_with_namespace__(self)
            vbase = getattr(v, 'aq_base', v)
            if safe_callable(vbase):
                if getattr(vbase, 'isDocTemp', 0):
                    v = v(None, self)
                else:
                    v = v()
        return v

    def __len__(self):
        total = 0
        for d in self.dicts.dicts:
            total = total + len(d)
        return total

    def __contains__(self, key):
        try:
            self.dicts[key]
        except KeyError:
            return False
        return True

    def has_key(self, key):
        return key in self

    getitem = __getitem__

    def __call__(self, *args, **kw):
        if args:
            if len(args) == 1 and not kw:
                m = args[0]
            else:
                m = self.__class__()
                for a in args:
                    m._push(a)
                if kw:
                    m._push(kw)
        else:
            m = kw
        return (DictInstance(m),)
