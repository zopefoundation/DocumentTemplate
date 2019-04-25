# split off into its own module for aliasing without circrefs
import six

from DocumentTemplate.ustr import ustr

try:
    from html import escape
except ImportError:  # PY2
    from cgi import escape


def html_quote(v, name='(Unknown name)', md={}, encoding=None):
    if encoding is None:
        encoding = 'Latin-1'  # the old default
    v = ustr(v)
    if isinstance(v, six.binary_type):
        v = v.decode(encoding)
    return escape(v, 1)
