import afprotowatcher
import logging
import struct

class State(object):
	def __init__(self, roll, pitch, yaw, x, y, z):
		self.roll = roll
		self.pitch = pitch
		self.yaw = yaw
		self.x = x
		self.y = y
		self.z = z

	def toBinaryString(self):
		return struct.pack('=ffffff', self.roll, self.pitch, self.yaw, self.x, self.y, self.z)

	def fromBinaryString(self, string):
		self.roll, self.pitch, self.yaw, self.x, self.y, self.z = struct.unpack('ffffff', string)

class Llfc(afprotowatcher.SerialAfprotoWatcher):
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Llfc, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self, path='/dev/ttyUSB0', baudrate=115200, pubsub_server=None):
		afprotowatcher.SerialAfprotoWatcher.__init__(self, path, baudrate)
		str_unpack = lambda x: str(struct.unpack('%ds' % len(x), x))
		state_unpack = lambda x: struct.unpack('%6f' % len(x))
		recv_cmds = {
			2: ('debug_msg', str_unpack),
			3: ('error_msg', str_unpack),
			4: ('gyro_state', state_unpack),
			5: ('accelerometer_state', state_unpack),
			6: ('inertial_state', state_unpack),
			7: ('motors_state', lambda x: struct.unpack('4f', x)),
			8: ('setpoint_state', state_unpack),
			}
		self.msg_handlers = {}

	def handle_msg(self, msg):
		try:
			cmd_id = ord(msg[0])
			recv_cmd = self.recv_cmds[cmd_id]
			name = recv_cmd[0]
			unpacker = recv_cmd[1]
			self.msg_handlers[name](*unpacker(msg[1:]))
		except KeyError:
			pass

	def handle_debug_msg(self, msg):
		# trash the msg id byte
		msg = msg[1:]		
		
		# log debug message
		logging.debug('LLFC Debug: %s' % msg)

		self.publish('LlfcDebug', msg)

	def send_command(self, cmd_id, data):
		self.send_msg(chr(cmd_id) + data)

