#!/usr/bin/env python

import RPi.GPIO as GPIO
from requests import get
from time import time, sleep, strftime

try:
	from config import *
except ImportError:
	from defaults import *
	print 'Warning! copy defaults.py to config.py and edit that file!'

LDR_PIN              = 4	#LDR = Light Dependent Resistore
MAX_MEASUREMENTS     = 9000	#assume there is no led flashing with this little light
IMPRESSION_THRESHOLD = 0.9	#if measurements < MAX_MEASUREMENTS * IMPRESSION_THRESHOLD: then we assume led flashed
MAX_WATT             = 7500	#it's probably an measuring error if we're above
#IMPRESSIONS_PER_kWh  = 1000	#my electricity meter flashes a light this many times per kWh
PVOUTPUT_INTERVAL    = 300	#5 minutes between sending updates


def	RCtime():
	sleep(0.1)	#try to avoid detecting the same led flash twice

	# Discharge capacitor
	GPIO.setup(LDR_PIN, GPIO.OUT)
	GPIO.output(LDR_PIN, GPIO.LOW)
	sleep(0.1)

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

	lastPvOutputTime = time()
	lastLedFlashTime = time()	#first impression duration will be inaccurate
	watt = 0

	while True:
		nMeasurements, duration = RCtime()
		duration = int(duration * 100000.0) # Low values for much light
		now = time()

		if nMeasurements < MAX_MEASUREMENTS * IMPRESSION_THRESHOLD:
			impressionDuration = now - lastLedFlashTime
			lastWatt = watt
			watt = 3600 / impressionDuration
			lastLedFlashTime = now

			if watt > MAX_WATT:
				print 'Ignore %d Watt' % watt
				continue

			print 'Impression took %.1f seconds (%d Watt) [%d Watt change]' %\
				(impressionDuration, watt, watt - lastWatt)

			if now >= lastPvOutputTime + PVOUTPUT_INTERVAL:
				payload = {
					'key' : pvoutput_key,
					'sid' : pvoutput_sid,
					'd'   : strftime('%Y%m%d'),
					't'   : strftime('%H:%M'),
					'v4'  : watt
					}
				r = get('http://pvoutput.org/service/r2/addstatus.jsp', params=payload)
				#XXX post current power consumption for the moment
				lastPvOutputTime = now
				print 'Sent power consumption value to pvoutput.org (response %d)' % r.status_code

		#print '%4d measurements in %5d time units (%d Watt) [%d Watt change]' %\
		#	(nMeasurements, duration, watt, watt - lastWatt)

if __name__ == '__main__':
	main()

