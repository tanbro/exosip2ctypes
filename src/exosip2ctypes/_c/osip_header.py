"""
osip_header Struct Reference
"""

from ctypes import Structure, c_char_p


class Header(Structure):
    """
    Definition of a generic sip header.
    """
    _fields_ = [
        ('hname', c_char_p),  # < Name of header
        ('hvalue', c_char_p),  # < Value for header
    ]
