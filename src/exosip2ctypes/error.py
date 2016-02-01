# -*- coding: utf-8 -*-


class MallocError(Exception):
    pass


class ApiReturnError(Exception):
    def __init__(self, exit_code):
        super().__init__("eXosip2 function returns {}".format(int(exit_code)))
        self._exit_code = exit_code

    @property
    def exit_code(self):
        return self._exit_code
