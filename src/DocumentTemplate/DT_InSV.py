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
"""Sequence variables support"""

import re
from math import sqrt

import roman


try:
    import Missing
    mv = Missing.Value
except ImportError:
    mv = None

TupleType = tuple


class sequence_variables:

    alt_prefix = None

    def __init__(self, items=None, query_string='', start_name_re=None,
                 alt_prefix=''):
        if items is not None:
            # Turn iterable into a list, to support key lookup
            items = list(items)
        self.items = items
        self.query_string = query_string
        self.start_name_re = start_name_re
        if alt_prefix:
            self.alt_prefix = alt_prefix + '_'

        self.data = {
            'previous-sequence': 0,
            'next-sequence': 0,
            'sequence-start': 1,
            'sequence-end': 0,
        }

    def __len__(self):
        return 1

    def number(self, index):
        return index + 1

    def even(self, index):
        return index % 2 == 0

    def odd(self, index):
        return index % 2

    def letter(self, index):
        return chr(ord('a') + index)

    def Letter(self, index):
        return chr(ord('A') + index)

    def key(self, index):
        return self.items[index][0]

    def item(self, index, tt=type(())):
        i = self.items[index]
        if type(i) is tt and len(i) == 2:
            return i[1]
        return i

    def roman(self, index):
        return self.Roman(index).lower()

    def Roman(self, num):
        # Force number to be an integer value
        num = int(num) + 1

        return roman.toRoman(num)

    def value(self, index, name):
        data = self.data
        item = self.items[index]
        if type(item) == TupleType and len(item) == 2:
            item = item[1]
        if data['mapping']:
            return item[name]
        return getattr(item, name)

    def first(self, name, key=''):
        data = self.data
        if data['sequence-start']:
            return 1
        index = data['sequence-index']
        return self.value(index, name) != self.value(index - 1, name)

    def last(self, name, key=''):
        data = self.data
        if data['sequence-end']:
            return 1
        index = data['sequence-index']
        return self.value(index, name) != self.value(index + 1, name)

    def length(self, ignored):
        l_ = self['sequence-length'] = len(self.items)
        return l_

    def query(self, *ignored):

        if self.start_name_re is None:
            raise KeyError('sequence-query')
        query_string = self.query_string
        while query_string and query_string[:1] in '?&':
            query_string = query_string[1:]
        while query_string[-1:] == '&':
            query_string = query_string[:-1]
        if query_string:
            query_string = '&%s&' % query_string
            reg = self.start_name_re
            if isinstance(reg, type(re.compile(r""))):
                mo = reg.search(query_string)
                if mo is not None:
                    v = mo.group(0)
                    l_ = mo.start(0)
                    query_string = (query_string[:l_] +  # NOQA: W504
                                    query_string[l_ + len(v) - 1:])

            else:
                l_ = reg.search_group(query_string, (0,))
                if l_:
                    v = l_[1]
                    l_ = l_[0]
                    query_string = (query_string[:l_] +  # NOQA: W504
                                    query_string[l_ + len(v) - 1:])

            query_string = '?' + query_string[1:]
        else:
            query_string = '?'
        self['sequence-query'] = query_string

        return query_string

    statistic_names = (
        'total', 'count', 'min', 'max', 'median', 'mean', 'variance',
        'variance-n', 'standard-deviation', 'standard-deviation-n',
    )

    def statistics(self, name, key):
        items = self.items
        data = self.data
        mapping = data['mapping']
        count = sum = sumsq = 0
        min = max = None
        smin = smax = None
        values = []
        svalues = []
        for item in items:
            try:
                if mapping:
                    item = item[name]
                else:
                    try:
                        item = getattr(item, name)
                    except Exception:
                        if name != 'item':
                            raise
                try:
                    if item is mv:
                        item = None
                    if isinstance(item, int):
                        s = item * int(item)
                    else:
                        s = item * item
                    sum = sum + item
                    sumsq = sumsq + s
                    values.append(item)
                    if min is None:
                        min = max = item
                    else:
                        if item < min:
                            min = item
                        if item > max:
                            max = item
                except TypeError:
                    if item is not None and item is not mv:
                        if smin is None:
                            smin = smax = item
                        else:
                            if item < smin:
                                smin = item
                            if item > smax:
                                smax = item
                        svalues.append(item)
            except Exception:
                pass

        # Initialize all stats to empty strings:
        for stat in self.statistic_names:
            data[f'{stat}-{name}'] = ''

        count = len(values)
        try:  # Numeric statistics
            n = float(count)
            mean = sum / n
            sumsq = sumsq / n - mean * mean
            data['mean-%s' % name] = mean
            data['total-%s' % name] = sum
            data['variance-n-%s' % name] = sumsq
            data['standard-deviation-n-%s' % name] = sqrt(sumsq)
            if count > 1:
                sumsq = sumsq * n / (n - 1)
                data['variance-%s' % name] = sumsq
                data['standard-deviation-%s' % name] = sqrt(sumsq)
            else:
                data['variance-%s' % name] = ''
                data['standard-deviation-%s' % name] = ''
        except ZeroDivisionError:
            if min is None:
                min, max, values = smin, smax, svalues
            else:
                if smin < min:
                    min = smin
                if smax > max:
                    max = smax
                values = values + svalues
            count = len(values)

        data['count-%s' % name] = count
        if min is not None:
            data['min-%s' % name] = min
            data['max-%s' % name] = max
            values.sort()
            if count == 1:
                data['median-%s' % name] = min
            else:
                if count % 2 != 0:
                    data['median-%s' % name] = values[count // 2]
                else:
                    half = count // 2
                    try:
                        data['median-%s' % name] = (
                            values[half] + values[half - 1]) // 2
                    except Exception:
                        try:
                            data['median-%s' % name] = (
                                "between {} and {}".format(values[half],
                                                           values[half - 1]))
                        except Exception:
                            pass

        return data[key]

    def next_batches(self, suffix='batches', key=''):
        if suffix != 'batches':
            raise KeyError(key)
        data = self.data
        sequence = self.items
        try:
            if not data['next-sequence']:
                return ()
            sz = data['sequence-step-size']
            start = data['sequence-step-start']
            end = data['sequence-step-end']
            l_ = len(sequence)
            orphan = data['sequence-step-orphan']
            overlap = data['sequence-step-overlap']
        except Exception:
            pass
        r = []
        while end < l_:
            start, end, spam = opt(end + 1 - overlap, 0,
                                   sz, orphan, sequence)
            v = sequence_variables(self.items,
                                   self.query_string, self.start_name_re)
            d = v.data
            d['batch-start-index'] = start - 1
            d['batch-end-index'] = end - 1
            d['batch-size'] = end + 1 - start
            d['mapping'] = data['mapping']
            r.append(v)
        data['next-batches'] = r
        return r

    def previous_batches(self, suffix='batches', key=''):
        if suffix != 'batches':
            raise KeyError(key)
        data = self.data
        sequence = self.items
        try:
            if not data['previous-sequence']:
                return ()
            sz = data['sequence-step-size']
            start = data['sequence-step-start']
            end = data['sequence-step-end']
            orphan = data['sequence-step-orphan']
            overlap = data['sequence-step-overlap']
        except Exception:
            pass
        r = []
        while start > 1:
            start, end, spam = opt(0, start - 1 + overlap,
                                   sz, orphan, sequence)
            v = sequence_variables(self.items,
                                   self.query_string, self.start_name_re)
            d = v.data
            d['batch-start-index'] = start - 1
            d['batch-end-index'] = end - 1
            d['batch-size'] = end + 1 - start
            d['mapping'] = data['mapping']
            r.append(v)
        r.reverse()
        data['previous-batches'] = r
        return r

    special_prefixes = {
        'first': first,
        'last': last,
        'previous': previous_batches,
        'next': next_batches,
        # These two are for backward compatability with a missfeature:
        'sequence-index': \
        lambda self, suffix, key: self['sequence-' + suffix],
        'sequence-index-is': \
        lambda self, suffix, key: self['sequence-' + suffix],
    }
    for n in statistic_names:
        special_prefixes[n] = statistics

    def __setitem__(self, key, value):
        self.data[key] = value
        if self.alt_prefix:
            if key.startswith('sequence-'):
                key = key[9:]
            self.data[self.alt_prefix + key] = value

    def __getitem__(self, key,
                    special_prefixes=special_prefixes,
                    special_prefix=special_prefixes.__contains__
                    ):
        data = self.data
        if key in data:
            return data[key]

        l_ = key.rfind('-')
        if l_ < 0:
            alt_prefix = self.alt_prefix
            if not (alt_prefix and key.startswith(alt_prefix)):
                raise KeyError(key)

            suffix = key[len(alt_prefix):].replace('_', '-')
            if '-' in suffix:
                try:
                    return self[suffix]
                except KeyError:
                    pass
            prefix = 'sequence'
            key = 'sequence-' + suffix
        else:
            suffix = key[l_ + 1:]
            prefix = key[:l_]

        if hasattr(self, suffix):
            try:
                v = data[prefix + '-index']
            except Exception:
                pass
            else:
                return getattr(self, suffix)(v)

        if special_prefix(prefix):
            return special_prefixes[prefix](self, suffix, key)

        if prefix[-4:] == '-var':
            prefix = prefix[:-4]
            try:
                return self.value(data[prefix + '-index'], suffix)
            except Exception:
                pass

        if key == 'sequence-query':
            return self.query()

        raise KeyError(key)


def opt(start, end, size, orphan, sequence):
    if size < 1:
        if start > 0 and end > 0 and end >= start:
            size = end + 1 - start
        else:
            size = 7

    if start > 0:
        try:
            sequence[start - 1]
        except Exception:
            start = len(sequence)

        if end > 0:
            if end < start:
                end = start
        else:
            end = start + size - 1
            try:
                sequence[end + orphan - 1]
            except Exception:
                end = len(sequence)

    elif end > 0:
        try:
            sequence[end - 1]
        except Exception:
            end = len(sequence)
        # if end > l: end=l
        start = end + 1 - size
        if start - 1 < orphan:
            start = 1
    else:
        start = 1
        end = start + size - 1
        try:
            sequence[end + orphan - 1]
        except Exception:
            end = len(sequence)
    return (start, end, size)
