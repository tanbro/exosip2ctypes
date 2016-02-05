# -*- coding: utf-8 -*-


from ._c.osip_error import *


class MallocError(Exception):
    pass


osip_errors = {
    OSIP_SUCCESS: 'SUCCESS',
    OSIP_UNDEFINED_ERROR: 'UNDEFINED_ERROR',
    OSIP_BADPARAMETER: 'BADPARAMETER',
    OSIP_WRONG_STATE: 'WRONG_STATE',
    OSIP_NOMEM: 'NOMEM',
    OSIP_SYNTAXERROR: 'SYNTAXERROR',
    OSIP_NOTFOUND: 'NOTFOUND',
    OSIP_API_NOT_INITIALIZED: 'API_NOT_INITIALIZED',
    OSIP_NO_NETWORK: 'NO_NETWORK',
    OSIP_PORT_BUSY: 'PORT_BUSY',
    OSIP_UNKNOWN_HOST: 'UNKNOWN_HOST',
    OSIP_DISK_FULL: 'DISK_FULL',
    OSIP_NO_RIGHTS: 'NO_RIGHTS',
    OSIP_FILE_NOT_EXIST: 'FILE_NOT_EXIST',
    OSIP_TIMEOUT: 'TIMEOUT',
    OSIP_TOOMUCHCALL: 'TOOMUCHCALL',
    OSIP_WRONG_FORMAT: 'WRONG_FORMAT',
    OSIP_NOCOMMONCODEC: 'NOCOMMONCODEC',
}


class OsipError(Exception):
    def __init__(self, error_code):
        self._error_code = error_code
        self._error_message = osip_errors.get(error_code, '')
        super(OsipError, self).__init__("osip/eXosip error: {}.".format(self._error_message))

    @property
    def error_code(self):
        return self._error_code

    @property
    def error_message(self):
        return self._error_message
