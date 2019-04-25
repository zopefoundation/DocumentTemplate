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
"""Rendering object hierarchies as Trees
"""

from binascii import a2b_base64
from binascii import b2a_base64
import json
import zlib

import six

from DocumentTemplate.DT_Util import add_with_prefix
from DocumentTemplate.DT_Util import Eval
from DocumentTemplate.DT_Util import InstanceDict
from DocumentTemplate.DT_Util import name_param
from DocumentTemplate.DT_Util import parse_params
from DocumentTemplate.DT_Util import ParseError
from DocumentTemplate.DT_Util import render_blocks
from DocumentTemplate.DT_Util import simple_name
from DocumentTemplate.DT_Util import ValidationError
from DocumentTemplate.DT_String import String

if six.PY3:
    unicode = str
    tbl = b''.join([chr(i).encode('latin-1') for i in range(256)])
else:
    tbl = b''.join([chr(i) for i in range(256)])

tplus = tbl[:ord('+')] + b'-' + tbl[ord('+') + 1:]
tminus = tbl[:ord('-')] + b'+' + tbl[ord('-') + 1:]


class Tree(object):
    name = 'tree'
    blockContinuations = ()
    expand = None

    def __init__(self, blocks, encoding=None):
        self.encoding = encoding
        tname, args, section = blocks[0]
        args = parse_params(args,
                            name=None,
                            expr=None,
                            nowrap=1,
                            expand=None,
                            leaves=None,
                            header=None,
                            footer=None,
                            branches=None,
                            branches_expr=None,
                            sort=None,
                            reverse=1,
                            skip_unauthorized=1,
                            id=None,
                            single=1,
                            url=None,
                            # opened_decoration=None,
                            # closed_decoration=None,
                            # childless_decoration=None,
                            assume_children=1,
                            urlparam=None, prefix=None)
        if '' in args or 'name' in args or 'expr' in args:
            name, expr = name_param(args, 'tree', 1)

            if expr is not None:
                args['expr'] = expr
            elif '' in args:
                args['name'] = name
        else:
            name = 'a tree tag'

        if 'branches_expr' in args:
            if 'branches' in args:
                raise ParseError(
                    'branches and  and branches_expr given', 'tree')
            args['branches_expr'] = Eval(args['branches_expr']).eval
        elif 'branches' not in args:
            args['branches'] = 'tpValues'

        if 'id' not in args:
            args['id'] = 'tpId'
        if 'url' not in args:
            args['url'] = 'tpURL'
        if 'childless_decoration' not in args:
            args['childless_decoration'] = ''

        prefix = args.get('prefix')
        if prefix and not simple_name(prefix):
            raise ParseError(
                'prefix is not a simple name', 'tree')

        self.__name__ = name
        self.section = section.blocks
        self.args = args

    def render(self, md):
        args = self.args

        if 'name' in args:
            v = md[args['name']]
        elif 'expr' in args:
            v = args['expr'].eval(md)
        else:
            v = md.this
        return tpRender(v, md, self.section, self.args)

    __call__ = render


String.commands['tree'] = Tree

pyid = id  # Copy builtin

simple_types = {str: 1, unicode: 1, int: 1, float: 1,
                tuple: 1, list: 1, dict: 1}


def try_call_attr(ob, attrname, simple_types=simple_types):
    attr = getattr(ob, attrname)
    if type(attr) in simple_types:
        return attr
    try:
        return attr()
    except TypeError:
        return attr


