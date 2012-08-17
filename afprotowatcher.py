import evloop
import serial
import afproto

class SerialAfprotoWatcher(evloop.FdWatcher):
	def __init__(self, path, baudrate):
		evloop.FdWatcher.__init__(self)
		self.open_serial_path(path, baudrate)
		self.in_buff = ''
		self.out_buff = ''

	def open_serial_path(self, path, baudrate):
		self.device = serial.Serial(path, baudrate, timeout=0)
		self.setup_fd(self.device.fd, 0)
		self.set_readable()

	def send_msg(self, msg):
		frame = afproto.serialize_payload(msg)
		self.device.write(frame)
		return
		if len(self.out_buff) == 0:
			self.set_writable()
		self.out_buff += frame

	def handle_write(self, fd):
		sent = self.device.write(self.out_buff)
		self.out_buff = self.out_buff[sent:]
		if len(self.out_buff) == 0:
			self.set_writable(False)

	def handle_read(self, fd):
		self.in_buff += self.device.read(1)
		tmp_buff = self.in_buff
		msg, self.in_buff = afproto.extract_payload(self.in_buff)
		if msg != None:
			self.handle_msg(msg)


