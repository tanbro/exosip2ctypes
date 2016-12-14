# -*- coding: utf-8 -*-

"""
Error definitions

see `osip/include/osipparser2/osip_port.h`
"""

from ._c.osip_error import *

__all__ = [
    'raise_if_osip_error', 'MallocError', 'OsipError', 'OsipUnknownError',
    'OsipUndefinedError', 'OsipBadParameter', 'OsipWrongState',
    'OsipNoMem', 'OsipSyntaxError', 'OsipNotFound', 'OsipApiNotInitialized',
    'OsipNoNetwork', 'OsipPortBusy', 'OsipUnknownHost', 'OsipDiskFull',
    'OsipNoRights', 'OsipFileNotExists', 'OsipTimeout', 'OsipTooMuchCall',
    'OsipWrongFormat', 'OsipNoCommonCodec'
]


class MallocError(RuntimeError):
    """
    Failed to allocate an `eXosip` context.
    """
    pass


class OsipError(RuntimeError):
    """
    Base `Osip` error :class:`Exception` Class
    """
    pass


class OsipUnknownError(OsipError):
    """
    Osip error, but don't known the error code
    """
    pass


class OsipUndefinedError(OsipError):
    pass


class OsipBadParameter(OsipError):
    pass


class OsipWrongState(OsipError):
    pass


class OsipNoMem(OsipError):
    pass


class OsipSyntaxError(OsipError):
    pass


class OsipNotFound(OsipError):
    pass


class OsipApiNotInitialized(OsipError):
    pass


class OsipNoNetwork(OsipError):
    pass


class OsipPortBusy(OsipError):
    pass


class OsipUnknownHost(OsipError):
    pass


class OsipDiskFull(OsipError):
    pass


class OsipNoRights(OsipError):
    pass


class OsipFileNotExists(OsipError):
    pass


class OsipTimeout(OsipError):
    pass


class OsipTooMuchCall(OsipError):
    pass


class OsipWrongFormat(OsipError):
    pass


class OsipNoCommonCodec(OsipError):
    pass


#: mappings between osip error codes and exception classes
osip_error_map = {
    OSIP_UNDEFINED_ERROR: OsipUndefinedError,
    OSIP_BADPARAMETER: OsipBadParameter,
    OSIP_WRONG_STATE: OsipWrongState,
    OSIP_NOMEM: OsipNoMem,
    OSIP_SYNTAXERROR: OsipSyntaxError,
    OSIP_NOTFOUND: OsipNotFound,
    OSIP_API_NOT_INITIALIZED: OsipApiNotInitialized,
    OSIP_NO_NETWORK: OsipNoNetwork,
    OSIP_PORT_BUSY: OsipPortBusy,
    OSIP_UNKNOWN_HOST: OsipUnknownHost,
    OSIP_DISK_FULL: OsipDiskFull,
    OSIP_NO_RIGHTS: OsipNoRights,
    OSIP_FILE_NOT_EXIST: OsipFileNotExists,
    OSIP_TIMEOUT: OsipTimeout,
    OSIP_TOOMUCHCALL: OsipTooMuchCall,
    OSIP_WRONG_FORMAT: OsipWrongFormat,
    OSIP_NOCOMMONCODEC: OsipNoCommonCodec,
}


def raise_if_osip_error(error_code, message=None):
    """raise an :exc:`OsipError` exception if `error_code` is not :data:`OSIP_SUCCESS`

    :param int error_code: `osip` and/or `exosip` C functions return code
    :param str message: Exception message passed to the raised :class:`OsipError`
    :raises OsipError: Throw exception if `error_code` is smaller than zero(:data:`OSIP_SUCCESS`)

    Can be used to check osip2/eXosip2 API function integer return value

    .. attention:: All error codes in `osip` are smaller than 0
    """
    error_code = int(error_code)
    if error_code < OSIP_SUCCESS:
        exce_cls = osip_error_map.get(error_code, OsipUnknownError)
        if message:
            raise exce_cls(message)
        else:
            raise exce_cls('{0}({1})'.format(exce_cls.__name__, error_code))
