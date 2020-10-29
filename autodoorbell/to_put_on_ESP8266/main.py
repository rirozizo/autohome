# Complete project details at https://RandomNerdTutorials.com
mqtt_connected = False
def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'notification' and msg == b'received':
    print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub, mqtt_connected
  time.sleep(5)
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  mqtt_connected = True
#  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker' % (mqtt_server))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
#  time.sleep(10)
#  machine.reset()

try:
  while mqtt_connected == False:
    print("not connected to MQTT Server")
    client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

  
#Relay Pin Setup (This is an active LOW relay so everything is kinda backwards
#We need to do the following steps exactly so that we prevent accidental activation while setting up
#Pin 5 in code relates to D1 IRL
#Pin 4 in code relates to D2 IRL
#Pin 0 in code relates to D3 IRL
relay_pin = machine.Pin(5, machine.Pin.OUT,value=1)

switch_pin = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
# Functions to run when the button is pressed.
def Input_1(channel):
        global mqtt_connected, client
        # Debouncing Code
        time.sleep(0.05)
        counter = 0
        while switch_pin.value() == 0 and counter != 3:
          counter += 1
        
        if switch_pin.value() == 0:
        # Put whatever the Button does in here
          relay_pin.off()
          print('DING!')
        ### DO WHATEVER HERE ###
        # make the telegram bot upload latest clip
        # don't repeat until upload is done (maybe make a "Busy" file to control this)
          time.sleep(0.3)
          relay_pin.on()
          print('DONG!')
          if sta_if.isconnected() and mqtt_connected == True:
            print('CONNECTED!!')
            client.publish(topic_pub, "DING")
          else:
            connect_to_wifi()
            connect_and_subscribe()
          time.sleep(1.7)

# Does a Callback to the appropriate Input function.
switch_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=Input_1) # Waiting for Doorbell to be pressed.

print("setup")
#while True:
  #Remember that off() activates the relay, and on() deactivates it
  #relay_pin.off()
  #print("off")
  #time.sleep(2)
  #relay_pin.on()
  #print("on")
  #time.sleep(2)
#  try:

#    client.check_msg()
#    if (time.time() - last_message) > message_interval:
#      msg = b'Hello #%d' % counter
#      client.publish(topic_pub, msg)
#      last_message = time.time()
#      counter += 1
#  except OSError as e:
#    restart_and_reconnect()
