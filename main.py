#!/usr/bin/env python
import struct
import logging
import evloop
from optparse import OptionParser

import settings
import plugin_loader

if __name__=='__main__':
	# Setup the option parser
	use = "Usage: %prog [-options]"
	parser = OptionParser(usage=use)
	(options, args) = parser.parse_args()

	import llfc
	lfc = llfc.Llfc(None, 57600)

	pl = plugin_loader.PluginLoader(settings.plugins_dir)
	pl.load_all()

	logging.basicConfig(level=logging.DEBUG)
	evloop.EventDispatcher().loop_forever()