def tpRender(self, md, section, args,
             try_call_attr=try_call_attr, encoding=None):
    """Render data organized as a tree.

    We keep track of open nodes using a cookie.  The cookie stored the
    tree state. State should be a tree represented like:

      []  # all closed
      ['eagle'], # eagle is open
      ['eagle'], ['jeep', [1983, 1985]]  # eagle, jeep, 1983 jeep and 1985 jeep

    where the items are object ids. The state will be pickled to a
    compressed and base64ed string that gets unencoded, uncompressed,
    and unpickled on the other side.

    Note that ids used in state need not be connected to urls, since
    state manipulation is internal to rendering logic.

    Note that to make unpickling safe, we use the MiniPickle module,
    that only creates safe objects
    """

    data = []

    id = extract_id(self, args['id'])

    try:
        # see if we are being run as a sub-document
        root = md['tree-root-url']
        url = md['tree-item-url']
        state = md['tree-state']
        diff = md['tree-diff']
        substate = md['-tree-substate-']
        colspan = md['tree-colspan']
        level = md['tree-level']

    except KeyError:
        # OK, we are a top-level invocation
        level = -1

        if 'collapse_all' in md:
            state = [id, []],
        elif 'expand_all' in md:
            if 'branches' in args:
                def get_items(node, branches=args['branches'], md=md):
                    get = md.guarded_getattr
                    if get is None:
                        get = getattr
                    items = get(node, branches)
                    return items()
            elif 'branches_expr' in args:
                def get_items(node, branches_expr=args['branches_expr'],
                              md=md):
                    md._push(InstanceDict(node, md))
                    items = branches_expr(md)
                    md._pop()
                    return items
            state = [id, tpValuesIds(self, get_items, args)],
        else:
            if 'tree-s' in md:
                state = md['tree-s']
                state = decode_seq(state)
                try:
                    if state[0][0] != id:
                        state = [id, []],
                except IndexError:
                    state = [id, []],
            else:
                state = [id, []],

            if 'tree-e' in md:
                diff = decode_seq(md['tree-e'])
                apply_diff(state, diff, 1)

            if 'tree-c' in md:
                diff = decode_seq(md['tree-c'])
                apply_diff(state, diff, 0)

        colspan = tpStateLevel(state)
        substate = state
        diff = []

        url = ''
        root = md['URL']
        right_end = root.rfind('/')
        if right_end >= 0:
            root = root[right_end + 1:]

    treeData = {'tree-root-url': root,
                'tree-colspan': colspan,
                'tree-state': state}

    prefix = args.get('prefix')
    if prefix:
        for k, v in treeData.items():
            treeData[prefix + k[4:].replace('-', '_')] = v

    md._push(InstanceDict(self, md))
    md._push(treeData)

    try:
        tpRenderTABLE(
            self, id, root, url, state, substate, diff, data, colspan,
            section, md, treeData, level, args, encoding=encoding)
    finally:
        md._pop(2)

    if state is substate and not ('single' in args and args['single']):
        state = state or ([id],)
        state = encode_seq(state)
        md['RESPONSE'].setCookie('tree-s', state)

    return ''.join(data)


