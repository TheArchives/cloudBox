# Arc is copyright 2009-2011 the Arc team and other contributors.
# Arc is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSING" file in the "docs" folder of the Arc Package.

"""
World protocol class
"""

from myne2.mprotocol import MyneProtocolBase
from myne2.format import Format

class WorldProtocol(MyneProtocolBase):
    
    PACKET_FORMATS = {
        0: ("initial", Format("bssb")),
    }
    
    