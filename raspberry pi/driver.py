##############################################################################################################
## AutoHome is a system that enables you to control any device at home using a Raspberry Pi, and AdafruitIO.##
## You can also integrate IFTTT with AdafruitIO so you can control everything using Google Assistant.	    ##
## You can find the project with README at github.com/rirozizo/AutoHome									    ##
##############################################################################################################

#Importing needed libraries
import sys
from Adafruit_IO import MQTTClient
import RPi.GPIO as GPIO

#library for time and sleep, might need later
#from time import sleep

#Dummy relay pin number (GPIO number and NOT physical pins)
ac_relay_pin = 26
GPIO.setmode(GPIO.BCM)

#Set GPIO pin to OUT
GPIO.setup(ac_relay_pin, GPIO.OUT)

#Give HIGH
#GPIO.output(ac_relay_pin, 1)

#Give LOW
#GPIO.output(ac_relay_pin, 0)

#Sleep for 5 seconds
#sleep(5)


# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!

# I used a separate file to read the key from. This is done so that we don't expose the key in the code itself, but a separatefile
f=open("/home/pi/autohome/aiokey.txt", "r")
contents =f.read()
contents = contents.strip()
#print(contents)
ADAFRUIT_IO_KEY = contents

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'rirozizo'

# Set the IDs of the feeds to subscribe to for updates.
MASTER_FEED_ID = 'master'
AC_FEED_ID = 'ac'
AC_STATUS_FEED_ID = 'ac-status'
SERVICE_STATUS_FEED_ID = 'service-status'

# Set the statuses of global variables
#This is to keep track of the Master switch so we can disable the control of everything in one switch
MASTER_DATA = 'OFF'
#This is to keep track of the last (old) value of the Master switch, so that we can apply the current feeds' data when we switch Master back on
OLD_MASTER_DATA = 'OFF'


# Define callback functions which will be called when certain events happen.
def connected(client):
	# Connected function will be called when the client is connected to Adafruit IO.
	# This is a good place to subscribe to feed changes.  The client parameter
	# passed to this function is the Adafruit IO MQTT client so you can make
	# calls against it easily.
	print('Connected to Adafruit IO!  Listening for {0} changes...'.format(AC_FEED_ID))
	# Subscribe to changes on the feed.
	client.subscribe(AC_FEED_ID)
	client.subscribe(MASTER_FEED_ID)
	# Get existing value from feed so we match the current user input
	client.receive(MASTER_FEED_ID)
	client.publish(SERVICE_STATUS_FEED_ID, "ON")


def disconnected(client):
	# Disconnected function will be called when the client disconnects.
	print('Disconnected from Adafruit IO!')
	sys.exit(1)




##############################################################################################################################

def message(client, feed_id, payload):
	# Message function will be called when a subscribed feed has a new value.
	# The feed_id parameter identifies the feed, and the payload parameter has
	# the new value.
	print('Feed {0} received new value: {1}'.format(feed_id, payload))
	# I'm a noob, this took a while to figure out, always add "global" before a variable if you intend on changing it
	global MASTER_DATA
	global OLD_MASER_DATA
	global MASTER_FEED_ID
	
	# If we modify the Master switch
	if feed_id == MASTER_FEED_ID:
		OLD_MASER_DATA = MASTER_DATA
		MASTER_DATA = payload
		# If master is switched from Off to On
		if MASTER_DATA == "ON":
			client.receive(AC_FEED_ID)
	
	##########################################
	#Do the next action if the payload is ON:#
	##########################################
	
	#If the received feed id is the one that belongs to the AC control, and the payload is ON
	if MASTER_DATA == "ON" and feed_id == AC_FEED_ID and payload == "ON":
		print('Turning AC ON')
		ac_control("ON")
		
	###########################################
	#Do the next action if the payload is OFF:#
	###########################################
	
	#If the received feed id is the one that belongs to the AC control, and the payload is OFF
	if MASTER_DATA == "ON" and feed_id == AC_FEED_ID and payload == "OFF":
		print('Turning AC OFF')
		ac_control("OFF")
	
	elif MASTER_DATA == "OFF":
		print('Master seems to be OFF, not doing anything')

##############################################################################################################################
		
def ac_control(control):
	if control == "ON":
		#Let AdaFruitIO know of the current status now
		print('Setting AC\'s status to ON')
		client.publish(AC_STATUS_FEED_ID, "ON")
		#It's counter intuitive to give 0 to the pin for ON, but the relay has a "low-is-on, high-is-off" logic.
		#So it switches on as soon as it gets powered if we don't do anything about it.
		GPIO.output(ac_relay_pin, 0)
	if control == "OFF":
		print('Setting AC\'s status to OFF')
		#Let AdaFruitIO know of the current status now
		client.publish(AC_STATUS_FEED_ID, "OFF")
		#It's counter intuitive to give 0 to the pin for ON, but the relay has a "low-is-on, high-is-off" logic.
		#So it switches on as soon as it gets powered if we don't do anything about it.
		GPIO.output(ac_relay_pin, 1)

##############################################################################################################################

# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect	 = connected
client.on_disconnect = disconnected
client.on_message	 = message

# Connect to the Adafruit IO server.
client.connect()

# Start a message loop that blocks forever waiting for MQTT messages to be
# received.	 Note there are other options for running the event loop like doing
# so in a background thread--see the mqtt_client.py example to learn more.
try:
	client.loop_blocking()
except:
	client.publish(SERVICE_STATUS_FEED_ID, "OFF")
	print('\nExited Successfully \n')
	GPIO.cleanup()
