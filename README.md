# MaskIt

## Domain specific solution - Healthcare
Since Covid-19 the way we physically interact with each other has changed. Covid 19 has brought a lot of uncertainty for humanity and this pandemic may well be with us for some time yet. The wearing of masks is ubiquitous. Although mandated, it cannot be enforced by store owners. While most people comply with the healthcare advice, there are those who still choose to ignore this advice. I have encountered this situation at first hand in my local supermarket. With retail outlets in mind, I would like to create an IoT solution that will only allow entry to their premises based on the mandatory condition that a customer is wearing a mask. 

## General Concept
A customer’s physical approach to the retail premises will activate a PIR motion sensor. Once this sensor is activated, a security light will also turn on providing an increase to the ambient light for the Pi camera (which will constantly be active) to work effectively. I plan to use Open CV’s Haar feature-based Cascade Classifiers to determine if the person present is wearing a mask or not. If it’s determined the customer is wearing a mask, this confirmation data will then be sent to the Iot platform ThingSpeak. The door lock  mechanism (using a servo motor to represent this) will be triggered from ThingSpeak’s talkback app and the door will open. A React, will send daily compliance updates to the owner of the store. This data also acts as a customer counter for the store and having this data could allow for further data extrapolation in combination with the purchase information which would give the owner information on the number of people entering the store versus the number of people who purchase in store.

## Face Detection
I have read that > masks have been confounding traditional facial recognition software > *(https://www.nationalgeographic.com/science/2020/09/face-mask-recognition-has-arrived-for-coronavirus-better-or-worse-cvd/)* Although facial recognition doesn’t appeal to me I am interested to see if the same applies to more general face detection models. I have yet to try this out but non-detection by the face classifiers and detection with the PIR sensor could in effect determine there is a person present and their face isn’t visible so their face must be covered. If face detection does work with masks the second option would be to use frontal face detection and mouth detection together to determine If a person is wearing a mask.

## Physical Hardware:
Raspberry Pi3 model B+, Raspberry Pi Camera Module V2, GPIO Breakout Board & Ribbon Cable for Raspberry Pi, Passive Infrared (PIR) sensor, servo motor, LEDs, Jumper Wires: Male to Male for the breakout board and 3 x Male to Female for the PIR Sensor

## Proposed IoT Platforms and Communication:
IoT Platform: Thingspeak, IFTTT, HTTP Protocols
Python, JSON,
Computer vision tools like Open CV, IMUtils (convenience functions to expedite Open CV on Raspberry Pi)

##--------------------------------------------------------------------------

# Working the project:

## Program files required from this repo
standardFirmata.ino
maskIt_main.py
storeFileFB.py
captureClass.py

## Communication between Arduino and Raspberry Pi
I decided to assign the computing intensive tasks to the Raspberry Pi and the sensor controlling tasks to an Arduino and use PiFirmata protocol for communication with the microcontroller

## Set Up Instructions
Opencv Software Installation:
After a few unsuccessful attempts I found these links to be the most accurate and helpful 

## Installation on the Pi3
https://towardsdatascience.com/installing-opencv-3-4-3-on-raspberry-pi-3-model-b-e9af08a9f1d9

## Installation on the Pi4
https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/

## Install PyFirmata2 on Raspberry Pi 4
https://github.com/berndporr/pyFirmata2

## Install Arduino IDE
https://www.arduino.cc/en/software
In the Arduino IDE upload the Standard Firmata sketch to the Arduino Uno board
accessible from File > Examples > Firmata > StandardFirmata
The StandardFirmata.ino file should be uploaded to the Arduino board. 

## Servo Motor
https://learn.sparkfun.com/tutorials/hobby-servo-tutorial/all?print=1
It is always recommended to use an external power supply for servo motors.
A Female DC Power adapter 2.1mm jack to screw terminal block and a 4xAA (6v) battery pack soldered together works. 
Refer to the 'maskIt_documentation.pdf' file in this repo for further information and photo documentation.

## Pi Camera Documentation
https://www.raspberrypi.org/documentation/hardware/camera/

## Open Cv documentation - Face Detection using Hair Cascades
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html

## Face detection Issues
Refer to the 'maskIt_documentation.pdf' file in this repo for further information.

## Bufferless Capture
Captured video is first stored in a buffer.When I first start the camera, the buffer is accumulated so reading from the buffer always gives me the old frames.
Setting the buffer size to 1 (value must be between 1 and 10) and fps to 1 helped but didn't solve the issue.
I found a link online which suggests having a separate thread to clear the buffer.
The frame reader thread is encapsulated inside the custom VideoCapture class and communication with the main thread is via a queue. 
This worked for me perfectly so thank you to the author of this code.
https://stackoverflow.com/questions/43665208/how-to-get-the-latest-frame-from-capture-device-camera-in-opencv

## Limitations of PIR Sensor
The nature of PIR sensors mean they will be activated not only by people but any warm bodied creatures, like cats, dog etc. To eliminate the possibility of false detections by non-humans, the default wide angle view of the PIR should be confined to eliminate detections below the average height of a dog. I used some old plumbers pipe to test this, fitting it snugly over the PIR). Using this shielded PIR in addition to positioning the PIR at a height to bypass being activated by small animals worked as a quick hack for this.
