import logging

import plugin
import llfc

class Logger(plugin.Plugin):
	def __init__(self):
		llfc.Llfc().add_cmd_handler('debug_msg', self.debug)

	def debug(self, msg):
		logging.debug('Quadcopter: ' %s)