def tpRenderTABLE(self, id, root_url, url, state, substate, diff, data,
                  colspan, section, md, treeData, level=0, args=None,
                  try_call_attr=try_call_attr, encoding=None,
                  ):
    "Render a tree as a table"
    exp = 0

    if level >= 0:
        urlattr = args['url']
        if urlattr and hasattr(self, urlattr):
            tpUrl = try_call_attr(self, urlattr)
            url = (url and ('%s/%s' % (url, tpUrl))) or tpUrl
            root_url = root_url or tpUrl

    ptreeData = add_with_prefix(treeData, 'tree', args.get('prefix'))
    ptreeData['tree-item-url'] = url
    ptreeData['tree-level'] = level
    ptreeData['tree-item-expanded'] = 0

    output = data.append

    items = None
    if ('assume_children' in args and args['assume_children'] and
            substate is not state):
        # We should not compute children unless we have to.
        # See if we've been asked to expand our children.
        for i in range(len(substate)):
            sub = substate[i]
            if sub[0] == id:
                exp = i + 1
                break
        if not exp:
            items = 1

    get = md.guarded_getattr
    if get is None:
        get = getattr

    if items is None:
        if 'branches' in args and hasattr(self, args['branches']):
            items = get(self, args['branches'])
            items = items()
        elif 'branches_expr' in args:
            items = args['branches_expr'](md)

        if not items and 'leaves' in args:
            items = 1

    if items and items != 1:

        getitem = getattr(md, 'guarded_getitem', None)
        if getitem is not None:
            unauth = []
            for index in range(len(items)):
                try:
                    getitem(items, index)
                except ValidationError:
                    unauth.append(index)
            if unauth:
                if 'skip_unauthorized' in args and args['skip_unauthorized']:
                    items = list(items)
                    unauth.reverse()
                    for index in unauth:
                        del items[index]
                else:
                    raise ValidationError(unauth)

        if 'sort' in args:
            # Faster/less mem in-place sort
            if isinstance(items, tuple):
                items = list(items)
            sort = args['sort']
            size = range(len(items))
            for i in size:
                v = items[i]
                k = getattr(v, sort)
                try:
                    k = k()
                except Exception:
                    pass
                items[i] = (k, v)
            items.sort()
            for i in size:
                items[i] = items[i][1]

        if 'reverse' in args:
            items = list(items)  # Copy the list
            items.reverse()

    diff.append(id)

    _td_colspan = '<td colspan="%s" style="white-space: nowrap"></td>'
    _td_single = '<td width="16" style="white-space: nowrap"></td>'

    sub = None
    if substate is state:
        output('<table cellspacing="0">\n')
        sub = substate[0]
        exp = items
    else:
        # Add prefix
        output('<tr>\n')

        # Add +/- icon
        if items:
            if level:
                if level > 3:
                    output(_td_colspan % (level - 1))
                elif level > 1:
                    output(_td_single * (level - 1))
                output(_td_single)
                output('\n')
            output('<td width="16" valign="top" style="white-space: nowrap">')
            for i in range(len(substate)):
                sub = substate[i]
                if sub[0] == id:
                    exp = i + 1
                    break

            s = encode_str(compress(json.dumps(diff)))  # bytes in ASCII enc.

            # For rendering the encoded state string in a URL under Python 3,
            # we must lose the "b" prefix by decoding
            if six.PY3:
                s = s.decode('ASCII')

            # Propagate extra args through tree.
            if 'urlparam' in args:
                param = args['urlparam']
                param = "%s&" % param
            else:
                param = ""

            if exp:
                ptreeData['tree-item-expanded'] = 1
                icon = ('<i title="Collapse..."'
                        ' class="fas fa-caret-down text-muted"></i>')
                output('<a name="%s" href="%s?%stree-c=%s#%s">%s</a>' %
                       (id, root_url, param, s, id, icon))
            else:
                icon = ('<i title="Expand..."'
                        ' class="fas fa-caret-right text-muted"></i>')
                output('<a name="%s" href="%s?%stree-e=%s#%s">%s</a>' %
                       (id, root_url, param, s, id, icon))
            output('</td>\n')

        else:
            if level > 2:
                output(_td_colspan % level)
            elif level > 0:
                output(_td_single * level)
            output(_td_single)
            output('\n')

        # add item text
        dataspan = colspan - level
        output('<td%s%s valign="top" align="left">' %
               ((dataspan > 1 and (' colspan="%s"' % dataspan) or ''),
                ('nowrap' in args and
                 args['nowrap'] and ' style="white-space: nowrap"' or ''))
               )
        output(render_blocks(section, md, encoding=encoding))
        output('</td>\n</tr>\n')

    if exp:
        level = level + 1
        dataspan = colspan - level
        if level > 2:
            h = _td_colspan % level
        elif level > 0:
            h = _td_single * level
        else:
            h = ''

        if 'header' in args:
            doc = args['header']
            if doc in md:
                doc = md.getitem(doc, 0)
            else:
                doc = None
            if doc is not None:
                output(doc(
                    None, md,
                    standard_html_header=(
                        '<tr>%s'
                        '<td width="16" style="white-space: nowrap"></td>'
                        '<td%s valign="top">'
                        % (h,
                           (dataspan > 1 and (' colspan="%s"' % dataspan) or
                            ''))),
                    standard_html_footer='</td></tr>',
                ))

        if items == 1:
            # leaves
            if 'leaves' in args:
                doc = args['leaves']
                if doc in md:
                    doc = md.getitem(doc, 0)
                else:
                    doc = None
                if doc is not None:
                    treeData['-tree-substate-'] = sub
                    ptreeData['tree-level'] = level
                    md._push(treeData)
                    try:
                        output(doc(
                            None, md,
                            standard_html_header=(
                                '<tr>%s<td '
                                'width="16" style="white-space: nowrap"></td>'
                                '<td%s valign="top">'
                                % (h,
                                   (dataspan > 1 and
                                    (' colspan="%s"' % dataspan) or ''))),
                            standard_html_footer='</td></tr>',
                        ))
                    finally:
                        md._pop(1)
        elif 'expand' in args:
            doc = args['expand']
            if doc in md:
                doc = md.getitem(doc, 0)
            else:
                doc = None
            if doc is not None:
                treeData['-tree-substate-'] = sub
                ptreeData['tree-level'] = level
                md._push(treeData)
                try:
                    output(doc(
                        None, md,
                        standard_html_header=(
                            '<tr>%s<td '
                            'width="16" style="white-space: nowrap"></td>'
                            '<td%s valign="top">'
                            % (h,
                               (dataspan > 1 and
                                (' colspan="%s"' % dataspan) or ''))),
                        standard_html_footer='</td></tr>',
                    ))
                finally:
                    md._pop(1)
        else:
            __traceback_info__ = sub, args, state, substate
            ids = {}
            for item in items:
                id = extract_id(item, args['id'])
                if len(sub) == 1:
                    sub.append([])
                substate = sub[1]
                ids[id] = 1
                md._push(InstanceDict(item, md))
                try:
                    data = tpRenderTABLE(
                        item, id, root_url, url, state, substate, diff, data,
                        colspan, section, md, treeData, level, args)
                finally:
                    md._pop()
                if not sub[1]:
                    del sub[1]

            ids = ids.__contains__
            for i in range(len(substate) - 1, -1):
                if not ids(substate[i][0]):
                    del substate[i]

        if 'footer' in args:
            doc = args['footer']
            if doc in md:
                doc = md.getitem(doc, 0)
            else:
                doc = None
            if doc is not None:
                output(doc(
                    None, md,
                    standard_html_header=(
                        '<tr>%s<td '
                        'width="16" style="white-space: nowrap"></td>'
                        '<td%s valign="top">'
                        % (h,
                           (dataspan > 1 and (' colspan="%s"' % dataspan) or
                            ''))),
                    standard_html_footer='</td></tr>',
                ))

    del diff[-1]
    if not diff:
        output('</table>\n')

    return data


