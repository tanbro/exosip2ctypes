#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path

# Always prefer setuptools over distutils
from setuptools import setup, find_packages


PY_MAJOR_MINOR = '{0[0]}.{0[1]}'.format(sys.version_info)
TESTS_REQUIRE = []
if PY_MAJOR_MINOR < '3.3':
    # Backport of the unittest.mock package from Python 3.3
    TESTS_REQUIRE.append('mock')

setup(
    name='exosip2ctypes',

    packages=find_packages('src'),
    package_dir={'': 'src'},  # tell distutils packages are under src
    test_suite='exosip2ctypes.tests',
    description='libeXosip2 Python wrapper',
    author='Liu Xue Yan',
    author_email='realtanbro@gmail.com',
    url='http://github.com/tanbro/exosip2ctypes',
    license='GPL',

    use_scm_version={
        # guess-next-dev:	automatically guesses the next development version (default)
        # post-release:	generates post release versions (adds postN)
        'version_scheme': 'guess-next-dev',
    },
    setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],

    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',

    install_requires=[
        'enum34;python_version<"3.4"',
        'futures;python_version<"3.0"',
    ],
    tests_require=TESTS_REQUIRE,

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Communications :: Telephony',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License (GPL)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    keywords='sip osip osip2 libosip lilbosip2 eXosip eXosip2 libeXosip2 exosip2ctypes',
)
