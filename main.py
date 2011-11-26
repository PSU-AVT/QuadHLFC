import struct
import logging
import evloop

import llfc

if __name__=='__main__':
	logging.basicConfig(level=logging.DEBUG)
	#lfc = llfc.Llfc('/dev/ttyUSB0', 115200)
	evloop.EventDispatcher().loop_forever()

