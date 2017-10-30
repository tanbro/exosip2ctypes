#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path

# Always prefer setuptools over distutils
from setuptools import setup, find_packages


PY_MAJOR_MINOR = '{0[0]}.{0[1]}'.format(sys.version_info)


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


# Read version from source file
version_module_dict = {}
exec(read('src/exosip2ctypes/version.py'), version_module_dict)
__version__ = version_module_dict['__version__']


INSTALL_REQUIRES = []
TESTS_REQUIRE = []

if PY_MAJOR_MINOR < '3.4':
    # Backport of the enum package from Python 3.4
    INSTALL_REQUIRES.append('enum34')
    TESTS_REQUIRE.append('enum34')
if PY_MAJOR_MINOR < '3.3':
    # Backport of the unittest.mock package from Python 3.3
    TESTS_REQUIRE.append('mock')
if PY_MAJOR_MINOR < '3.2':
    # Backport of the concurrent.futures package from Python 3.2
    INSTALL_REQUIRES.append('futures')
    TESTS_REQUIRE.append('futures')

setup(
    name='exosip2ctypes',
    version=__version__,
    tests_require=TESTS_REQUIRE,
    install_requires=INSTALL_REQUIRES,
    # include all packages under src, or special packages in a list.
    packages=find_packages('src'),
    package_dir={'': 'src'},  # tell distutils packages are under src
    test_suite='exosip2ctypes.tests',
    description='libeXosip2 Python wrapper',
    long_description=read('README.rst'),
    author='Liu Xue Yan',
    author_email='realtanbro@gmail.com',
    url='http://github.com/tanbro/exosip2ctypes',
    license='GPL',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Communications :: Telephony',
        'Topic :: Documentation :: Sphinx',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License (GPL)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    keywords='sip osip osip2 libosip lilbosip2 eXosip eXosip2 libeXosip2 exosip2ctypes',
)
