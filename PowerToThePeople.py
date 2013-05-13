#!/usr/bin/env python

import serial
from requests import get
from requests.exceptions import Timeout, ConnectionError
from time import time, strftime, asctime
from sys import stdout
from subprocess import check_output

try:
	from config import *
except ImportError:
	from defaults import *
	print 'Warning! copy defaults.py to config.py and edit that file!'

PVOUTPUT_INTERVAL = 300		#5 minutes between sending updates


def	main():
	usbDevice = check_output('ls /dev/ttyACM*', shell=True).strip()
	ser = serial.Serial(usbDevice, 115200)
	ser.flushInput()
	ser.readline()	#Skip first led flash to get a proper duration after this

	lastPvOutputTime = lastLedFlashTime = time()	#first impression duration will be inaccurate
	nLedFlashes = 0

	while True:
		s = ser.readline()
		#print 'Arduino: ', s,

		now = time()
		current_usage = '%s : %4d Watt' % (asctime(), 3600 / (now - lastLedFlashTime))
		lastLedFlashTime = now
		nLedFlashes += 1

		print current_usage
		try:
			r = get('http://127.0.0.1:8083/watt/' + current_usage, timeout=1.0)	#update webcache
		except Timeout:
			print 'Warning: webcache update failed'

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
			try:
				r = get('http://pvoutput.org/service/r2/addstatus.jsp', params=payload, timeout=5.0)
			except ConnectionError:
				print 'Warning: pvoutput update failed'
			lastPvOutputTime = now
			nLedFlashes = 0

		stdout.flush()


if __name__ == '__main__':
	main()

