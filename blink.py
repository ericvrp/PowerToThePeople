#!/usr/bin/env python

import RPi.GPIO as GPIO
import time 


PIN = 4
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
print "Setup pin", PIN
GPIO.setup(PIN, GPIO.OUT)

while True:
  print "Set output false"
  GPIO.output(PIN, False)
  time.sleep(1.0)
 
  print "Set output true"
  GPIO.output(PIN, True)
  time.sleep(0.5)
