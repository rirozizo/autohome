import os, time
volt_cmd = "cat /sys/class/leds/led1/brightness"

from Adafruit_IO import MQTTClient
f=open("/home/pi/autohome/aiokey.txt", "r")
contents =f.read()
contents = contents.strip()
ADAFRUIT_IO_KEY = contents

ADAFRUIT_IO_USERNAME = 'rirozizo'

PIVOLT_FEED_ID = 'pi-volt'

def connected(client):
	pass

def disconnected(client):
	# Disconnected function will be called when the client disconnects.
	print('Disconnected from Adafruit IO!')
	sys.exit(1)

def message(client, feed_id, payload):
	print('Feed {0} received new value: {1}'.format(feed_id, payload))

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

client.on_connect	 = connected
client.on_disconnect = disconnected
client.on_message	 = message

client.connect()
client.loop_background()

while True:
	pivolt = str(os.popen(volt_cmd).read())
	pivolt = pivolt[:pivolt.rfind('\n')]
	client.publish(PIVOLT_FEED_ID, pivolt)
	time.sleep(10)
