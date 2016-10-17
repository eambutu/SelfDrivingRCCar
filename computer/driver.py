import serial

class Driver(object):
    def __init__(self):
        # Initialize connection to serial port
        # Blah blah parameters
        SERIAL_PORT = '/dev/tty0'
        BAUDRATE = 19200
        self.ser = serial.Serial(SERIAL_PORT, BAUDRATE)

    def up(self):
        print 'Write serial to drive up'
        self.ser.write('')

    def right(self):
        print 'Write serial to drive right'
        self.ser.write('')

    def back(self):
        print 'Write serial to drive back'
        self.ser.write('')

    def left(self):
        print 'Write serial to drive left'
        self.ser.write('')
