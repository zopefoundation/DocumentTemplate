# split off into its own module for aliasing without circrefs
from .ustr import ustr


try:
    from html import escape
except ImportError:  # PY2
    from cgi import escape


def html_quote(v, name='(Unknown name)', md={}, encoding=None):
    v = ustr(v)
    if isinstance(v, bytes):
        # decode using the old default if no encoding is passed
        v = v.decode(encoding or 'Latin-1')
    return escape(v, 1)
