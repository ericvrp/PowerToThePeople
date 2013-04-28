PowerToThePeople
----------------

Use the flashing led of my electricity meter to compute my power consumption. Show this info on pvoutput.org.

Schematics: http://learn.adafruit.com/basic-resistor-sensor-reading-on-raspberry-pi/basic-photocell-reading
   (attach to GPIO port 4 (pin 7) instead of 18
   
Install dependencies: sudo apt-get install python-rpi.gpio python-requests

Usage: sudo ./PowerToThePeople.py
