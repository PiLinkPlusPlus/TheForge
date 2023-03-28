#!/bin/bash
until (wmctrl -l | grep RaceCapture | grep -v grep > /dev/null)
do
sleep 1
done
sleep 1
# move RC window to perfered location
if tvservice -l | grep "HDMI 1" > /dev/null; then
wmctrl -r RaceCapture -e 0,1920,0,1280,720
else
wmctrl -r RaceCapture -b toggle,hidden
wmctrl -r RaceCapture -e 0,660,200,1230,700
fi