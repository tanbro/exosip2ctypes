"""
osip_content_length Struct Reference
"""

from ctypes import Structure, c_char_p


class ContentLength(Structure):
    """
    Definition of the Content-Length header.
    """
    _fields_ = [
        ('value', c_char_p),  # < value for Content-Length (size of attachments)
    ]


Allow = ContentLength
