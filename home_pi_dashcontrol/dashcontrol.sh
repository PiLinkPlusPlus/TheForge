#!/bin/bash
# new way - DashControl already running, just need to switch to it
#DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool search --desktop 0 --name "DashControl" windowactivate

  if (ps aux | grep DashControl_v2.7.py | grep -v grep > /dev/null)
  then
DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool search --desktop 0 --name "DashControl" windowactivate

  else

DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority python3 /home/pi/DashControl_v2.7.py &
while [[ ! `DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority wmctrl -l|grep DashControl` ]] ; do
  true
done
DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool search --desktop 0 --name "DashControl" windowactivate

  fi
