#!/bin/bash
#reflect normal HDMI2
xrandr --output HDMI-2 --reflect normal
xinput map-to-output 'wch.cn USB2IIC_CTP_CONTROL' HDMI-1
