class Plugin(object):
	'''Base class for all plugins
	   to create a plugin, subclass this and place in the plugins
	   directory.'''

	enabled = True # Set to false in subclasses to disable that plugin

	def activate(self):
		'''Called after plugin is loaded but before added to event
		   loop'''
		pass

	def deactivate(self):
		'''Called before plugin is unloaded'''
		pass
