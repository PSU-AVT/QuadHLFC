import llfc
import plugin
import evloop
import struct
import settings

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

class JoystickWatcher(evloop.FdWatcher):
	def __init__(self, dev_path):
		super(JoystickWatcher, self).__init__()
		f = open(dev_path)
		self.fd = fd
		self.setup_fd(f, 0)
		self.set_readable(True)

	def handle_read(self, fd):
		msg = self.fd.read(8)
		event = JoystickEvent.init_from_linux_raw(msg)

class JoystickPlugin(plugin.Plugin):
	enabled = settings.joystick_enabled

	def __init__(self):
		self.joystick_watcher = JoystickWatcher(settings.joystick_path)

