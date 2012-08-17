import afprotowatcher
import logging
import struct
import eventbus
import settings

def cmd_handler(fn, cmd_name):
	Llfc().add_cmd_handler(cmd_name, fn)

class Llfc(afprotowatcher.SerialAfprotoWatcher):
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(Llfc, cls).__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self, path='/dev/ttyUSB0', baudrate=115200, event_bus=eventbus.EventBus()):
		if path != None:
			afprotowatcher.SerialAfprotoWatcher.__init__(self, path, baudrate)
		self.event_bus = event_bus
		self.path = path
		str_unpack = lambda x: str(struct.unpack('%ds' % len(x), x))
		state_unpack = lambda x: struct.unpack('6f', x)
		self.recv_cmds = {
			2: ('debug_msg', str_unpack),
			3: ('error_msg', str_unpack),
			4: ('gyro_state', lambda x: struct.unpack('3f', x)),
			5: ('accelerometer_state', lambda x: struct.unpack('3f', x)),
			6: ('inertial_state', state_unpack),
			7: ('motors_state', lambda x: struct.unpack('4f', x)),
			8: ('setpoint_state', state_unpack),
			}

	def handle_msg(self, msg):
		try:
			cmd_id = ord(msg[0])
			recv_cmd = self.recv_cmds[cmd_id]
		except KeyError:
			pass
		name = recv_cmd[0]
		unpacker = recv_cmd[1]
		logging.debug('Message from llfc. Type: %s Length: %d' % (name, len(msg)))
		self.event_bus.emit('llfc.%s' % name, unpacker(msg[1:]))

	def send_command(self, cmd_id, data):
		logging.debug('Sending command %d to llfc with data %s' % (cmd_id\
		              , ''.join(['%02x' % ord(ch) for ch in data])))
		if self.path != None:
			self.send_msg(chr(cmd_id) + data)

	def set_roll(self, roll):
		self.send_command(1, struct.pack('f', roll))

	def set_pitch(self, pitch):
		self.send_command(2, struct.pack('f', pitch))

	def set_yaw(self, yaw):
		self.send_command(5, struct.pack('f', yaw))

	def set_z(self, z):
		self.send_command(4, struct.pack('f', z))

	def turn_on(self):
		self.send_command(7, '')

	def turn_off(self):
		self.send_command(6, '')

llfc = Llfc(settings.llfc_serial_path, 57600, eventbus.event_bus)
