eXosip2CTypes
#############

exosip2ctypes is a Python package,
it wraps `eXosip2`_.

The library is based on `ctypes`_ ,
so it can be used with `libeXosip2` without compiling.

Dependencies
============
In Python2.x serials, Python2.7 is supported.
The 3rd-part library `enum34`_ is required,
you can simply install the library using `pip`_ ::

    pip install enum34

For Python3.4 and above, no 3rd-part dependencies are required.

For Python3.x blows 3.4, `enum34`_ is still required.

Contribution
============
Contributions are welcome!

1. Install `pip`_
-----------------
See https://pip.pypa.io/en/stable/installing/

2. Create a virtual environment
-------------------------------
It's advised to develop in a `python virtual environment<https://docs.python.org/3/library/venv.html>`

If you're using Python3.3+, create a virtual environment by::

    python -m venv /your/virtual/env

else, install `virtualenv`_, and then create a virtual environment by::

    python -m virtualenv /your/virtual/env

After that, active the virtual environment:

    * POSIX::

        source /your/virtual/env/bin/activate

    * Widows::

        /your/virtual/env/bin/activate

3. Install dependencies
-----------------------
For Python version less than 3.4, install the dependencies from the requirement file `requirements-lt_3.4-dev.txt` ::

    pip install -r requirements-lt_3.4-dev.txt

else install the dependencies from the requirement file `requirement-dev.txt` ::

    pip install -r requirements-dev.txt

4. Developing
-------------
Look at:

* http://www.antisip.com/doc/exosip2/index.html
* http://www.gnu.org/software/osip/doc/html/index.html

then develop, good luck!

Documentation
=============
The project's API documentation is written inside the source code as `Docstring`_ ,
you shall build the documentation from source, using `sphinx-doc`_ .

.. _eXosip2: http://www.antisip.com/exosip2-toolkit

.. _ctypes: http://docs.python.org/3/library/ctypes.html

.. _enum34: http://pypi.python.org/pypi/enum34

.. _Docstring: http://www.python.org/dev/peps/pep-0257/

.. _sphinx-doc: http://sphinx-doc.org/

.. _pip: https://pypi.python.org/pypi/pip

.. _virtualenv: https://pypi.python.org/pypi/virtualenv
