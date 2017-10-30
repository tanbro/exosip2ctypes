"""
osip_content_length Struct Reference
"""

from __future__ import absolute_import, unicode_literals

from ctypes import Structure, c_char_p


class ContentLength(Structure):
    """Definition of the Content-Length header."""
    _fields_ = [
        #: value for Content-Length (size of attachments)
        ('value', c_char_p),
    ]


Allow = ContentLength
