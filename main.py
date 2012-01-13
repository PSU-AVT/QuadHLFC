import struct
import logging
import evloop

import llfc
import controlgw
import pubsub

if __name__=='__main__':
	logging.basicConfig(level=logging.DEBUG)
	lfc = llfc.Llfc('/dev/ttyUSB0', 115200, pubsub.PubSubServer('', 8090))
	cgw = controlgw.ControlGw('localhost', 8091, lfc)
	evloop.EventDispatcher().loop_forever()

