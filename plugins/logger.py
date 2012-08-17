import logging

import plugin
from eventbus import event_bus

class Logger(plugin.Plugin):
	enable = True

	def __init__(self):
		event_bus.connect('llfc.debug_msg', self.debug)
		event_bus.connect('llfc.error_msg', self.error)
		event_bus.connect('llfc.inertial_state', self.inertial_state)

	def debug(self, msg):
		logging.debug('Quadcopter: %s' % msg)

	def error(self, msg):
		logging.error('Quadcopter: %s' % msg)

	def inertial_state(self, state):
		logging.debug('Quadcopter state: Roll: %f\tPitch: %f\tYaw: %f' % (state[0], state[1], state[2]))
