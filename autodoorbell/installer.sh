#!/bin/bash
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi
echo "Make sure all the files are in /home/pi/autodoorbell/ (Including this installer)"
echo "DON\'T FORGET TO PUT YOUR TELEGRAM TOKEN in token.txt!!!"
echo "Installing telepot python package"
pip3 install telepot
echo "Installing Rpi.GPIO python package"
pip3 install RPi.GPIO
echo "Installing motion"
apt-get install motion
echo "Configuring motion"
mkdir /home/pi/motion/
cp /home/pi/autodoorbell/motion.conf /etc/motion/motion.conf
#echo "Adding autodoorbell service to your system"
#cp /home/pi/autohome/autohome.service /etc/systemd/system/
#echo "Reloading systemctl daemon"
#systemctl daemon-reload
#echo "Starting service"
#systemctl start autohome
#echo "Enabling service on boot"
#systemctl enable autohome
#echo "Done! To start and stop the service, run \"service autohome start\" as root :D"
echo "To edit this program, you can modify the driver.py file in this directory"
echo "DON\'T FORGET TO PUT YOUR TELEGRAM TOKEN in token.txt!!!"
