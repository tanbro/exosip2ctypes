eXosip2CTypes
#############

exosip2ctypes is a Python package,
it wraps `eXosip2`_.

The library is based on `ctypes`_,
so it can be used with `libeXosip2` without compiling.

Supported Python version
=========================
* Python2.x: 2.6 +
* Python3.x: 3.0 +

Dependencies
============
Below Python3.4:

	The 3rd-part library `enum34`_ is required,
	you can simply install the library using `pip`_::

    	pip install enum34

Below Python3.2:

	The 3rd-part library `futures`_ is required,
	you can simply install the library using `pip`_::

    	pip install futures

Contributing
============
Contributions are welcome!

Development Environment
-----------------------
You can prepare your development environment as blow:

1. Install `pip`_
`````````````````
See https://pip.pypa.io/en/stable/installing/

2. Create a virtual environment
```````````````````````````````
It's advised to develop in a `Python Virtual Environment<https://docs.python.org/3/library/venv.html>`

If you're using Python3.3+, create a new virtual environment by following command::

    python -m venv /your/virtual/env

else, install `virtualenv`_, and then create a virtual environment by following command::

    python -m virtualenv /your/virtual/env

After that, active the virtual environment:

    * POSIX::

        source /your/virtual/env/bin/activate

    * Widows::

        \your\virtual\env\Scripts\activate

3. Install dependencies
```````````````````````
For Python version less than 3.2 (including 2.x),
install dependencies from requirements file `requirements-lt_3.3-dev.txt`::

    pip install -r requirements-dev-lt_3.2.txt

For Python version greater than or qual to 3.2 (including 2.x), and smaller than 3.4,
install dependencies from requirements file `requirements-lt_3.4-dev.txt`::

    pip install -r requirements-dev-lt_3.4.txt

else install the dependencies from requirements file `requirement-dev.txt`::

    pip install -r requirements-dev.txt

4. Developing
`````````````
Now, you can start developing, look at:

* http://www.antisip.com/doc/exosip2/index.html
* http://www.gnu.org/software/osip/doc/html/index.html

Good luck!

Documentation
=============
Visit http://exosip2ctypes.readthedocs.org/ for the docs.

The project's API documentation is written inside the source code as `Docstring`_ ,
you shall build the documentation from source, using `sphinx-doc`_ .

.. _eXosip2: http://www.antisip.com/exosip2-toolkit

.. _ctypes: http://docs.python.org/3/library/ctypes.html

.. _enum34: http://pypi.python.org/pypi/enum34

.. _futures: http://pypi.python.org/pypi/futures

.. _Docstring: http://www.python.org/dev/peps/pep-0257/

.. _sphinx-doc: http://sphinx-doc.org/

.. _pip: http://pypi.python.org/pypi/pip

.. _virtualenv: https://pypi.python.org/pypi/virtualenv
