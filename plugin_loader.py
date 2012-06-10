import logging
import collections
import os
import imp

class PluginLoader(object):
	def __init__(self, plugins_dir):
		self.plugins_dir = plugins_dir
		if self.plugins_dir[-1:] != '/':
			self.plugins_dir += '/'
		self.plugins = collections.deque()

	def load_all(self):
		logging.debug('Starting plugin loading')
		plugins_dir = os.listdir(self.plugins_dir)
		for poss_plugin in plugins_dir:
			full_path = self.plugins_dir + poss_plugin
			full_plugin_path = full_path.replace('/', '.')
			if poss_plugin[-3:] == '.py':
				logging.debug('loading %s' % full_path)
				__import__(full_plugin_path[:-3])
			elif os.path.isdir(full_path) and os.path.isfile(full_path+'/__init__.py'):
				__import__(full_plugin_path)
			else:
				logging.debug('skipping %s' + full_path)
		logging.debug('Finished plugin loading')

