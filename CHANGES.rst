Changelog
=========

3.0a1 (2017-01-19)
------------------

- Ensure html_quote is being applied to content.

- Replace C code with a pure-Python implementation.

- Add `__contains__` support to DocumentTemplate.TemplateDict.

- Modernised C code in preparation of porting to Python 3.

2.13.2 (2011-12-12)
-------------------

- Restrict the available functions in `DocumentTemplate.sequence` to public
  API's of `zope.sequencesort`.

2.13.1 (2010-07-15)
-------------------

- LP #143273: Enable the dtml-var modifiers url_quote, url_unquote,
  url_quote_plus and url_unquote_plus to handle unicode strings.


2.13.0 (2010-06-19)
-------------------

- Released as separate package.
