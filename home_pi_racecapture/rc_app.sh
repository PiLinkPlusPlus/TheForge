#!/bin/bash

# new way - RaceCapture already running, just need to switch to it
#DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool search --desktop 0 --name "RaceCapture" windowactivate


  if (ps aux | grep race_capture | grep -v grep > /dev/null)
  then
DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool search --desktop 0 --name "RaceCapture" windowactivate

  else

DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority /home/pi/racecapture/run_racecapture.sh &
while [[ ! `DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority wmctrl -l|grep RaceCapture` ]] ; do
  true
done
DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool search --desktop 0 --name "RaceCapture" windowactivate

  fi
