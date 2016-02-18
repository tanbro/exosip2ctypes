eXosip2CTypes
=============

exosip2ctypes is a Python package,
it wraps `eXosip2`_.

The library is based on `ctypes`_ ,
so it can be used with `libeXosip2` without compiling.

Dependencies
------------
For Python2.x serials, Python2.7 are supported.
The 3rd library `enum34`_ is required,
you can simply install the library using pip::

    pip install enum34

For Python3.4 and above, no 3rd dependencies are required.

For Python3.x blows 3.4, `enum34`_ is still required.

Documentation
-------------
The project's API documentation is written inside the source code as `Docstring`_ ,
you shall build the documentation from source, using `sphinx-doc`_ .

.. _eXosip2: http://www.antisip.com/exosip2-toolkit

.. _ctypes: http://docs.python.org/3/library/ctypes.html>

.. _enum34: http://pypi.python.org/pypi/enum34

.. _Docstring: http://www.python.org/dev/peps/pep-0257/

.. _sphinx-doc: http://sphinx-doc.org/