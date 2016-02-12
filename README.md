# eXosip2CTypes

exosip2ctypes is a [Python](http://python.org) library wraps [eXosip2](http://www.antisip.com/exosip2-toolkit) C API.

The library is based on [ctypes](http://docs.python.org/3/library/ctypes.html), so it can be used with eXosip without compiling.

## dependencies

### Python2.x
For Python2.x serials, Python2.7 are supported. The 3rd library [enum34](http://pypi.python.org/pypi/enum34) are needed, you can simply install the library using pip:

    pip install enum34

### Python3.x
No 3rd dependencies are needed for Python3.4 and above.
[enum34](http://pypi.python.org/pypi/enum34) are still needed in Python3.x blow 3.4.

## Documentation
The project's API documentation is written inside the soure code as [Docstring](http://www.python.org/dev/peps/pep-0257/), so you shall build the documentation from source using [sphinx-doc](sphinx-doc.org).
