import pyfirmata2
import time

# Find port and create a new board
PORT =  pyfirmata2.Arduino.AUTODETECT
board = pyfirmata2.Arduino(PORT)
board.samplingOn() # default sampling interval of 19ms

# global variables
greenLed = board.get_pin('d:7:o') # Pin 7 is used for the green led set to output
redLed = board.get_pin('d:12:o') # Pin 12 is used for the red led set to output
whiteLed = board.get_pin('d:8:o') # Pin 8 is used for the red led set to output
servo = board.get_pin('d:9:s') # configure Pin 9 as a servo


LEDs = [greenLed, redLed, whiteLed]
LED_index = 0

pirSensor = board.get_pin('d:3:i') # Pin 2 is used for the red led set to input
pirSensor.enable_reporting()
read_value = 0 # initialise pir read value to 0
last_read_value = 0 # initialise previous pir value to 0


for LED in LEDs:
    LED.write(0)

def door_status(face_detect):
    print("running  door status")
    if face_detect == 1:
        whiteLed.write(0)
        greenLed.write(1)
        print('access granted')
        servo.write(120)
        time.sleep(5)
        greenLed.write(0)
        servo.write(0)
    elif face_detect == 0:
        whiteLed.write(0)
        redLed.write(1)
        print('access denied')
        time.sleep(5)
        redLed.write(0)

if __name__ == "__main__":
    while True:
        read_value = pirSensor.read()
        print('reading pir')
        if read_value != last_read_value:
            if read_value == 1:
                whiteLed.write(1)
                print('pir sensor activated') 
                time.sleep(5)
                door_status(1) # hard coded for testing
        last_read_value = read_value
