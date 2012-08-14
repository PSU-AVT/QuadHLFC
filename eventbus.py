class EventBus(object):
	def __init__(self):
		self.event_handlers = {}

	def connect(self, event, handler):
		try:
			handlers = self.event_handlers[event]
		except KeyError:
			handlers = []
			self.event_handlers[event] = handlers
		handlers.append(handler)

	def emit(self, event, *args, **kwargs):
		try:
			handlers = self.event_handlers[event]
		except KeyError:
			return
		for handler in handlers:
			handler(*args, **kwargs)

event_bus = EventBus()

