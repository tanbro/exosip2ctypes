:Source: http://github.com/tanbro/exosip2ctypes/
:Document: http://exosip2ctypes.readthedocs.org/
:Repo: http://pypi.org/project/exosip2ctypes/

|travis| |codacy-grade| |codacy-coverage| |readthedocs| |pylicense| |pyversion| |pyimp| |pyformat| |pystatus|

------

eXosip2CTypes
==============

eXosip2CTypes is a `python`_ package, it wraps `eXosip2`_.

The library is based on `ctypes`_, it loads `eXosip2`_ shared object on runtime.

Environment
-----------

OS:

* Linux
* MacOS

Python:

* Python2.x: 2.7
* Python3.x: 3.3 and later

Install
-------

1. Install `eXosip2`_.

    `eXosip2`_ depends on `osip2`_, they are native ``C`` libraries.
    You can compile these two libraries from source code, or install them with a package manager if possible.
    For example, ubuntu 16.04 users can install the libraries by::

        sudo apt install libexosip2-11

    "develop" packages are not needed.

2. Install `python`_

    `python`_ 2.7 and `python`_ 3.4+ are expect.

    `python`_ 2.7 is installed by default in many POSIX OS.

3. Install eXosip2CTypes

    It's advised to install eXosip2CTypes by `pip`_::

        pip install exosip2ctypes

    Or clone from http://github.com/tanbro/exosip2ctypes, then install by ``setup.py``::

        https://github.com/tanbro/exosip2ctypes.git
        cd exosip2ctypes
        path/of/your/python setup.py install

Develop
-------

Now, your can use it in your APP, Good luck!

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

.. |travis| image:: https://img.shields.io/travis/tanbro/exosip2ctypes.svg
   :target: https://github.com/tanbro/exosip2ctypes

.. |codacy-grade| image:: https://img.shields.io/codacy/grade/842a184f326741ca8ed208bd33238b6c.svg
    :target: https://www.codacy.com/app/tanbro/exosip2ctypes?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tanbro/exosip2ctypes&amp;utm_campaign=Badge_Grade

.. |codacy-coverage| image:: https://img.shields.io/codacy/coverage/842a184f326741ca8ed208bd33238b6c.svg
    :target: https://www.codacy.com/app/tanbro/exosip2ctypes?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=tanbro/exosip2ctypes&amp;utm_campaign=Badge_Grade

.. |readthedocs| image:: https://readthedocs.org/projects/exosip2ctypes/badge/?version=latest
    :target: http://exosip2ctypes.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. |pylicense| image:: https://img.shields.io/pypi/l/exosip2ctypes.svg
    :alt: GNU GENERAL PUBLIC LICENSE
    :target: http://www.antisip.com/doc/exosip2/eXosip2_license.html

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/exosip2ctypes.svg
    :alt: Supported Python versions.
    :target: http://pypi.python.org/pypi/exosip2ctypes/

.. |pyimp| image:: https://img.shields.io/pypi/implementation/exosip2ctypes.svg
    :alt: Support Python implementations.
    :target: http://pypi.python.org/pypi/exosip2ctypes/

.. |pyformat| image:: https://img.shields.io/pypi/format/exosip2ctypes.svg
    :target: http://pypi.python.org/pypi/exosip2ctypes/

.. |pystatus| image:: https://img.shields.io/pypi/status/exosip2ctypes.svg
    :target: http://pypi.python.org/pypi/exosip2ctypes/
