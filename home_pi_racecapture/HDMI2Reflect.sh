#!/bin/bash
#reflect HDMI2
xrandr --output HDMI-2 --reflect x
xinput map-to-output 'wch.cn USB2IIC_CTP_CONTROL' HDMI-1

