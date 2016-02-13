from distutils.core import setup

setup(
    name='exosipctypes',
    version='0.1',
    packages=['exosip2ctypes', 'exosip2ctypes._c', 'exosip2ctypes.tests'],
    package_dir={'': 'src'},
    url='',
    license='GPL',
    author='Liu Xue Yan',
    author_email='realtanbro@gmai.com',
    description='exosip2ctypes is a Python library wraps eXosip2 C API'
)
