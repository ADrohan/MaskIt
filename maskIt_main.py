
# This program is the next and final itteration after 'maskIt_facedetect_smile.py'
# CHANGES:
# 1. Added bufferless video capture class
# 2. The video capture class now controls the camera capture (1 image) along with camera
# capture error checking, so previous capture error check, bufferzise and FPS
# settings have been removed
# 3. Additional comments have also been added

import pyfirmata2
import time
from time import sleep
import datetime
import numpy as np
import cv2
import storeFileFB
from captureClass import VideoCapture # captures bufferless video
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

# start all leds low i.e. off
LEDs = [greenLed, redLed, whiteLed]
LED_index = 0
for LED in LEDs:
    LED.write(0)

# loading classifiers
face_cascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
smile_cascade= cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_smile.xml')
#mouth_cascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_mcs_mouth.xml')

# Initialise pi camera.
cap = VideoCapture(-1) # Open video capture object with capture class instead
#cap = cv2.VideoCapture(-1)


### Face detection function ###
# Start reading the capture,
# Covert to grayscale for Detect MultiScale funtion to work and assign output
# of opencv's multiscale function to 'faces'
# A numpy array is returned which holds the rect x,y,w,h co-ordinated of faces
# Check the length of this array to determine if any face is detected.
# If no face is detected assign maskStatus to No
# If a face is detected load the smile classifier and check the length of this
# If the length is 0 no smile is detected so assign maskDetect to Yes
# Or if the length is >1, a smile is detected so assign maskStatus to No

# Possible outcomes: Return value for MaskStatus. Is mask on?
# Pir activated, face is detected, no smile(mouth) is detected: YES
# Pir activated, face is detected, smile(mouth) is detected: NO
# Pir activated, No face is detected so no smile(mouth) detected either: NO

def capture_image():
    image = cap.read()
    # ret, image = cap.read()
    print("capturing video")
    currentTime = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S') 
    print(currentTime)
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
    faces = face_cascade.detectMultiScale(grayImage, 1.1, 6 ) # detect faces
    maskStatus = 'No' # initialize mask status to no mask

    if (len(faces)) == 0: # if length of faces numpy array is 0 no faces detected
       maskStatus = 'No' # Pir activated, No face detected
       print("No faces detected")
       print("Mask Status: " + str(maskStatus))
    else:
        for (x,y,w,h) in faces:
            image = cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
            roi_grayImage = grayImage[y:y+h,x:x+w]
            roi_color = image[y:y+h, x:x+w]
            smile = smile_cascade.detectMultiScale(roi_grayImage, 1.7, 20 )
            # print("print smile co-ords ")
            # print(smile.shape)
            if(len(smile)) == 0: #  face detected but no smile detected
                maskStatus = 'Yes' # Pir activated, face detected, no smile
                print("face detected but no smile")
                print("Mask Status: " + str(maskStatus))
            else:
                for (sx,sy,sw,sh) in smile:
                    cv2.rectangle(roi_color, (sx,sy), (sx+sw,sy+sh), (255,0,0),1)
                    print("face and smile detected")
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

### Door Status Function ###
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



