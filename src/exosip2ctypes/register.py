# -*- coding: utf-8 -*-

"""eXosip2 REGISTER and Registration Management
"""

from ctypes import byref, create_string_buffer, c_void_p, c_int

from ._c import register
from .error import raise_if_osip_error
from .message import ExosipMessage
from .utils import to_bytes

__all__ = ['InitialRegister', 'Register']


class InitialRegister(ExosipMessage):
    """initial REGISTER request.

    To start a registration, you need to build a default REGISTER request by providing several mandatory headers.

    You can start as many registration you want even in one eXosip_t context.

    The created instance has a registration identifier (:attr:`rid`) that you can use to update your registration.
    In future events about this registration, you'll see that registration identifier when applicable.

    .. note::
        You should let eXosip2 manage contact headers alone.
        The setup you have provided will generate various behavior, all being controlled by eXosip2.
        See the "NAT and Contact header" section in setup documentation.
    """

    def __init__(self, context, from_, proxy, contact=None, expires=3600):
        """Build initial REGISTER request.

        :param context: eXosip_t instance.
        :param str from_: 	SIP url for caller.
        :param str proxy: 	Proxy used for registration.
        :param str contact:	Contact address. (optional)
        :param int expires: The expires value for registration.
        """
        ptr = c_void_p()  # osip_message_t* init_register_request = NULL;
        self._from = str(from_) if from_ else None
        self._proxy = str(proxy) if proxy else None
        self._contact = str(contact) if contact else None
        self._expires = abs(int(expires))
        rid = register.FuncRegisterBuildInitialRegister.c_func(
            context.ptr,
            create_string_buffer(to_bytes(self._from)) if self._from else None,
            create_string_buffer(to_bytes(self._proxy)) if self._proxy else None,
            create_string_buffer(to_bytes(self._contact)) if self._contact else None,
            c_int(self._expires),
            byref(ptr)
        )
        raise_if_osip_error(rid)
        self._rid = int(rid)
        super(InitialRegister, self).__init__(ptr, context)

    @property
    def rid(self):
        """
        :return: registration identifier
        :rtype: int
        """
        return self._rid

    @property
    def proxy(self):
        """
        :return:Proxy used for registration.
        :rtype: str
        """
        return self._proxy

    @property
    def contract(self):
        """
        :return: Contact address. (optional)
        :rtype: str
        """
        return self._contact

    @property
    def expires(self):
        """
        :return: The expires value for registration.
        :rtype: int
        """
        return self._expires

    def send(self):
        """Send this REGISTER request
        """
        error_code = register.FuncRegisterSendSegister.c_func(self.context.ptr, c_int(self._rid), self.ptr)
        raise_if_osip_error(error_code)

    def remove(self):
        """Remove existing registration without sending REGISTER.

        If you need to delete a context without sending a REGISTER with expires 0,
        you can use this method to release memory.
        """
        error_code = register.FuncRegisterRemove.c_func(self.context.ptr, c_int(self._rid))
        raise_if_osip_error(error_code)


class Register(ExosipMessage):
    """REGISTER request for an existing registration.

    Use this class if you need to update a registration,
    You just need to reuse the registration identifier (:class:`InitialRegister.rid`)


    .. note::
        An UAC should delete its registration on the SIP server when terminating.
        To do so, you have to send a REGISTER request with the expires header set to value "0".
    """

    def __init__(self, context, rid, expires=3600):
        """Build a new REGISTER request for an existing registration.

        :param Context context:	eXosip_t instance.
        :param int rid:         A unique identifier for the registration context
        :param int expires:     The expires value for registration.
        """
        ptr = c_void_p()  # osip_message_t* register_request = NULL;
        self._rid = abs(int(rid))
        self._expires = abs(int(expires))
        error_code = register.FuncRegisterBuildRegister.c_func(
            context.ptr,
            c_int(self._rid),
            c_int(self._expires),
            byref(ptr)
        )
        raise_if_osip_error(error_code)
        super(Register, self).__init__(ptr, context)

    @property
    def rid(self):
        """
        :return: A unique identifier for the registration context
        :rtype: int
        """
        return self._rid

    @property
    def expires(self):
        """
        :return: The expires value for registration.
        :rtype: int
        """
        return self._expires

    def send(self):
        """Send this REGISTER request
        """
        error_code = register.FuncRegisterSendSegister.c_func(self.context.ptr, c_int(self._rid), self.ptr)
        raise_if_osip_error(error_code)

    def remove(self):
        """Remove existing registration without sending REGISTER.

        If you need to delete a context without sending a REGISTER with expires 0,
        you can use this method to release memory.
        """
        error_code = register.FuncRegisterRemove.c_func(self.context.ptr, c_int(self._rid))
        raise_if_osip_error(error_code)
