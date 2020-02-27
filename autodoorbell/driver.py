#!/usr/bin/env python

### IMPORTS ###
import os # Allows us to run a program
from time import sleep  # Allows us to call the sleep function to slow down our loop
import RPi.GPIO as GPIO # Allows us to call our GPIO pins and names it just GPIO
import botdriver
GPIO.setmode(GPIO.BCM)  # Set's GPIO pins to BCM GPIO numbering

import subprocess as sp
import os
tmp = os.popen('sh kill_motion.sh').read()
tmp = os.popen('sh start_motion.sh').read()



### TEXT COLORS ###
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

### BUTTON PRESS DETECTION ###
# Set input pin to use the internal pull down
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Our test relay is the same as the AC Relay for now
GPIO.setup(13, GPIO.OUT)


# Functions to run when the button is pressed.
def Input_1(channel):
	# Put whatever the Button does in here
	GPIO.output(13, 1)
	print(bcolors.OKGREEN + 'DING!' + bcolors.ENDC)
	print(bcolors.FAIL + 'DONG!' + bcolors.ENDC)
	### DO WHATEVER HERE ###
	# make the telegram bot upload latest clip
	# don't repeat until upload is done (maybe make a "Busy" file to contrl this)
	sleep(0.3)
	GPIO.output(13, 0)
	tmp = os.popen('sh snap.sh').read()
	sleep(0.3)
	botdriver.send()

# Does a Callback to the appropriate Input function.  Also debounces to prevent clicking the button multiple times a second.
GPIO.add_event_detect(16, GPIO.RISING, callback=Input_1, bouncetime=2000) # Waiting for Button 1 to be pressed.

# Starts a neverending loop otherwise the script will just quit.
try:
	while True:
		print("Waiting for input.") # Insert Random Loop Junk


		sleep(60);		   # Sleeps for a minute to save CPU cycles.  Any interrupt will break this.

except KeyboardInterrupt:
	tmp = os.popen('sh kill_motion.sh').read()
#	GPIO.cleanup()
GPIO.cleanup()
