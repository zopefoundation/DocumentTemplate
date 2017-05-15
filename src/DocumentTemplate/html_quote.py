# split off into its own module for aliasing without circrefs

from DocumentTemplate.ustr import ustr

try:
    from html import escape
except ImportError:  # PY2
    from cgi import escape


def html_quote(v, name='(Unknown name)', md={}):
    return escape(ustr(v), 1)
