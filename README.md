PowerToThePeople
----------------

Use the flashing led of my electricity meter to compute my power consumption. Show this info on pvoutput.org.
The Raspberry Pi doesn't have an analog input so we will be using an Arduino for reading the Light Dependant Resistor (LDR). The two boards are communicating over usb.

Install dependencies: sudo apt-get install python-requests python-serial

Usage: ./PowerToThePeople.py
