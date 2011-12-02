import socket
import struct

import afproto
import evloop

import settings

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
		cmd_id = struct.unpack('B', data[:1])[0]
		data = data[1:]
		self.handle_command(cmd_id, data, addr)

	def handle_command(self, command_id, data, addr):
		print "Got command %d of length %d" % (command_id, len(data))
		if settings.ControlGw.command_id['Ping'] == command_id:
			msg = struct.pack('B', settings.ControlGw.response_id['Pong'])
			msg += data
			self.socket.sendto(msg, addr)
		else:
			self.controller.send_msg(data)

