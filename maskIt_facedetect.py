import pyfirmata2
import time
from time import sleep
import datetime
import numpy as np
import cv2

# Find port and create a new board
PORT =  pyfirmata2.Arduino.AUTODETECT
board = pyfirmata2.Arduino(PORT)
board.samplingOn() # default sampling interval of 19ms

# global variables
greenLed = board.get_pin('d:7:o') # Pin 7 is used for the green led set to outp$
redLed = board.get_pin('d:12:o') # Pin 12 is used for the red led set to output
whiteLed = board.get_pin('d:8:o') # Pin 8 is used for the red led set to output
servo = board.get_pin('d:9:s') # configure Pin 9 as a servo
pirSensor = board.get_pin('d:3:i') # Pin 2 is used for the red led set to input

pirSensor.enable_reporting()
read_value = 0 # initialise pir read value to 0
last_read_value = 0 # initialise previous pir value to 0
face_detect = 0

# start leds off
LEDs = [greenLed, redLed, whiteLed]
LED_index = 0
for LED in LEDs:
    LED.write(0)

# loading classifiers
face_cascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')

# initialise pi camera
cap = cv2.VideoCapture(-1) # open video capture object
print("camera initialized")

# Face detection function
def capture_image():
    ret, image = cap.read()
    print("capturing video")
    currentTime = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
    print(currentTime)
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayImage, 1.1, 5 )
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
    cv2.imshow('Image with faces',image)
    face_detect = len(faces)
    if face_detect >= 1:
        print("lenfaces is more than 1")
        fileLoc = "/home/pi/Images/image{}.jpg".format(currentTime)
        print(fileLoc)
        cv2.imwrite(fileLoc, image)
    elif face_detect == 0:
        print("lenfaces is 0")
    cv2.destroyAllWindows()
    print("printing face detect value from capture image: ")
    print(face_detect)
    return face_detect

# Function to determine if door opens or not.
# This funtion also controls turning off the white light
# and turning on the green or red light as an indicator to the customer
# that the door is opening (green light) or will remain closed (red light).
def door_status(face_detect):
    print("printing face detect values passed to door status:")
    print(face_detect)
    print("about to run door status")
    if face_detect == 0:
        whiteLed.write(0)
        greenLed.write(1)
        print('access granted')
        servo.write(120)
        sleep(5)
        greenLed.write(0)
        servo.write(0)
    elif face_detect >= 1:
        whiteLed.write(0)
        redLed.write(1)
        print('access denied')
        sleep(5)
        redLed.write(0)

# loop to read PIR sensor and only activate the capture_image() function
# based on a HIGH read value from the PIR sensor, as this means the sensor
# has been activated by a warm bodied being. The value returned from the
# capture_image function (face_detect) which returns the number of faces
# detected is then passed to the door_status function to determine whether
# to open the door or not.
while True:
    read_value = pirSensor.read()
    if read_value != last_read_value: # check for a change in PIR value
        if read_value == 1: # if IR sensor reads high
            whiteLed.write(1)
            print('pir sensor activated') 
            sleep(5)
            print("getting ready to run capture")
            # assign returned value from capture_image to returned_value
            returned_value = capture_image()
            print("printing returned value")
            print(returned_value) 
            print("geting ready to run door status")
            # pass the returned value for face_detect to door_status function
            door_status(returned_value)
            print("resetting PIR")
    last_read_value = read_value # set last read PIR value to read_value


