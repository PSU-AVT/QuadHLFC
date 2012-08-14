import llfc
import plugin

class HelloWorld(plugin.Plugin):
	enabled = False

	def __init__(self):
		print 'plugin hello'
