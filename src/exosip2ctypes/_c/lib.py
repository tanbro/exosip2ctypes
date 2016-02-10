# -*- coding: utf-8 -*-

from platform import system
from ctypes import CDLL, RTLD_GLOBAL, c_void_p
from ctypes.util import find_library

from . import globs, auth, conf, event, message

# < Default so/dll name
DLL_NAME = 'eXosip2'

# < libc ``free()`` function
free = None


def initialize(path=''):
    """Load `libeXosip2` into this Python library

    :param path: `libeXosip2` SO/DLL path.
        When `None` or empty string, the function will try to find and load so/dll by :data:`DLL_NAME`
    """
    if not path:
        path = find_library(DLL_NAME)
    globs.libexosip2 = CDLL(path, mode=RTLD_GLOBAL)
    for cls in globs.func_classes:
        cls.bind()
    libc_path = find_library('c')
    if not libc_path:
        raise RuntimeError('Can not find "c" library')
    libc = CDLL(libc_path)
    if not libc:
        raise RuntimeError('Can not load "c" library')
    global free
    free = getattr(libc, 'free')
    if not free:
        raise RuntimeError('Can not find std c function "free')
    free.argtypes = (c_void_p,)
