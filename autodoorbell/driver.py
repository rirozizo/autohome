#!/usr/bin/env python

### IMPORTS ###
import os # Allows us to run a program
from time import sleep  # Allows us to call the sleep function to slow down our loop
import botdriver
import paho.mqtt.client as mqtt

import subprocess as sp
import os
tmp = os.popen('sh /home/pi/autodoorbell/kill_motion.sh').read()
tmp = os.popen('sh /home/pi/autodoorbell/start_motion.sh').read()



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

### BUTTON PRESS DETECTION DEPRECATED! WE'RE NOW USING A SEPARATE ESP8266 BOARD FOR THIS###
# Set input pin to use the internal pull down
#GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# Our test relay is the same as the AC Relay for now
#GPIO.setup(13, GPIO.OUT)


def on_connect(mqttclient, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        #On ESP's side we set the Topic to "doorbell"
        mqttclient.subscribe("doorbell")

def on_message(mqttclient, userdata, msg):
        #If the ESP8266 send a "DING", which is when someone rings the doorbell
        if msg.payload.decode() == "DING":
                print("DING!")
                ### DO WHATEVER HERE ###
                tmp = os.popen('sh /home/pi/autodoorbell/snap.sh').read()
                sleep(0.3)
                botdriver.send()

mqttclient = mqtt.Client()
mqttclient.connect('localhost',1883,5)

mqttclient.on_connect = on_connect
mqttclient.on_message = on_message


try:
	print('loop')
	mqttclient.loop_forever()

except KeyboardInterrupt:
	tmp = os.popen('sh /home/pi/autodoorbell/kill_motion.sh').read()
