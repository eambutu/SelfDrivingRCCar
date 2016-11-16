import struct
import serial
from sys import platform

class Driver(object):
    def __init__(self):
        # Initialize connection to serial port
        # Blah blah parameters
        if platform == 'linux' or platform == 'linux2':
            SERIAL_PORT = '/dev/tty0'
            BAUDRATE = 19200
        elif platform == 'darwin':
            SERIAL_PORT = '/dev/cu.usbmodem1421'
            BAUDRATE = 9600
        self.ser = serial.Serial(SERIAL_PORT, BAUDRATE)

    def up(self):
        print 'Write serial to drive up'
        self.ser.write('4')

    def right(self):
        print 'Write serial to drive right'
        self.ser.write('2')

    def back(self):
        print 'Write serial to drive back'
        self.ser.write('8')

    def left(self):
        print 'Write serial to drive left'
        self.ser.write('1')
    
    def write(self, keys):
        print 'Writing to serial:' + str(keys)
        self.ser.write(struct.pack('>B',keys))
