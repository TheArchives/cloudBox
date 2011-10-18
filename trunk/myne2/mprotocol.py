# Arc is copyright 2009-2011 the Arc team and other contributors.
# Arc is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSING" file in the "docs" folder of the Arc Package.

"""
Basic protocol class for the original Minecraft format.
"""

from twisted.internet.protocol import Protocol


class MyneProtocolMetaclass(type):
    
    """
    Metaclass which makes the name-to-packet reverse mapping PKT.
    """
    
    def __new__(self, name, bases, kwargs):
        if name != "MyneProtocolBase":
            kwargs['PKT'] = type("PKT", tuple(), dict([(name.upper(), num) for num, (name, format) in kwargs['PACKET_FORMATS'].items()]))
        return type.__new__(self, name, bases, kwargs)


class MyneProtocolBase(object, Protocol):
    
    """
    Main protocol class for talking in myne-protocol-speak.
    """
    
    __metaclass__ = MyneProtocolMetaclass
    
    def sendPacked(self, mtype, *args):
        fmt = self.PACKET_FORMATS[mtype]
        self.transport.write(chr(mtype) + fmt.encode(*args))
    
    def sendError(self, error):
        self.log("Sending error: %s" % error)
        self.sendPacked(self.PKT.ERROR, error)
        reactor.callLater(0.2, self.transport.loseConnection)
    
    def packString(self, string, length=64, packWith=" "):
        return string + (packWith*(length-len(string)))

    def dataReceived(self, data):
        # First, add the data we got onto our internal buffer
        self.buffer += data
        # While there's still data there...
        while self.buffer:
            # Examine the first byte, to see what the command is
            type_num = ord(self.buffer[0])
            type_name, type_format = self.PACKET_FORMATS[type_num]
            # See if we have all its data
            if len(self.buffer) - 1 < len(type_format):
                # Nope, wait a bit
                break
            # OK, decode the data
            parts = list(type_format.decode(self.buffer[1:]))
            self.buffer = self.buffer[len(type_format)+1:]
            # Pass that off to a function to handle
            getattr(self, "pkt%s" % type_name.title())(parts)