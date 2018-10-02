Changelog
=========

3.0b5 (unreleased)
------------------

- Fix regression with exception handling in ``<dtml-except>`` with Python 2.
- Stabilized TreeTag rendering for objects without ``_p_oid`` values.

- Added support for Python 3.7.

- Remove support for string exceptions in ``<dtml-except>``.


3.0b4 (2018-07-12)
------------------

- Drop Python 3.4 support.

- Fix a regression in the Python implementation differing from the C
  implementation in ``DocumentTemplate.DT_Util.InstanceDict``.
  `#24 <https://github.com/zopefoundation/DocumentTemplate/pull/24>`_

- Improve compatibility with flake8.

- Update deprecated assert method calls.


3.0b3 (2018-04-18)
------------------

- Fixed a problem with Python 3 compatibility when computing the
  state strings in tree tags.

- No longer use icons which got deleted in Zope 4.

- Fix sorting in <dtml-in> for duplicate entries in Python 3.


3.0b2 (2017-11-03)
------------------

- Under Python 3, make sure no binary representations end up in the
  state string used for the tree tag.


3.0b1 (2017-09-15)
------------------

- No changes since 3.0a4.

3.0a4 (2017-06-06)
------------------

- Further fixes for Python 3 compatibility.

3.0a3 (2017-05-17)
------------------

- Further fixes for Python 3 compatibility.

3.0a2 (2017-05-05)
------------------

- Add support for Python 3.4 up to 3.6.

3.0a1 (2017-01-19)
------------------

- Ensure html_quote is being applied to content.

- Replace C code with a pure-Python implementation.

- Add `__contains__` support to DocumentTemplate.TemplateDict.

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
