#!/usr/bin/env python
import struct
import logging
import evloop

import controlgw
import pubsub

from optparse import OptionParser

if __name__=='__main__':
	# Setup the option parser
	use = "Usage: %prog [-options]"
	parser = OptionParser(usage=use)
	parser.add_option('-s', '--noserial', dest="noserial", action="store_true", default=False, help="Disable serial")
	(options, args) = parser.parse_args()

	if not options.noserial:
		import llfc	
		lfc = llfc.Llfc('/dev/ttyUSB0', 57600, pubsub.PubSubServer('', 8090))
	else:
		lfc = None

	logging.basicConfig(level=logging.DEBUG)
	cgw = controlgw.ControlGw('localhost', 8091, lfc)
	evloop.EventDispatcher().loop_forever()

