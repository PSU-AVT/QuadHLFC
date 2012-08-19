# Plugins directory
plugins_dir = 'plugins'

# Path to serial device for LLFC (Usually an XBee)
llfc_serial_path = '/dev/ttyUSB0'

# Logging
import logging
# Log debug, notice, and error messages
#logging.basicConfig(level=logging.DEBUG)

# Only log error messages
logging.basicConfig(level=logging.ERROR)

# Joystick
joystick_enabled = True
joystick_path = '/dev/input/js0'
joystick_roll_axis = 0
joystick_pitch_axis = 1
joystick_z_axis = 2

# Remote event system (eventbus gateway)
remoteevent_enabled = True
remoteevent_host = '0.0.0.0'
remoteevent_port = 9601

