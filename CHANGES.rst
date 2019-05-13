Changelog
=========

3.1b1 (2019-05-13)
------------------

Bug fixes
+++++++++

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
