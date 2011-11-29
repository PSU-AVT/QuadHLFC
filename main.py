import struct
import logging
import evloop

import llfc
import controlgw

if __name__=='__main__':
	logging.basicConfig(level=logging.DEBUG)
	#lfc = llfc.Llfc('/dev/ttyUSB0', 115200)
	cgw = controlgw.ControlGw('localhost', 8091)
	evloop.EventDispatcher().loop_forever()

