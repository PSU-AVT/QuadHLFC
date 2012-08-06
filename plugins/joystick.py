import logging
import sys # what is sys?

import plugin
from llfc import llfc

# find out which port the joystick uses
#  heavily depends on http://hackshark.com/?p=147#axzz22jTSqLWt

pipe = open('/dev/js0','r')

while 1:
        for character in pipe.read(1):
                sys.stdout.write(repr(character))
                sys.stdout.flush()


