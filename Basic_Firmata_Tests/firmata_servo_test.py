import pyfirmata2
import time

# Find port and create a new board
PORT =  pyfirmata2.Arduino.AUTODETECT
board = pyfirmata2.Arduino(PORT)
board.samplingOn() # default sampling interval of 19ms

servo = board.get_pin('d:9:s') # configure Pin 9 as a servo
print('Setup ok')
servo.write(0) # set servo position 0-255
time.sleep(1)
servo.write(120)


