from llfc import llfc
from eventbus import event_bus
import plugin
import evloop
import struct
import settings
import select

class JoystickEvent(object):
	BUTTON_EVENT = 0x01
	AXIS_EVENT = 0x00
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
			self.AXIS_EVENT: 'AXIS'}[self.event_type & 0x1]
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
			msg = self.fd.read(8)
			event = JoystickEvent.init_from_linux_raw(msg)
			self.got_event(event)

	def got_event(self, event):
    		event_bus.emit('joystick.got_event', event)
		if event.number == 3:
			event.value -= 32767
			event.value = -event.value
			llfc.set_z(event.value / float(32767))

class JoystickPlugin(plugin.Plugin):
	enabled = settings.joystick_enabled

	def __init__(self):
		self.joystick_watcher = JoystickWatcher(settings.joystick_path)

