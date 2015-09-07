#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division, absolute_import, print_function

import os

from setuptools import find_packages
from setuptools import setup
from setuptools.command.test import test as TestCommand

# Get the long description from the relevant file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# setup PyTest's weird TestCommand stuff
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)




setup(
    name='gfitpy',
    version='0.1.0',
    license='BSD',
    description='Gfitpy - A library for interacting with Google Fit',
    long_description=long_description,
    author='Leo Hemsted',
    author_email='leohemsted@gmail.com',
    url='https://github.com/leohemsted/gfitpy',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    keywords=[
        'fitness', 'google', 'api', 'rest'
    ],
    install_requires=[
        'httplib2',
        'requests',
        'google-api-python-client',
        # 'oauth2client>=1.4.6',
    ],
    tests_require=['mock', 'pytest'],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'gfitpy = gfitpy.__main__:main',
        ]
    },
)
