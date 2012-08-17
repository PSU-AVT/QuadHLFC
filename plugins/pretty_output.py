import plugin
from eventbus import event_bus

class PrettyOutputPlugin(plugin.Plugin):
	def __init__(self):
		event_bus.connect('llfc.turn_on', self.turn_on)
		event_bus.connect('llfc.turn_off', self.turn_off)
		event_bus.connect('llfc.inertial_state', self.inertial_state)

	def inertial_state(self, state):
		print 'Roll: %0.5f\tPitch: %0.5f\tYaw: %0.5f\tZ: %0.5f' % (state[0], state[1], state[2], state[5])

	def turn_on(self):
		print 'LLFC is on'

	def turn_off(self):
		print 'LLFC is off'
