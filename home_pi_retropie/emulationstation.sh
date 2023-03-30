#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/games:/usr/games
#DISPLAY=:0.0 emulationstation

if [ -e /dev/input/js0 ] ; then
	DISPLAY=:0.0 emulationstation
else
	DISPLAY=:0.0 zenity --info --text="Game controller not detected\nTurn on the game controller and try again"  --title="Retropie launcher" --width=560 --height=20

fi