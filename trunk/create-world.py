#!/usr/bin/python

import os
import sys
import getopt
    
cmdline_options, args = getopt.gnu_getopt(sys.argv[1:], "p:x:y:z:")
options = {"p": "26000"}
options.update(dict([(k.strip("-"), v) for k, v in cmdline_options]))

# Read the target from the command line
try:
    base_path = args[0]
except IndexError:
    print "Please provide the directory name for the new world."
    sys.exit(1)

# Make sure it doesn't exist already
if os.path.exists(base_path):
    print "The path you gave (%s) already exists." % base_path
    sys.exit(1)

# Make sure its parent does
if base_path[-1] == "/":
    base_path = base_path[:-1]
parent = os.path.dirname(base_path)
if not os.path.isdir(parent):
    print "The parent directory (%s) does not exist." % parent
    sys.exit(1)

# Make sure they specified the size
if "x" not in options or "y" not in options or "z" not in options:
    print "Please specify the size using -x, -y and -z."
    sys.exit(1)

# Make the directory
os.mkdir(base_path)

# Calculate some locations
x = int(options['x'])
y = int(options['y'])
z = int(options['z'])
options['sp_x'] = x // 2
options['sp_y'] = y
options['sp_z'] = z // 2

# Make the configuration file
cfh = open(os.path.join(base_path, "world.conf"), "w")
cfh.write("""
[network]
port = %(p)s

[size]
x = %(x)s
y = %(y)s
z = %(z)s

[spawn]
x = %(sp_x)s
y = %(sp_y)s
z = %(sp_z)s
""" % options)
    
# Alright, make a world.
from myne2.world.blockengine import BlockEngine
BlockEngine.create(base_path, x, y, z, ["\0"]*y)