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
		self.msg_handlers = {
			2: self.handle_debug_msg,
			3: self.handle_error_msg,
			4: self.handle_gyro_state,
			5: self.handle_accelero_state,
			6: self.handle_intertial_state,
			7: self.handle_motors_state,
			8: self.handle_setpoint_state }
		self.pubsub_server = pubsub_server

	def publish(self, tag, msg):
		try:
			self.pubsub_server.publish('' + tag + ': ' + msg)
		except AttributeError:
			pass

	def handle_msg(self, msg):
		try:
			self.msg_handlers[ord(msg[0])](msg)
		except KeyError:
			pass

	def handle_debug_msg(self, msg):
		# trash the msg id byte
		msg = msg[1:]		
		
		# log debug message
		logging.debug('LLFC Debug: %s' % msg)

		self.publish('LlfcDebug', msg)

	def handle_error_msg(self, msg):
		# trash the msg id byte
		msg = msg[1:]

		# log error message
		logging.error('LLFC Error: %s' % msg)

		self.publish('LlfcError', msg)

	def handle_gyro_state(self, msg):
		logging.debug('LLFC Gyro State:\tRoll: %f\tPitch: %f\tYaw: %f' % struct.unpack('fff', msg[1:]))
		self.publish('LlfcStateGyro', msg[1:])

	def handle_accelero_state(self, msg):
		logging.debug('LLFC Accelero State:\tX: %f\tY: %f\tZ: %f' % struct.unpack('fff', msg[1:]))
		self.publish('LlfcStateAccelero', msg[1:])

	def handle_intertial_state(self, msg):
		logging.debug('LLFC Inertial State:\tRoll: %f\tPitch: %f\tYaw: %f' % struct.unpack('fff', msg[1:13]))
		self.publish('LlfcStateInertial', msg[1:])

	def handle_motors_state(self, msg):
		logging.debug('Llfc Motors State: \t1: %f\t2: %f\t3: %f\t4: %f' % struct.unpack('ffff', msg[1:]))
		self.publish('LlfcStateMotors', msg[1:])

	def handle_setpoint_state(self, msg):
		logging.debug('Llfc Setpoint: \tRoll: %f\tPitch: %f\tYaw: %f' % struct.unpack('fff', msg[1:13]))
		print len(msg)
		self.publish('LlfcStateSetpoint', msg[1:])

	def send_command(self, cmd_id, data):
		self.send_msg(chr(cmd_id) + data)

