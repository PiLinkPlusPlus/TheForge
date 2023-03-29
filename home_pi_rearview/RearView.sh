!/bin/bash

#Start RearView with openapp button, exit and bring AutoApp back to foreground
DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority python3 /home/pi/RearView.py
DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool search --desktop 0 --name "autoapp" windowactivate
