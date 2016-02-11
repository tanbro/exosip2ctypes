# -*- coding: utf-8 -*-


from ._c.osip_error import *


class MallocError(Exception):
    pass


class OsipError(Exception):
    pass


class OsipUnknownError(OsipError):
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


osip_error_map = {
    OSIP_UNDEFINED_ERROR: OsipUndefinedError,
    OSIP_BADPARAMETER: OsipBadParameter,
    OSIP_WRONG_STATE: OsipWrongFormat,
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

    use it to check osip2/eXosip2 API function integer return value

    :param error_code:
    :type error_code: int or ctypes.c_int
    :param message: Exception message
    :raises OsipError: if `err_code` is not zero
    """
    error_code = int(error_code)
    if error_code != OSIP_SUCCESS:
        exce_cls = osip_error_map.get(error_code, OsipUnknownError)
        if message:
            raise exce_cls(message)
        else:
            raise exce_cls()
