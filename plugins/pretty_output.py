import plugin
from eventbus import event_bus

class PrettyOutputPlugin(plugin.Plugin):
	def __init__(self):
		event_bus.connect('llfc.turn_on', self.turn_on)
		event_bus.connect('llfc.turn_off', self.turn_off)
		event_bus.connect('llfc.inertial_state', self.inertial_state)
		event_bus.connect('llfc.roll_setpoint', self.roll_setpoint)
		event_bus.connect('llfc.pitch_setpoint', self.pitch_setpoint)
		event_bus.connect('llfc.yaw_setpoint', self.yaw_setpoint)
		event_bus.connect('llfc.z_setpoint', self.z_setpoint)

	def inertial_state(self, state):
		print 'Roll: %0.5f\tPitch: %0.5f\tYaw: %0.5f\tZ: %0.5f' % (state[0], state[1], state[2], state[5])

	def turn_on(self):
		print 'LLFC is on'

	def turn_off(self):
		print 'LLFC is off'

	def roll_setpoint(self, roll):
		print 'Set roll to %f' % roll

	def pitch_setpoint(self, pitch):
		print 'Set pitch to %f' % pitch

	def yaw_setpoint(self, yaw):
		print 'Set yaw to %f' % yaw

	def z_setpoint(self, z):
		print 'Set z to  %f' % z
