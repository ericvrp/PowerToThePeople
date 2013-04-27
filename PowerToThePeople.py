#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import time, sleep


LDR_PIN             = 4		#LDR = Light Dependent Resistore
MAX_MEASUREMENTS    = 1999	#assume there is no led flashing with this little light
IMPRESSIONS_PER_kWh = 1000	#my electricity meter flashes a light this many times per kWh


def	RCtime():
	# Discharge capacitor
	GPIO.setup(LDR_PIN, GPIO.OUT)
	GPIO.output(LDR_PIN, GPIO.LOW)
	sleep(0.1)	#XXX Do we really need this?

	GPIO.setup(LDR_PIN, GPIO.IN)
	nMeasurements, start = 0, time()
	#Wait until voltage across capacitor reads high on GPIO
	while nMeasurements < MAX_MEASUREMENTS and GPIO.input(LDR_PIN) == GPIO.LOW:
		nMeasurements += 1

	duration = time() - start
	return nMeasurements, duration


def	main():
	GPIO.setwarnings(False)	#shut up!
	GPIO.setmode(GPIO.BCM)	#use Broadcom GPIO references (instead of board references)

	while True:
		nMeasurements, duration = RCtime()
		duration = int(duration * 100000.0) # Low values for much light
		print '%4d measurements in %4d time units' % (nMeasurements, duration)

if __name__ == '__main__':
	main()
