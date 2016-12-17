# -*- coding: utf-8 -*-

"""eXosip API

:author: Liu Xue Yan
:email: realtanbro@gmail.com

eXosip is a high layer library for rfc3261: the SIP protocol. It offers a simple API to make it easy to use.
eXosip2 offers great flexibility for implementing SIP endpoint like:

* SIP User-Agents
* SIP Voicemail or IVR
* SIP B2BUA
* any SIP server acting as an endpoint (music server...)

If you need to implement proxy or complex SIP applications, you should consider using osip instead.

Here are the eXosip capabilities:

* REGISTER                 to rpc_handler registration.
* INVITE/BYE               to start/stop VoIP sessions.
* INFO                     to send DTMF within a VoIP sessions.
* OPTIONS                  to simulate VoIP sessions.
* re-INVITE                to modify VoIP sessions
* REFER/NOTIFY             to transfer calls.
* MESSAGE                  to send Instant Message.
* SUBSCRIBE/NOTIFY         to rpc_handler presence capabilities.
* any other request        to rpc_handler what you want!

Constants
==========

.. data:: DLL_NAME

    Default so/dll name, value is ``eXosip2``

Functions
==========

.. function:: initialize(path: str=None) -> None:

    Load `libeXosip2` into this Python library

    :param str path: `libeXosip2` SO/DLL path, `default` is `None`.
        When `None` or empty string, the function will try to find and load so/dll by :data:`DLL_NAME`
    :raises RuntimeError: When failed loading so/dll

    .. attention:: You **MUST** call this function **FIRST** to initialize `libeXosip2`, before any other actions!

"""

from ._c.lib import DLL_NAME, initialize, unload
from .context import *
from .event import *
from .version import *

#: version of the package, equal :data:`version.version`
__version__ = '1.1.3'
__date__ = '2016-12-16'
