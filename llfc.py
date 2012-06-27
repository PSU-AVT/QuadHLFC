import afprotowatcher
import logging
import struct

def cmd_handler(fn, cmd_name):
	Llfc().add_cmd_handler(cmd_name, fn)

class Llfc(afprotowatcher.SerialAfprotoWatcher):
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Llfc, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self, path='/dev/ttyUSB0', baudrate=115200):
		if path != None:
			afprotowatcher.SerialAfprotoWatcher.__init__(self, path, baudrate)
		str_unpack = lambda x: str(struct.unpack('%ds' % len(x), x))
		state_unpack = lambda x: struct.unpack('6f' % len(x))
		recv_cmds = {
			2: ('debug_msg', str_unpack),
			3: ('error_msg', str_unpack),
			4: ('gyro_state', lambda x: struct.unpack('3f', x)),
			5: ('accelerometer_state', lambda x: struct.unpack('3f', x)),
			6: ('inertial_state', state_unpack),
			7: ('motors_state', lambda x: struct.unpack('4f', x)),
			8: ('setpoint_state', state_unpack),
			}
		self.cmd_handlers = {}

	def handle_msg(self, msg):
		try:
			cmd_id = ord(msg[0])
			recv_cmd = self.recv_cmds[cmd_id]
			name = recv_cmd[0]
			unpacker = recv_cmd[1]
			self.cmd_handlers[name](*unpacker(msg[1:]))
		except KeyError:
			pass

	def send_command(self, cmd_id, data):
		self.send_msg(chr(cmd_id) + data)

	def add_cmd_handler(self, cmd_name, handler):
		self.cmd_handlers[cmd_name] = handler

llfc = Llfc(None, 9600)
