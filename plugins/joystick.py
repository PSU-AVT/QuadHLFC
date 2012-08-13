import llfc
import plugin

import pygame

print 'Initializing joystick plugin.'

# Joystick port on my laptop. More likely to be js0
jsport = "/dev/hidraw0"

# Control Gateway listens on UDP port 8089 and binds to all IPs on host
# First byte of CGW is command ID

class Joystick(plugin.Plugin):
        def __init__(self):
                print 'Self'
        def stick_movement(self, socket):
                data_stick = self.socket.recvfrom(4096)
                print 'Got: %s' % data_stick
        def button_press(self, button):
                data_button = self.socket.recvfrom(4096)
                print 'Button press: %s' % data_button

# where does this go?

        while True:
                handleEvent();

# X and Y axes
# Button press

# register the joystick file descripter as a handler
        # if any sockets have data or timers have timed out, 
        # each plugin has an event handler must return immediately

