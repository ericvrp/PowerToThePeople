#!/usr/bin/env python

import serial
from requests import get
from time import time, strftime, asctime

try:
	from config import *
except ImportError:
	from defaults import *
	print 'Warning! copy defaults.py to config.py and edit that file!'

PVOUTPUT_INTERVAL = 300		#5 minutes between sending updates


def	main():
	ser = serial.Serial('/dev/ttyACM0', 9600)
	ser.flushInput()
	ser.readline()	#Skip first led flash to get a proper duration after this

	lastPvOutputTime = lastLedFlashTime = time()	#first impression duration will be inaccurate
	nLedFlashes = 0

	while True:
		s = ser.readline()
		#print 'Arduino: ', s,

		now = time()
		watt = 3600 / (now - lastLedFlashTime)
		lastLedFlashTime = now
		nLedFlashes += 1

		print '%s : %4d Watt' % (asctime(), watt)

		if now >= lastPvOutputTime + PVOUTPUT_INTERVAL: #XXX should post average power consumption
			watt_average = nLedFlashes * 3600 / (now - lastPvOutputTime)
		 	#print 'Watt Average %d' % watt_average
			payload = {
				'key' : pvoutput_key,
				'sid' : pvoutput_sid,
				'd'   : strftime('%Y%m%d'),
				't'   : strftime('%H:%M'),
				'v4'  : watt_average
				}
			r = get('http://pvoutput.org/service/r2/addstatus.jsp', params=payload)
			lastPvOutputTime = now
			nLedFlashes = 0


if __name__ == '__main__':
	main()

