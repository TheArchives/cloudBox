#!/usr/bin/python
# Arc is copyright 2009-2011 the Arc team and other contributors.
# Arc is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSING" file in the "docs" folder of the Arc Package.

import sys
import logging
from logging.handlers import SMTPHandler
from twisted.internet import reactor

from myne.server import MyneFactory
from myne.controller import ControllerFactory

logging.basicConfig(
    format="%(asctime)s - %(levelname)7s - %(message)s",
    level=("--debug" in sys.argv) and logging.DEBUG or logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

factory = MyneFactory()
controller = ControllerFactory(factory)
reactor.listenTCP(factory.config.getint("network", "port"), factory)
reactor.listenTCP(factory.config.getint("network", "controller_port"), controller)
logging.log(logging.INFO, "Running!")

# Setup email handler
if factory.config.has_section("email"):
    emh = SMTPHandler(
        factory.config.get("email", "host"),
        factory.config.get("email", "from"),
        [factory.config.get("email", "to")],
        factory.config.get("email", "subject"),
    )
    emh.setLevel(logging.ERROR)
    logging.root.addHandler(emh)

try:
    reactor.run()
finally:
    # Make sure worlds are flushed
    logging.log(logging.INFO, "Saving server meta...")
    factory.saveMeta()
    logging.log(logging.INFO, "Flushing worlds to disk...")
    for world in factory.worlds.values():
        world.stop()
        world.save_meta()