import logging

import plugin
from eventbus import event_bus

class Logger(plugin.Plugin):
	def __init__(self):
		event_bus.connect('llfc.debug', self.debug)
		event_bus.connect('llfc.error', self.error)

	def debug(self, msg):
		logging.debug('Quadcopter: ' %s)

	def error(self, msg):
		logging.error('Quadcopter: ' %s)
