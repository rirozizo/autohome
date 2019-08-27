# AutoHome
A System to control any Home Equipment via a Raspberry Pi

I will create a video guide explaining everything as soon as I get the project working :D Keep watch on my [YouTube Channel](https://youtube.com/rirozizo)

## The basic idea
The idea behind this project is to find a way to remotely control any possible home appliances without the use of proprietary hardware and apps. We use a Raspberry Pi connected to relays to control the power to the appliances, we use Google Assistant to send it commands at will, or any app that can communicate with MQTT, and we use AdaFruitIO as the middle man behind everything.

I'm going to create this project step by step and add new features and guides on how to use them as I go along. Right now the idea behind all of this is to just turn my bedroom AC on from anywhere in the world. Later on, I'm going to try and control my powered window blinds, then make it fully automated with a temperature sensor inside the room, then possibly going as far as making a Nest Hello clone on the Raspberry Pi, with a custom app and everything. But let's start with the basics, I just want to turn my AC on.

You tell Google Assistant to turn your AC on, the assistant sends that command to IFTTT, IFTTT routes it to AdaFruitIO, AdaFruitIO broadcasts this new change in its data, the Raspberry Pi picks up this new data and turns the Relay on to power on the AC.

A more basic way of doing things is to just find any way to send the data to AdaFruitIO, either by opening their site and manually hitting the ON/OFF toggle, or by using an app that talks to AdaFruitIO via MQTT, or using something fancy like Google Assistant :D

## Requirements
### Hardware
* A Raspberry Pi (I use an RPi 4, but you can use a 3)
* Some female-to-female jumper cables
* A breadboard to hold everything together
* A relay, I used a 4 Channel relay for this project
### Software
* Some knowledge on how to setup Raspbian OS
* A bit of Python code knowledge to edit the script to work with your specific case
* Patience and Caution! Working with high voltages might lead to injuries!

## Hardware Guide
### On the Raspberry Pi
This section will contain everything you need to know to plug your Raspberry Pi to the relay
### Breadboard
This section will contain everything you need to know to wire everything up from the Raspberry Pi to the relay
### Relay
This section will contain everything you need to know to properly setup the wires on the relay
## Software Guide
### AdafruitIO
* Create an AdaFruit IO Account [HERE](https://accounts.adafruit.com/)
* Go to [io.adafruit.com](io.adafruit.com)
* Create a new Dashboard. I chose to call it "Home Automation", you can call it whatever you want because this won't be related to any code.
* Create a new Block
* Select Toggle
* In the "Choose feed" screen, create a new feed and call it something you'll use in your code. I chose AC because I want to control my Air Conditioner
* Name your block anything you want and hit create at the bottom right. By default, the text to turn the toggle on would be "ON", and "OFF" would turn the toggle off.
* Click on "AIO Key" and save the long randomly generated key in the file /raspberry pi/aiokey.txt  We will use this later on in the script to communicate with AdaFruitIO
### IFTTT (Optional)
* Create an IFTTT Account [HERE](https://ifttt.com/)
* Click on your profile, then click Create
* Click on the word "This"
* Search for "Google Assistant" and choose that
* Choose "Say a simple phrase"
* Customize what you would want to say to trigger the toggle in AdaFruitIO. I chose "Turn bedroom AC On" and made it reply "Bedroom AC has been turned on"
* Click on the word "That"
* Choose "Send data to Adafruit IO"
* Choose your feed name
* Input the data you want to send to AdaFruit's feed. I chose "ON" as data

Now you can turn your device On via the Google Assistant

* Click on your profile, then click Create
* Click on the word "This"
* Search for "Google Assistant" and choose that
* Choose "Say a simple phrase"
* Customize what you would want to say to trigger the toggle in AdaFruitIO. I chose "Turn bedroom AC Off" and made it reply "Bedroom AC has been turned off"
* Click on the word "That"
* Choose "Send data to Adafruit IO"
* Choose your feed name
* Input the data you want to send to AdaFruit's feed. I chose "OFF" as data

Now IFTTT communicates with AdaFruitIO via your commands sent to Google Assistant :)
### Raspberry Pi
This section will contain everything you need to know to program the Raspberry Pi to work with AdaFruit and the Relay so we can achieve what we want to do
