import plugin
import settings
from eventbus import event_bus

import socket
import evloop
import logging

if settings.remoteevent_enabled:
	import msgpack

class TcpClient(evloop.TcpSocketWatcher):
	def __init__(self, socket):
		super(TcpClient, self).__init__()
		self.setup_socket(socket)
		self.unpacker = msgpack.Unpacker()

	def handle_read(self, fd):
		print 'read'
		data = self.socket.recv(1024)
		if not data:
			self.close()
			return
		self.unpacker.feed(data)
		for ev in self.unpacker:
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
			logging.debug('Got event %s with args %s, kwargs %s', event_name, event_args, event_kwargs)
			event_bus.emit(event_str, *event_args, **event_kwargs)

class TcpServer(evloop.TcpSocketWatcher):
	def __init__(self, host, port):
		super(TcpServer, self).__init__()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))
		s.listen(3)
		self.setup_socket(s)

	def handle_read(self, fd):
		client = TcpClient(self.socket.accept()[0])

class RemoteEventPlugin(plugin.Plugin):
	enabled = settings.remoteevent_enabled

	def __init__(self):
		self.tcp_server = TcpServer(settings.remoteevent_host,\
		                            settings.remoteevent_port)

