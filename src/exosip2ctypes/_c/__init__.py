# -*- coding: utf-8 -*-

from ctypes import CDLL, RTLD_GLOBAL
from ctypes.util import find_library

from . import globs, auth, conf, event, message

DLL_NAME = 'eXosip2'


def load(path=''):
    if not path:
        path = find_library(DLL_NAME)
    globs.dll = CDLL(path, mode=RTLD_GLOBAL)
    for cls in globs.func_classes:
        cls.bind()
