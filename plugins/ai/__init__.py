import settings
import plugin
from eventbus import event_bus

enabled = settings.ai_enabled

class AiPlugin(plugin.Plugin):
	def __init__(self):
		event_bus.connect('remote_event.ai.takeoff', self.takeoff)
		event_bus.connect('remote_event.ai.takeoff', self.land)

	def takeoff(self):
		pass

	def land(self):
		pass
