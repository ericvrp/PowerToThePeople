#
# Copy this file to config.py and insert to correct values there!
#
ldr_gpio_pin      = 0

mongodb_url       = 'mongodb://<user>:<pass>@ds<num>.mongolab.com:57867/<database>'
mongodb_collectionPrefix = ''
mongodb_interval  = 0	#in seconds (or 0 to disable sample output) (current wattage updated every second)
mongodb_userId    = '<db.user._id>'

pvoutput_interval = 0	#in seconds (or 0 to disable pvoutput)
pvoutput_key      = '<your api key from pvoutput.org goes here>'
pvoutput_sid      = '<your system id goes here>'
