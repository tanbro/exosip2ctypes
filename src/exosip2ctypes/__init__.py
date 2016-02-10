# -*- coding: utf-8 -*-

"""eXosip API

eXosip is a high layer library for rfc3261: the SIP protocol. It offers a simple API to make it easy to use. eXosip2 offers great flexibility for implementing SIP endpoint like:

    * SIP User-Agents
    * SIP Voicemail or IVR
    * SIP B2BUA
    * any SIP server acting as an endpoint (music server...)

If you need to implement proxy or complex SIP applications, you should consider using osip instead.

Here are the eXosip capabilities:

   * REGISTER                 to handle registration.
   * INVITE/BYE               to start/stop VoIP sessions.
   * INFO                     to send DTMF within a VoIP sessions.
   * OPTIONS                  to simulate VoIP sessions.
   * re-INVITE                to modify VoIP sessions
   * REFER/NOTIFY             to transfer calls.
   * MESSAGE                  to send Instant Message.
   * SUBSCRIBE/NOTIFY         to handle presence capabilities.
   * any other request        to handle what you want!
"""

from ._c.lib import DLL_NAME, initialize
from .call import *
from .context import *
from .version import *
