# -*- coding: utf-8 -*-

class MallocError(Exception):
    pass


class ExitNotZeroError(Exception):
    def __init__(self, func_name, exit_code):
        super().__init__("Function {0} returns {1}".format(func_name, exit_code))
        self._func_name = func_name
        self._exit_code = exit_code

    @property
    def func_name(self):
        return self._func_name

    @property
    def exit_code(self):
        return self._exit_code