def apply_diff(state, diff, expand):
    if not diff:
        return
    s = [None, state]
    diff.reverse()
    __traceback_info__ = s, diff
    while diff:
        id = diff[-1]
        del diff[-1]
        if len(s) == 1:
            s.append([])
        s = s[1]
        if isinstance(s, tuple):
            s = list(s)
        loc = -1
        for i in range(len(s)):
            if s[i][0] == id:
                loc = i
                break

        if loc >= 0:
            if not diff and not expand:
                del s[loc]
            else:
                s = s[loc]
        elif diff or expand:
            s.append([id, []])
            s = s[-1][1]
            while diff:
                id = diff[-1]
                del diff[-1]
                if diff or expand:
                    s.append([id, []])
                    s = s[-1][1]


def encode_seq(state):
    "Convert a sequence to an encoded string"
    state = compress(json.dumps(state))
    l_ = len(state)

    if l_ > 57:
        states = []
        for i in range(0, l_, 57):
            states.append(b2a_base64(state[i:i + 57])[:-1])
        state = b''.join(states)
    else:
        state = b2a_base64(state)[:-1]

    l_ = state.find(b'=')
    if l_ >= 0:
        state = state[:l_]

    state = state.translate(tplus)
    if six.PY3:
        state = state.decode('ascii')
    return state


def encode_str(state):
    """Convert bytes to a base64-encoded bytes.

    'state' should be bytes
    """
    if not isinstance(state, bytes):
        raise ValueError("state should be bytes")

    l_ = len(state)

    if l_ > 57:
        states = []
        for i in range(0, l_, 57):
            states.append(b2a_base64(state[i:i + 57])[:-1])
        state = b''.join(states)
    else:
        state = b2a_base64(state)[:-1]

    # state is still bytes, but all in 'ascii' encoding.
    l_ = state.find(b'=')
    if l_ >= 0:
        state = state[:l_]

    state = state.translate(tplus)
    return state


def decode_seq(state):
    "Convert an encoded string to a sequence"
    if not isinstance(state, bytes):
        state = state.encode('ascii')

    state = state.translate(tminus)
    l_ = len(state)

    if l_ > 76:
        states = []
        j = 0
        for i in range(l_ // 76):
            k = j + 76
            states.append(a2b_base64(state[j:k]))
            j = k

        if j < l_:
            state = state[j:]
            l_ = len(state)
            k = l_ % 4
            if k:
                state = state + b'=' * (4 - k)
            states.append(a2b_base64(state))
        state = b''.join(states)
    else:
        l_ = len(state)
        k = l_ % 4
        if k:
            state = state + b'=' * (4 - k)
        state = a2b_base64(state)

    state = decompress(state)
    try:
        return json.loads(state)
    except Exception:
        return []


def compress(input):
    """Compress text to bytes.

    'input' should be text.
    """
    if not isinstance(input, six.string_types):
        raise ValueError("Input should be text")
    if not isinstance(input, bytes):
        input = input.encode('utf-8')
    return zlib.compress(input)


def decompress(input):
    """Decompress bytes to text.

    'input' should be bytes.
    """
    if not isinstance(input, bytes):
        raise ValueError("Input should be bytes")
    return zlib.decompress(input).decode('utf-8')


def tpStateLevel(state, level=0):
    for sub in state:
        if len(sub) == 2:
            level = max(level, 1 + tpStateLevel(sub[1]))
        else:
            level = max(level, 1)
    return level


def tpValuesIds(self, get_items, args,
                try_call_attr=try_call_attr,
                ):
    # get_item(node) is a function that returns the subitems of node

    # This should build the ids of subitems which are
    # expandable (non-empty). Leaves should never be
    # in the state - it will screw the colspan counting.
    r = []
    try:
        try:
            items = get_items(self)
        except AttributeError:
            items = ()
        for item in items:
            try:
                if get_items(item):
                    id = extract_id(item, args['id'])

                    e = tpValuesIds(item, get_items, args)
                    if e:
                        id = [id, e]
                    else:
                        id = [id]
                    r.append(id)
            except Exception:
                pass
    except Exception:
        pass
    return r


def extract_id(item, idattr):
    if hasattr(item, idattr):
        return try_call_attr(item, idattr)
    elif getattr(item, '_p_oid', None):
        value = b2a_base64(item._p_oid)[:-1]
        if six.PY3:
            value = value.decode('ascii')
        return value
    else:
        return pyid(item)
