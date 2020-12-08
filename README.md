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
