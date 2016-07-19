##############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from os.path import join
from setuptools import setup, find_packages, Extension

setup(name='DocumentTemplate',
      version='3.0.dev0',
      url='http://pypi.python.org/pypi/DocumentTemplate',
      license='ZPL 2.1',
      description="Document Templating Markup Language (DTML)",
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      long_description=(open('README.rst').read() + '\n' +
                        open('CHANGES.rst').read()),
      packages=find_packages('src'),
      package_dir={'': 'src'},
      classifiers=[
          "Development Status :: 6 - Mature",
          "Environment :: Web Environment",
          "Framework :: Zope2",
          "License :: OSI Approved :: Zope Public License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2 :: Only",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: Implementation :: CPython",
      ],
      ext_modules=[
          Extension(
              name='DocumentTemplate.cDocumentTemplate',
              include_dirs=['include', 'src'],
              sources=[join('src', 'DocumentTemplate', 'cDocumentTemplate.c')],
              depends=[join('include', 'ExtensionClass', 'ExtensionClass.h')],
          ),
      ],
      install_requires=[
          'AccessControl',
          'Acquisition',
          'ExtensionClass>=4.1a1',
          'RestrictedPython',
          'zExceptions',
          'zope.sequencesort',
          'zope.structuredtext',
      ],
      include_package_data=True,
      zip_safe=False,
      )
