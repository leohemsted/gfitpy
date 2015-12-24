#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import division, absolute_import, print_function

import os

from setuptools import find_packages
from setuptools import setup

# Get the long description from the relevant file
HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.rst')) as f:
    DESC = f.read()

setup(
    name='gfitpy',
    version='0.1.0',
    license='BSD',
    description='Gfitpy - A library for interacting with Google Fit',
    long_description=DESC,
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
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
    setup_requires=['pytest-runner'],
    tests_require=['mock', 'pytest'],
    entry_points={
        'console_scripts': [
            'gfitpy = gfitpy.__main__:main',
        ]
    },
)
