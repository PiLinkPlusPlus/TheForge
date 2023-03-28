#!/bin/bash

DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority python3 /home/pi/DashControl_v2.7.py &
DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority python3 /home/pi/rc_lap_trigger.py &
while [[ ! `DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority wmctrl -l|grep DashControl` ]] ; do
  true
done
DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool search --desktop 0 --name "DashControl" windowminimize
