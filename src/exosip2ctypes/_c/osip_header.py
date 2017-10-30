"""
osip_header Struct Reference
"""

from __future__ import absolute_import, unicode_literals

from ctypes import Structure, c_char_p


class Header(Structure):
    """
    Definition of a generic sip header.
    """
    _fields_ = [
        #: Name of header
        ('hname', c_char_p),
        #: Value for header
        ('hvalue', c_char_p),
    ]
