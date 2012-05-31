#!/usr/bin/env python
import struct
import logging
import evloop
from optparse import OptionParser

if __name__=='__main__':
	# Setup the option parser
	use = "Usage: %prog [-options]"
	parser = OptionParser(usage=use)
	(options, args) = parser.parse_args()

	import llfc
	lfc = llfc.Llfc(None, 57600)

	logging.basicConfig(level=logging.DEBUG)
	evloop.EventDispatcher().loop_forever()

