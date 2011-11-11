import struct
import evloop

import llfc

if __name__=='__main__':
	lfc = llfc.Llfc('/dev/ttyUSB0', 115200)
	evloop.EventDispatcher().loop_forever()

