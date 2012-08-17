from llfc import llfc
from eventbus import event_bus
import plugin
import evloop
import struct
import settings
import select
import logging

class JoystickEvent(object):
	BUTTON_EVENT = 0x01
	AXIS_EVENT = 0x02
	INIT_EVENT = 0x80

	@staticmethod
	def init_from_linux_raw(msg):
		return JoystickEvent(*struct.unpack("IhBB", msg))

	def __init__(self, time, value, event_type, number):
		self.time = time
		self.value = value
		self.event_type = event_type
		self.number = number

	def __repr__(self):
		type_str = {
			self.BUTTON_EVENT: 'BUTTON',
			self.AXIS_EVENT: 'AXIS'}[self.event_type & ~0x80]
		if self.event_type & 0x80 != 0:
			type_str += ' (init)'
		return 'Time: %d Type: %s Number: %d Value: %d' % (\
		        self.time, type_str, self.number, self.value)

class JoystickWatcher(evloop.FdWatcher):
	def __init__(self, dev_path):
		super(JoystickWatcher, self).__init__()
		f = open(dev_path)
		self.fd = f
		self.setup_fd(f, select.POLLIN)

	def handle_read(self, fd):
		msg = True
		while msg:
			try:
				msg = self.fd.read(8)
			except IOError:
				return
			event = JoystickEvent.init_from_linux_raw(msg)
			self.got_event(event)

	def got_event(self, event):
		logging.debug('Joystick event: %s' % event)
    		event_bus.emit('joystick.got_event', event)
		if event.event_type == JoystickEvent.AXIS_EVENT:
			if event.number == 3:
				event.value -= 32767
				event.value = -event.value
				llfc.set_z(event.value / float(32767))
			elif event.number == 0:
				llfc.set_roll(event.value / float(32767))
			elif event.number == 1:
				llfc.set_pitch(event.value / float(32767))
		elif event.event_type == JoystickEvent.BUTTON_EVENT:
			if (event.number == 2 or event.number == 3) and event.value == 1:
				llfc.turn_off()
			elif (event.number == 4 or event.number == 5) and event.value == 1:
				llfc.turn_on()

class JoystickPlugin(plugin.Plugin):
	enabled = settings.joystick_enabled
	driver = True

	def __init__(self):
		self.joystick_watcher = JoystickWatcher(settings.joystick_path)

