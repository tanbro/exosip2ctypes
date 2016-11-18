eXosip2CTypes
#############

exosip2ctypes is a `python`_ package, it wraps `eXosip2`_.

The library is based on `ctypes`_, so it can be used with `eXosip2`_ without compiling a C extension.

Environment
===========

OS:

* Linux
* MacOS

Python:

* Python2.x: 2.6 +
* Python3.x: 3.0 +

Install
=======

1. Install `eXosip2`_.

    `eXosip2`_ is based on `eXosip2`_.
    You can compile those two libraries from code, or install by a package manager if possible.
    For example, ubuntu 16.04 users can install the library by::

        sudo apt install libexosip2-11

    "develop" packages are not needed.

2. Install `python`_

    `python`_ 2.7 and `python`_ 3.5+ are expect.

    `python`_ 2.7 is usually installed by default in many POSIX OS.

3. Install the package

    It's advised to install the package by `pip`_::

        path/to/your/python -m pip install exosip2ctypes

    Or get the source files from http://github.com/tanbro/exosip2ctypes , then install::

        cd path/to/exosip2ctypes
        path/to/your/python setup.py install

Develop
=======
Visit http://exosip2ctypes.readthedocs.org/ for the api docs.

The project's API documentation is written inside the source code as `Docstring`_ ,
you shall build the documentation from source, using `sphinx-doc`_ .

.. _osip2: http://www.gnu.org/software/osip/

.. _eXosip2: http://www.gnu.org/software/osip/

.. _python: http://python.org/

.. _pip: http://pypi.python.org/pypi/pip

.. _ctypes: http://docs.python.org/3/library/ctypes.html

.. _enum34: http://pypi.python.org/pypi/enum34

.. _futures: http://pypi.python.org/pypi/futures

.. _Docstring: http://www.python.org/dev/peps/pep-0257/

.. _sphinx-doc: http://sphinx-doc.org/

.. _virtualenv: https://pypi.python.org/pypi/virtualenv
