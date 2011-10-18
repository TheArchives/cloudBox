# Arc is copyright 2009-2011 the Arc team and other contributors.
# Arc is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSING" file in the "docs" folder of the Arc Package.

"""
Client protocol class
"""

from myne2.mprotocol import MyneProtocolBase
from myne2.format import Format

class ClientProtocol(MyneProtocolBase):
    
    PACKET_FORMATS = {
        0: ("initial", Format("bssb")),
        1: ("keepalive", Format("")),
        2: ("prechunk", Format("")),
        3: ("chunk", Format("hab")),
        4: ("levelsize", Format("hhh")),
        5: ("blockchange", Format("hhhbb")),
        6: ("blockset", Format("hhhb")),
        7: ("spawnpoint", Format("bshhhbb")),
        8: ("playerposabs", Format("bhhhbb")),
        9: ("playerposdir", Format("bbbbbb")),
        10: ("playerpos", Format("bbbb")),
        11: ("playerdir", Format("bbb")),
        12: ("playerleave", Format("b")),
        13: ("message", Format("bs")),
        14: ("error", Format("s")),
    }
    
    
