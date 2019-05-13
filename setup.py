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

from setuptools import setup, find_packages

with open('README.rst') as f:
    README = f.read()

with open('CHANGES.rst') as f:
    CHANGES = f.read()

version = '3.1b1'


setup(name='DocumentTemplate',
      version=version,
      url='https://github.com/zopefoundation/DocumentTemplate',
      project_urls={
          'Documentation': ('https://zope.readthedocs.io/en/latest/'
                            'zopebook/index.html'),
          'Issue Tracker': ('https://github.com/zopefoundation/'
                            'DocumentTemplate/issues'),
          'Sources': 'https://github.com/zopefoundation/DocumentTemplate',
      },
      license='ZPL 2.1',
      description="Document Templating Markup Language (DTML)",
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      long_description='\n\n'.join([README, CHANGES]),
      packages=find_packages('src'),
      package_dir={'': 'src'},
      classifiers=[
          "Development Status :: 6 - Mature",
          "Environment :: Web Environment",
          "Framework :: Zope",
          "Framework :: Zope :: 4",
          "License :: OSI Approved :: Zope Public License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: Implementation :: CPython",
          "Topic :: Text Processing :: Markup",
      ],
      keywords='DTML template zope HTML SQL web markup',
      install_requires=[
          'AccessControl >= 4.0a5',
          'Acquisition',
          'ExtensionClass>=4.1a1',
          'RestrictedPython >= 4.0a1',
          'roman',
          'six',
          'zExceptions',
          'zope.sequencesort',
          'zope.structuredtext',
      ],
      include_package_data=True,
      zip_safe=False,
      )
