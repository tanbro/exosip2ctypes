from . import globs


class OsipFunc:
    c_func = None
    prefix = 'osip_'
    func_name = ''
    argtypes = []
    restype = None

    @classmethod
    def bind(cls, dll=None):
        if dll is None:
            dll = globs.libexosip2
        cls.c_func = getattr(dll, '{0}{1}'.format(cls.prefix, cls.func_name))
        if cls.argtypes:
            cls.c_func.argtypes = cls.argtypes
        if cls.restype:
            cls.c_func.restype = cls.restype


class ExosipFunc(OsipFunc):
    prefix = 'eXosip_'
