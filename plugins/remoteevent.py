import plugin
import settings
from eventbus import event_bus

import socket
import evloop

if settings.remoteevent_enabled:
	import msgpack

class TcpServer(evloop.TcpSocketWatcher):
	def __init__(self, host, port):
		super(TcpServer, self).__init__()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))
		self.setup_socket(s)
		self.unpacker = msgpack.Unpacker()

	def handle_read(self, fd):
		unpacker.feed(self.socket.recv())
		for ev in unpacker:
			try:
				event_name = ev['name']
			except KeyError:
				continue
			try:
				event_args = ev['args']
			except KeyError:
				event_args = ()
			try:
				event_kwargs = ev['kwargs']
			except KeyError:
				event_kwargs = {}
			try:
				event_rooted = ev['rooted']
			except KeyError:
				event_rooted = False
			if event_rooted:
				event_str = event_name
			else:
				event_str = 'remote_event.%s' % event_name
			event_bus.emit(event_str, *event_args, **event_kwargs)

class RemoteEventPlugin(plugin.Plugin):
	enabled = settings.remoteevent_enabled

	def __init__(self):
		self.tcp_server = TcpServer(settings.remoteevent_host,\
		                            settings.remoteevent_port)

