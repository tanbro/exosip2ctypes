from . import globs


class ExosipStruct:
    def __init__(self, p):
        self._p = p

    @property
    def p(self):
        return self._p

    def release(self):
        self._p = None


class ExosipFunc:

    c_func = None

    func_name = ''

    argtypes = []

    restype = None

    @classmethod
    def bind(cls, dll=None):
        if dll is None:
            dll = globs.dll
        cls.c_func = getattr(dll, 'eXosip_{0}'.format(cls.func_name))
        if cls.argtypes:
            cls.c_func.argtypes = cls.argtypes
        if cls.restype:
            cls.c_func.restype = cls.restype
