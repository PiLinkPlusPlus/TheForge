#!/bin/sh
#Updatesuntime.sh
#run this at startup. Add the line below before openauto launch in file /etc/xdg/lxsession/LXDE-pi/autostart
#@/home/pi/Updatesuntime.sh
DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority python3 /home/pi/Updatesuntime.py &
