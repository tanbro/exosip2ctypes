# -*- coding: utf-8 -*-

import logging
from ctypes import CDLL, RTLD_GLOBAL, c_void_p
from ctypes.util import find_library

from . import globs

#: Default so/dll name
DLL_NAME = 'eXosip2'

_logger = logging.getLogger(__name__)


def initialize(path=None):
    """Load `libeXosip2` into this Python library

    :param str path: `libeXosip2` SO/DLL path, `default` is `None`.
        When `None` or empty string, the function will try to find and load so/dll by :data:`DLL_NAME`
    """
    _logger.info('initialize: >>> path=%s', path)
    if not path:
        _logger.debug('initialize: find_library "%s"', DLL_NAME)
        path = find_library(DLL_NAME)
    _logger.debug('initialize: CDLL %s', path)
    globs.libexosip2 = CDLL(path)
    _logger.debug('initialize: libexosip2=%s', globs.libexosip2)
    for cls in globs.func_classes:
        cls.bind()
    _logger.debug('initialize: find_library "c"')
    libc_path = find_library('c')
    if not libc_path:
        raise RuntimeError('Can not find "c" library')
    _logger.debug('initialize: CDLL %s', libc_path)
    globs.libc = CDLL(libc_path)
    _logger.debug('initialize: libc=%s', globs.libc)
    if not globs.libc:
        raise RuntimeError('Can not load "c" library')
    _logger.info('initialize: <<<')


def free(ptr):
    """`libc` ``free()`` function

    :param c_void_p ptr: Pointer to the resource to free
    """
    globs.libc.free(ptr)
