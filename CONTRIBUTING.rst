CONTRIBUTING
============

Contributions are welcome!

Environment
-----------
You can prepare your development environment as blow:

1. Preparation
``````````````
It's advised to develop on ubuntu 1604+.

Install libeXosip2 by::

    sudo apt install libexosip2-11

If using other OS, you may need to build libeXosip2 from source.

Install python, virtualenv, pip, wheel, setuptools

Python 2::

    sudo apt install python python-virtualenv python-pip python-setuptools

Python 3::

    sudo apt install python3 python3-virtualenv python3-pip python3-setuptools

2. Virtual Environment
``````````````````````
It's strongly recommended to do development in a python virtual environment::

    virutalenv --python=path/to/your/python path/to/your/env
    source path/to/your/env/bin/activate
    cd path/to/eXosip2CTypes
    python setup.py develop

Install other developing dependent libraries(optional)

Python version greater then 3.4::

    pip install -r requirements.txt

Python version 3.2 and 3.3::

    pip install -r requirements-lt_3.4.txt

Python version less then 3.2::

    pip install -r requirements-lt_3.2.txt

Developing
----------
Now, everything is ready, see C API here:

* http://www.antisip.com/doc/exosip2/index.html
* http://www.gnu.org/software/osip/doc/html/index.html
