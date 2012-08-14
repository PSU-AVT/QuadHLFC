import llfc
import plugin
import evloop

class JoystickWatcher(evloop.FdWatcher):
	def __init__(self, dev_path):
		super(JoystickWatcher, self).__init__()
		f = open(dev_path)
		self.fd = fd
		self.setup_fd(f, 0)
		self.set_readable(True)

	def handle_read(self, fd):
		msg = self.fd.read(8)
		print 'Got joystick event'

class JoystickPlugin(plugin.Plugin):
	enabled = False

	def __init__(self):
		self.joystick_watcher = JoystickWatcher('/dev/js0')

