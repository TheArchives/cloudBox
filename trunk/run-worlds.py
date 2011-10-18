#!/usr/bin/python
# Arc is copyright 2009-2011 the Arc team and other contributors.
# Arc is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSING" file in the "docs" folder of the Arc Package.

import sys
import logging
from twisted.internet import reactor

from myne2.world import World

logging.basicConfig(
    format="%(asctime)s - %(levelname)7s - %(message)s",
    level=("--debug" in sys.argv) and logging.DEBUG or logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Did they pass any worlds?
if len(sys.argv) == 1:
    print "Please provide some worlds to run."
    exit(1)

# Initialise worlds
worlds = [World(base_path) for base_path in sys.argv[1:]]

# Make them listen
for world in worlds:
    world.start()
    world.listen()

try:
    reactor.run()
finally:
    logging.info("Stopping...")
    for world in worlds:
        world.stop()