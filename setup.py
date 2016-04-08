from setuptools import setup, find_packages
from sys import version_info

pyver = '%s.%s' % (version_info[0], version_info[1])

if pyver < '3.2':
    INSTALL_REQUIRES = ['enum34', 'futures']
if pyver < '3.4':
    INSTALL_REQUIRES = ['enum34']
else:
    INSTALL_REQUIRES = []

setup(
    name='exosip2ctypes',
    version='0.1',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages('src'),  # include all packages under src, or special packages in a list.
    package_dir={'': 'src'},  # tell distutils packages are under src
    test_suite='exosip2ctypes.tests',
    description='libeXosip2 Python wrapper, using ctypes.',
    author='Liu Xue Yan',
    author_email='realtanbro@gmai.com',
    url='',
    license='GPL',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Communications :: Telephony',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License (GPL)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='sip osip osip2 libosip lilbosip2 eXosip eXosip2 libeXosip2 exosip2ctypes',
)
