import logging
import collections
import os

class PluginLoader(object):
	def __init__(self, plugins_dir):
		self.plugins_dir = plugins_dir
		self.plugins = collections.deque()

	def load_all(self):
		logging.debug('Starting plugin loading')
		plugins = os.listdir(self.plugins_dir)
		for plugin in plugins:
			print plugin
		logging.debug('Finished plugin loading')

class Plugin(object):
	pass
