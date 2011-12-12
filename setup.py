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
      version = '2.13.2',
      url='http://pypi.python.org/pypi/DocumentTemplate',
      license='ZPL 2.1',
      description="Document Templating Markup Language (DTML)",
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      long_description=open('README.txt').read() + '\n' +
                       open('CHANGES.txt').read(),
      packages=find_packages('src'),
      package_dir={'': 'src'},
      ext_modules=[Extension(
            name='DocumentTemplate.cDocumentTemplate',
            include_dirs=['include', 'src'],
            sources=[join('src', 'DocumentTemplate', 'cDocumentTemplate.c')],
            depends=[join('include', 'ExtensionClass', 'ExtensionClass.h')]),
      ],
      install_requires=[
        'AccessControl',
        'Acquisition',
        'ExtensionClass',
        'RestrictedPython',
        'zExceptions',
        'zope.sequencesort',
        'zope.structuredtext',
      ],
      include_package_data=True,
      zip_safe=False,
      )
