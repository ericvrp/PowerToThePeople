#!/usr/bin/env python

from requests import get
from requests.exceptions import Timeout, ConnectionError
from time import time, strftime, asctime, sleep
from sys import stdout
from exceptions import KeyboardInterrupt
from subprocess import check_output
import RPi.GPIO as GPIO
import pymongo  #http://api.mongodb.org/python/current/tutorial.html


try:
	from config import *
except ImportError:
	from defaults import *
	print 'Warning! copy defaults.py to config.py and edit that file!'


def _waitForLedFlash():
	while GPIO.input(ldr_gpio_pin) == GPIO.LOW:	#Wait for a pin rising
		sleep(0.01) #minimal sleep
	sleep(0.25)	#debounce sleep
	while GPIO.input(ldr_gpio_pin) == GPIO.HIGH:	#Make really really sure we get a LOW here
		sleep(0.01) #minimal sleep


def	main():
	connection = pymongo.Connection(mongodb_uri)
	Wattage = connection.mongolab001db.Wattage
	CurrentWattage = connection.mongolab001db.CurrentWattage

	#simply connect ldr_gpio_pin to 3.3V because we use a pulldown resistor from software

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(ldr_gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	_waitForLedFlash()	#Skip first led flash to get a proper duration for the first one we'll use

	lastWattDataTime = lastPvOutputTime = lastLedFlashTime = time()	#first impression duration will be inaccurate
	nLedFlashes = 0
	watt_data = []

	while True:
		_waitForLedFlash()

		now   = time()
		nowJS = int(now * 1000)	#milliseconds. As in Javascript 'new Date().getTime()'
		watt  = int(3600 / (now - lastLedFlashTime))
		current_usage = '%s : %4d Watt' % (asctime(), watt)
		lastLedFlashTime = now
		nLedFlashes += 1

		print current_usage

		CurrentWattage.update({'userId' : mongodb_userId}, {
			'userId'    : mongodb_userId,		#UNIQUE INDEX
			'createdAt' : nowJS, 
			'watt'      : watt},
			upsert = True)

		watt_data.append(watt)
		if mongodb_interval and now >= lastWattDataTime + mongodb_interval:
			interval    = now - lastWattDataTime
			averageWatt = float(sum(watt_data)) / len(watt_data)
			Wattage.insert({
				'userId'      : mongodb_userId,				#INDEX
				'createdAt'   : nowJS,
				'interval'    : interval,				#in seconds
				'kWh'         : averageWatt * interval / 3600 / 1000,	#/ 1000 converts Wh -> kWH 
				'averageWatt' : averageWatt,				#during interval (power used)
				'watt'        : watt_data})
			lastWattDataTime = now
			watt_data = []

		if pvoutput_interval and now >= lastPvOutputTime + pvoutput_interval:
			interval     = now - lastPvOutputTime
			watt_average = nLedFlashes * 3600 / interval
		 	#print 'Watt Average %d' % watt_average
			payload = {
				'key' : pvoutput_key,
				'sid' : pvoutput_sid,
				'd'   : strftime('%Y%m%d'),
				't'   : strftime('%H:%M'),
				'v4'  : watt_average
				}
			try:
				get('http://pvoutput.org/service/r2/addstatus.jsp', params=payload, timeout=5.0)
			except ConnectionError:
				print 'Warning: pvoutput update failed'
			except Timeout:
				print 'Warning: pvoutput timed out'
			lastPvOutputTime = now
			nLedFlashes = 0

		stdout.flush()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print 'Interrupted by user'
	GPIO.cleanup()

