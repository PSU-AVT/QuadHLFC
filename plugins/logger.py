import logging

import plugin
from eventbus import event_bus

class Logger(plugin.Plugin):
	enable = True

	def __init__(self):
		event_bus.connect('llfc.debug_msg', self.debug)
		event_bus.connect('llfc.error_msg', self.error)

	def debug(self, msg):
		logging.debug('Quadcopter: %s' % msg)

	def error(self, msg):
		logging.error('Quadcopter: %s' % msg)
