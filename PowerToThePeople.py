#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import time, sleep


# pvoutput.org-support3

LDR_PIN              = 4	#LDR = Light Dependent Resistore
MAX_MEASUREMENTS     = 9000	#assume there is no led flashing with this little light
IMPRESSION_THRESHOLD = 0.9	#if measurements < MAX_MEASUREMENTS * IMPRESSION_THRESHOLD: then we assume led flashed
IMPRESSIONS_PER_kWh  = 1000	#my electricity meter flashes a light this many times per kWh


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

	lastLedFlashTime = time()	#first impression duration will be inaccurate
	watt = 0

	while True:
		nMeasurements, duration = RCtime()
		duration = int(duration * 100000.0) # Low values for much light

		if nMeasurements < MAX_MEASUREMENTS * IMPRESSION_THRESHOLD:
			t = time()
			impressionDuration = t - lastLedFlashTime
			lastWatt = watt
			watt = 3600 / impressionDuration
			lastLedFlashTime = t
			print 'Impression took %.1f seconds (%d Watt) [%d Watt change]' %\
				(impressionDuration, watt, watt - lastWatt)

		#print '%4d measurements in %5d time units (%d Watt) [%d Watt change]' %\
		#	(nMeasurements, duration, watt, watt - lastWatt)

if __name__ == '__main__':
	main()

