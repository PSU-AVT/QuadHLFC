import socket
import struct

import afproto
import evloop

class ControlGw(evloop.UdpSocketWatcher):
	def __init__(self, host, port, controller):
		evloop.FdWatcher.__init__(self)

		self.controller = controller

		# Create and bind socket
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.socket.bind((host, port)) 

		self.setup_socket(self.socket)

	def handle_read(self, fd):
		data, addr = self.socket.recvfrom(2048)
		cmd_id, arg = struct.unpack('BB', data)
		self.controller.write(afproto.serialize_payload(data))

	def handle_write(self, fd):
		pass

