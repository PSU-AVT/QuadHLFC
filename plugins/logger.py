import logging

import plugin
from llfc import llfc

class Logger(plugin.Plugin):
	def __init__(self):
		llfc.add_cmd_handler('debug', self.debug)
		llfc.add_cmd_handler('error', self.error)

	def debug(self, msg):
		logging.debug('Quadcopter: ' %s)

	def error(self, msg):
		logging.error('Quadcopter: ' %s)
