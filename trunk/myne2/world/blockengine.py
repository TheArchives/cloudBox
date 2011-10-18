# Arc is copyright 2009-2011 the Arc team and other contributors.
# Arc is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSING" file in the "docs" folder of the Arc Package.

import mmap
import os
import threading
import subprocess
import struct

from myne2.deferred import Deferred

class BlockEngine(object):
    
    """
    Responsible for storing the 3D array of blocks which make up the World.
    Uses a disk-based mmap'd file for storing the array.
    
    Pass it a directory in which it can write - it will use the "blocks" and
    "blocks.gz" files in there to store the raw and gzipped versions.
    """
    
    def __init__(self, base_dir, sx, sy, sz):
        # Store the paths
        self.blocks_path = os.path.join(base_dir, "blocks")
        self.blocksheader_path = self.blocks_path + ".header"
        self.gzblocks_path = self.blocks_path + ".gz"
        # And the sizes
        self.sx = sx
        self.sy = sy
        self.sz = sz
        # Work out our expected data length
        self.size = sx * sy * sz
    
    @classmethod
    def create(self, base_dir, sx, sy, sz, levels):
        assert len(levels) == sy
        # Create the raw blocks file
        blocks_path = os.path.join(base_dir, "blocks")
        bfh = open(blocks_path, "w")
        for level in levels:
            bfh.write(level * (sx * sz))
        bfh.close()
    
    def start_mmap(self):
        "Initialises the mmap'd blocks array"
        self.blocks_handle = open(self.blocks_path, "r+")
        self.blocks = mmap.mmap(self.blocks_handle.fileno(), 0, access=mmap.ACCESS_WRITE)
        assert self.blocks.size() == self.size
    
    def stop_mmap(self):
        "Closes the mmap pointers"
        self.blocks.close()
        self.blocks_handle.close()
    
    def get_offset(self, x, y, z):
        "Turns block coordinates into a data offset"
        assert 0 <= x < self.sx
        assert 0 <= y < self.sy
        assert 0 <= z < self.sz
        return y*(self.sx*self.sz) + z*(self.sx) + x

    def get_coords(self, offset):
        "Turns a data offset into coordinates"
        assert 0 <= offset < self.size
        x = offset % self.sx
        z = (offset // self.sx) % self.sz
        y = offset // (self.sx * self.sz)
        return x, y, z
    
    def __getitem__(self, (x, y, z)):
        return self.blocks[self.get_offset(x, y, z)]
    
    def __setitem__(self, (x, y, z), value):
        assert isinstance(value, str)
        self.blocks[self.get_offset(x, y, z)] = value
    
    def get_gzip_handle(self):
        """
        Returns a Deferred object which will eventually yield a handle to
        the gzipped blocks file (with length header included).
        """
        d = Deferred()
        GzipperThread(self, d).start()
        return d


class GzipperThread(threading.Thread):
    
    def __init__(self, engine, deferred):
        self.engine = engine
        self.deferred = deferred
    
    def run(self):
        # Write the length header
        fh = open(self.engine.blocks_header_path, "w")
        fh.write(struct.pack("!i", self.engine.size))
        fh.close()
        # Gzip them up
        exitcode = subprocess.call('gzip -c "%s" "%s" > "%s"' % (
            self.engine.blocks_header_path,
            self.engine.blocks_path,
            self.engine.gzblocks_path,
        ), shell=True)
        # Return!
        if exitcode:
            print "gzip failed! %s" % exitcode
            self.deferred.errback(exitcode)
        else:
            self.deferred.callback(open(self.engine.gzblocks_path, "rb"))