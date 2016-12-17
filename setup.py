from setuptools import setup, find_packages
from sys import version_info

PYVER = '%s.%s' % (version_info[0], version_info[1])

INSTALL_REQUIRES = []
TESTS_REQUIRE = []

if PYVER < '3.4':
    # Backport of the enum package from Python 3.4
    INSTALL_REQUIRES.append('enum34')
    TESTS_REQUIRE.append('enum34')
if PYVER < '3.3':
    # Backport of the unittest.mock package from Python 3.3
    TESTS_REQUIRE.append('mock')
if PYVER < '3.2':
    # Backport of the concurrent.futures package from Python 3.2
    INSTALL_REQUIRES.append('futures')
    TESTS_REQUIRE.append('futures')

setup(
    name='exosip2ctypes',
    version='0.1.2.post7',
    tests_require=TESTS_REQUIRE,
    install_requires=INSTALL_REQUIRES,
    # include all packages under src, or special packages in a list.
    packages=find_packages('src'),
    package_dir={'': 'src'},  # tell distutils packages are under src
    test_suite='exosip2ctypes.tests',
    description='libeXosip2 Python wrapper',
    long_description=open('README.rst').read(),
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
