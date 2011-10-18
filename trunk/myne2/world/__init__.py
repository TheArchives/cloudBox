# Arc is copyright 2009-2011 the Arc team and other contributors.
# Arc is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSING" file in the "docs" folder of the Arc Package.

import os
import logging
from ConfigParser import RawConfigParser as ConfigParser

from twisted.internet import reactor
from twisted.internet.protocol import Factory

from myne2.world.worldprotocol import WorldProtocol
from myne2.world.blockengine import BlockEngine

class World(Factory):
    
    protocol = WorldProtocol
    
    def __init__(self, base_path):
        assert os.path.isdir(base_path)
        self.base_path = base_path
        self.config_path = os.path.join(self.base_path, "world.conf")
        self.load_config()
    
    def load_config(self):
        self.config = ConfigParser()
        self.config.read(self.config_path)
        self.size = [
            self.config.getint("size", "x"),
            self.config.getint("size", "y"),
            self.config.getint("size", "z"),
        ]
        self.spawn = [
            self.config.getint("spawn", "x"),
            self.config.getint("spawn", "y"),
            self.config.getint("spawn", "z"),
        ]
    
    def start(self):
        logging.info("Starting world '%s'" % self.base_path)
        self.engine = BlockEngine(self.base_path, self.size[0], self.size[1], self.size[2])
        self.engine.start_mmap()
    
    def stop(self):
        logging.info("Stopping world '%s'" % self.base_path)
        self.engine.stop_mmap()
        del self.engine
    
    def listen(self):
        # Makes us listen on our configured port.
        reactor.listenTCP(self.config.getint("network", "port"), self)