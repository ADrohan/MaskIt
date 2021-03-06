# This program is the next itteration after 'maskIt_firebase.py'
# CHANGES:
# 1. Added smile cascade in place of a mouch cascade to test my initial idea
# while I'm still looking for a working mouth cascade trained classifier
# 2. Added camera capture error check on start up
# 3. Limited Frame Buffer size and Frames per second capture to the value of 1
# 4. Amended face detection function to return a maskStatus Value instead of
# face_detect, based on the calculations in the face detect function.

import pyfirmata2
import time
from time import sleep
import datetime
import numpy as np
import cv2
import storeFileFB
#import json

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
frame = 0

# start all leds low i.e.off
LEDs = [greenLed, redLed, whiteLed]
LED_index = 0
for LED in LEDs:
    LED.write(0)

# loading classifiers used for face detection
face_cascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
smile_cascade= cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_smile.xml')


# Initialise pi camera. Check the camera is working. Exit and inform 
# me if the camera is not working.
cap = cv2.VideoCapture(-1) # open video capture object
if cap is None:
    sys.exit("Camera Could not be opened")
else:
    print("camera initialized")


# Set the buffersize to 1 and the framerate to 1 frame per second
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) # Only hold one image in the buffer
cap.set(cv2.CAP_PROP_FPS, 1) #  set the framerate at 1 Frame per second


# Face detection function
def capture_image():
    ret, image = cap.read()
    print("capturing video")
    currentTime = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S') 
    print(currentTime)
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayImage, 1.1, 6 )
    maskStatus = 'No'

    if (len(faces)) == 0:
        maskStatus = 'No' # Pir activated, No face detected
        print("Mask Status: " + str(maskStatus))
    else:
        for (x,y,w,h) in faces:
            image = cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
            roi_grayImage = grayImage[y:y+h,x:x+w]
            roi_color = image[y:y+h, x:x+w]
            smile = smile_cascade.detectMultiScale(roi_grayImage, 1.1, 6 )
            if(len(smile)) == 0:
                maskStatus = 'Yes' # Pir activated, face detected, no smile
                print("Mask Status: " + str(maskStatus))
            else:
                for (sx,sy,sw,sh) in smile:
                    cv2.rectangle(roi_color, (sx,sy), (sx+sw,sy+sh), (255,0,0),1)
                    if((y<sy) and (sy<(y+h))):
                       maskStatus = 'No' # Pir activated, face & smile detected
                       print("Mask Status: " + str(maskStatus))

    cv2.imshow('Image with faces',image)
    face_detect = len(faces)
    print("frame number is: " + str(frame))
    fileLoc = "/home/pi/Images/image{}.jpg".format(frame)
    #print(fileLoc)
    img_flip = cv2.flip(image, 1) # flip image horizontally on y axis before saving
    cv2.imwrite(fileLoc, img_flip)
    storeFileFB.store_file(fileLoc)
    storeFileFB.push_db(fileLoc, currentTime, face_detect, maskStatus)
    cv2.destroyAllWindows()
    print("Number of faces detected: " + str(face_detect))
    print("Mask Status being returned: " + str(maskStatus))
   # return face_detect
    return str(maskStatus)


# Function to determine if door opens or not.
# This funtion also controls turning off the white light
# and turning on the green or red light as an indicator to the customer
# that the door is opening (green light) or will remain closed (red light).

def door_status(face_detect):
    print("printing face detect values passed to door status:")
    print(face_detect)
    print("about to run door status")
    if face_detect == 'Yes':
        whiteLed.write(0)
        greenLed.write(1)
        print('access granted')
        servo.write(120)
        sleep(5)
        greenLed.write(0)
        servo.write(0)
    elif face_detect == 'No':
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
            frame += 1
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
