



# This file is executed on every boot (including wake-boot from deepsleep)

#import esp

#esp.osdebug(None)

import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)

import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import esp
esp.osdebug(None)
import gc
import webrepl
import network
import uasyncio


#CONNECT TO MY NETWORK
sta_if = network.WLAN(network.STA_IF)

def connect_to_wifi():
  if not sta_if.isconnected():

    print('connecting to network...')

    sta_if.active(True)

    sta_if.connect('NETWORK SSID', 'NETWORK PASSWORD')

#    while not sta_if.isconnected():
#
#        pass
#        
connect_to_wifi()

print('network config:', sta_if.ifconfig())

ap_if = network.WLAN(network.AP_IF)

ap_if.active(False)



#MQTT WORK
mqtt_server = 'MQTT_SERVER'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'notification'
topic_pub = b'doorbell'

last_message = 0
message_interval = 5
counter = 0


#WEBREPL WORK
webrepl.start()

gc.collect()




