import settings
import plugin
from eventbus import event_bus


class AiPlugin(plugin.Plugin):
	enabled = settings.ai_enabled
	driver = True

	def __init__(self):
		event_bus.connect('remote_event.ai.takeoff', self.takeoff)
		event_bus.connect('remote_event.ai.takeoff', self.land)

	def takeoff(self):
		pass

	def land(self):
		pass
