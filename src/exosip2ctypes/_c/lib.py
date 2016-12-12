# -*- coding: utf-8 -*-

import logging
from ctypes import CDLL
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
    if globs.libexosip2:
        raise RuntimeError('library eXosip2 already loaded')
    if not path:
        _logger.debug('initialize: find_library "%s"', DLL_NAME)
        path = find_library(DLL_NAME)
        if not path:
            raise RuntimeError('Failed to find library {}'.format(DLL_NAME))
    _logger.debug('initialize: CDLL %s', path)
    globs.libexosip2 = CDLL(path)
    if not globs.libexosip2:
        raise RuntimeError('Failed to load library {}'.format(path))
    _logger.debug('initialize: libexosip2=%s', globs.libexosip2)
    for cls in globs.func_classes:
        cls.bind()
    _logger.info('initialize: <<<')


def free(ptr):
    """ ANSI C ``free()`` function

    :param ptr: CTypes Pointer(``ctypes.c_void_p``) to the resource to free
    """
    if not globs.libexosip2:
        raise RuntimeError('library eXosip2 not loaded')
    globs.libexosip2.free(ptr)


def unload():
    if globs.libexosip2:
        globs.libexosip2 = None
