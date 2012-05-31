import logging
import collections
import os

import settings

class PluginLoader(Object):
	def __init__(self):
		self.plugins_dir = settings.plugins_dir
		self.plugins = collections.dequeue()

	def load_all():
		logging.debug('Starting plugin loading')
		plugins = os.listdir(self.plugins_dir)
			for plugin in plugins:
				print plugin
		logging.debug('Finished plugin loading')

class Plugin(Object):
	pass
