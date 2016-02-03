# -*- coding: utf-8 -*-


class MallocError(Exception):
    pass


error_codes = {
0: 'SUCCESS',
- 1: 'UNDEFINED_ERROR',
- 2:'BADPARAMETER',
- 3:'WRONG_STATE',
- 4:'NOMEM',
- 5:'SYNTAXERROR',
- 6:'NOTFOUND',
- 7: 'API_NOT_INITIALIZED',
- 10: 'NO_NETWORK',
- 11:'PORT_BUSY',
- 12:'UNKNOWN_HOST',
- 30:'DISK_FULL',
- 31:'NO_RIGHTS',
- 32:'FILE_NOT_EXIST',
- 50:'TIMEOUT',
- 51:'TOOMUCHCALL',
- 52:'WRONG_FORMAT',
- 53:'NOCOMMONCODEC',
}

class ApiReturnError(Exception):
    def __init__(self, exit_code):
        super().__init__("eXosip2 function returns {}".format(int(exit_code)))
        self._exit_code = exit_code

    @property
    def exit_code(self):
        return self._exit_code
