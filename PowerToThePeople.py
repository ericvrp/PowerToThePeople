#!/usr/bin/env python

from requests import get
from requests.exceptions import Timeout, ConnectionError
from time import time, strftime, asctime
from subprocess import check_output
import RPi.GPIO as GPIO

try:
	from config import *
except ImportError:
	from defaults import *
	print 'Warning! copy defaults.py to config.py and edit that file!'


def waitForLedFlash():
	GPIO.wait_for_edge(ldr_gpio_pin, GPIO.RISING)
	GPIO.wait_for_edge(ldr_gpio_pin, GPIO.FALLING)	#poormens debounce


def	main():
	#simply connect ldr_gpio_pin to 5V because we use a pulldown resistor from software

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(ldr_gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	waitForLedFlash()	#Skip first led flash to get a proper duration for the first one we'll use

	lastPvOutputTime = lastLedFlashTime = time()	#first impression duration will be inaccurate
	nLedFlashes = 0

	while True:
		waitForLedFlash()

		now = time()
		current_usage = '%s : %4d Watt' % (asctime(), 3600 / (now - lastLedFlashTime))
		lastLedFlashTime = now
		nLedFlashes += 1

		print current_usage
		try:
			if webcache_enabled:
				get('http://127.0.0.1:8083/watt/' + current_usage, timeout=1.0)	#update webcache
		except Timeout:
			print 'Warning: webcache update failed'

		if pvoutput_interval and now >= lastPvOutputTime + pvoutput_interval:
			watt_average = nLedFlashes * 3600 / (now - lastPvOutputTime)
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
			lastPvOutputTime = now
			nLedFlashes = 0


if __name__ == '__main__':
	main()
	#GPIO.cleanup()
