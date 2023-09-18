Changelog
=========

4.5 (2023-09-18)
----------------

- Add preliminary support for Python 3.12rc1.

- Be more resilient on sorting if the getter returns ``None``.
  (`#72 <https://github.com/zopefoundation/DocumentTemplate/pull/72>`_)


4.4 (2022-01-12)
----------------

- Drop support for Python 3.6.


4.3 (2022-12-21)
----------------

- Fix `restructured-text` format specification. Tests were silently skipped.


4.2 (2022-12-16)
----------------

- Fix insidious buildout configuration bug for tests against Zope 4.

- Add support for Python 3.11.


4.1 (2022-09-20)
----------------

- Set the ``tree-s`` cookie for ``dtml-tree`` tags with ``SameSite=Lax``.
  The tree tag never set this attribute. That causes modern browsers to show
  warnings in the browser console and break tree displays in the future.
  See https://hacks.mozilla.org/2020/08/changes-to-samesite-cookie-behavior/
  for information about the ``SameSite`` cookie attribute and why its handling
  in browsers is changing.

- Add support for Python 3.10.

- Drop support for Python 3.5.


4.0 (2020-11-12)
----------------

- Make ``ustr.ustr`` Python 3 compatible
  (`Zope#921 <https://github.com/zopefoundation/Zope/issues/921>`_)

- Add support for Python 3.9

- Restore ``sql_quote`` behavior of always returning native strings
  (`#54 <https://github.com/zopefoundation/DocumentTemplate/issues/54>`_)

- Fix broken tree tag
  (`#52 <https://github.com/zopefoundation/DocumentTemplate/issues/52>`_)

- Drop support for Python 2.

- Eventually drop BBB code leading to a deprecation warning in version 3.2+.
  (`#42 <https://github.com/zopefoundation/DocumentTemplate/issues/42>`_)

- Update `isort` to version 5.


3.2.2 (2020-02-04)
------------------

- de-fang ``sql_quote`` even more as quoting is too database-specific.
  (`#48 <https://github.com/zopefoundation/DocumentTemplate/issues/48>`_)


3.2.1 (2020-02-03)
------------------

- prevent a really strange ``AccessControl`` test failure when running
  Zope's ``alltests`` script by importing deprecated names from
  ``zope.sequencesort.ssort`` instead of ``sequence/SortEx.py`` in
  ``sequence/__init__.py``


3.2 (2020-02-03)
----------------

- no longer escape double quotes in ``sql_quote`` - that breaks PostgreSQL
  (`#48 <https://github.com/zopefoundation/DocumentTemplate/issues/48>`_)

- Added `DeprecationWarnings` for all deprecated files and names
  (`#42 <https://github.com/zopefoundation/DocumentTemplate/issues/42>`_)

- Import sorting done like Zope itself

- Applied extended linting configuration similar to Zope's own


3.1 (2020-01-31)
----------------

- Escape more characters in ``sql_quote``.  Taken over from PloneHotfix20200121.


3.1b2 (2019-05-16)
------------------

- Fix broken handling of SyntaxError under Python 3


3.1b1 (2019-05-13)
------------------

- Don't call HTTPExceptions that are looked up in TemplateDicts


3.0 (2019-05-09)
----------------

Changes since 2.13.2:

Breaking changes
++++++++++++++++

- Replace C code with a pure-Python implementation.

- Remove ``VSEval`` module. Please use DT_Util.EVal now.

- Remove ``DTtestExpr`` module. It contained nothing useful.

- Remove support for string exceptions in ``<dtml-except>``.
  (`#29 <https://github.com/zopefoundation/DocumentTemplate/pull/29>`_)

Features
++++++++

- Add support for Python 3.5, 3.6, 3.7, 3.8.

- Make the rendering encoding configurable to fix rendering on Zope 4.
  (`#43 <https://github.com/zopefoundation/DocumentTemplate/issues/43>`_)

- Add `__contains__` support to DocumentTemplate.TemplateDict.

Bug fixes
+++++++++

- Only decode input in ``html_quote`` when needed under Python 3
  (`Products.PythonScripts#28 <https://github.com/zopefoundation/Products.PythonScripts/issues/28`>_)

- Make sure all JSON-serialized data is text data and not bytes.
  (`#45 <https://github.com/zopefoundation/DocumentTemplate/issues/45>`_)

- Fix regression with exception handling in ``<dtml-except>`` with Python 2.
  (`#25 <https://github.com/zopefoundation/DocumentTemplate/issues/25>`_)

- Stabilized TreeTag rendering for objects without ``_p_oid`` values.
  (`#26 <https://github.com/zopefoundation/DocumentTemplate/issues/26>`_)

- Fix bugs with ``<dtml-in>``:

    - Raise proper error if prefix is not simple.
    - Fix complex multisort in Python 3.
    - Fix iteration over list of tuples in Python 3.

- Ensure html_quote is being applied to content.


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
