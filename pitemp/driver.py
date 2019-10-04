import os, time
temp_cmd = "vcgencmd measure_temp"
clock_cmd = "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"

from Adafruit_IO import MQTTClient
f=open("/home/pi/autohome/aiokey.txt", "r")
contents =f.read()
contents = contents.strip()
ADAFRUIT_IO_KEY = contents

ADAFRUIT_IO_USERNAME = 'rirozizo'

PITEMP_FEED_ID = 'pi-temp'
PICLOCK_FEED_ID = 'pi-clock'

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
	pitemp = str(os.popen(temp_cmd).read())
	pitemp = pitemp.split("\n")
	pitemp = pitemp[0]
	pitemp = pitemp[5:]
	pitemp = pitemp[:-2]
	piclock = str(os.popen(clock_cmd).read())
	piclock = piclock[:-4]
	client.publish(PITEMP_FEED_ID, pitemp)
	client.publish(PICLOCK_FEED_ID, piclock)
	time.sleep(10)
