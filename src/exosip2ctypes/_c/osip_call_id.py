"""
osip_call_id Struct Reference
"""

from __future__ import absolute_import, unicode_literals

from ctypes import Structure, c_char_p


class CallId(Structure):
    """
    Definition of the Call-Id header.
    """
    _fields_ = [
        #: Call-ID number
        ('number', c_char_p),
        #: Call-ID host information
        ('host', c_char_p),
    ]
