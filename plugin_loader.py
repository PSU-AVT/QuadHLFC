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
			if poss_plugin[-3:] == '.py':
				print 'loading %s' % full_path
				imp.load_source('plugins.'+poss_plugin, full_path)
			elif os.path.isdir(full_path) and os.path.isfile(full_path+'/__init__.py'):
				imp.load_source('plugins.'+poss_plugin, full_path+'/__init__.py')
			print poss_plugin
		logging.debug('Finished plugin loading')

