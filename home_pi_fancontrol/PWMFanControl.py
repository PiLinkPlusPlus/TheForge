#!/usr/bin/env python3
# Author: Justin DuBois
import os
import time
from time import sleep
import signal
import sys
import RPi.GPIO as GPIO

fanPin = 18 # The pin ID
desiredTemp = 45 # The desired temperature in Celsius for the automatic function
fanSpeed=100
sum=0
pTemp=15
iTemp=0.4

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    temp =(res.replace("temp=","").replace("'C\n",""))
    #print("temp is {0}".format(temp)) #Uncomment here for testing
    return temp

def fanOFF():
    myPWM.ChangeDutyCycle(0)
    return()

def handleFan():
    global fanSpeed,sum
    actualTemp = float(getCPUtemperature())
    diff=actualTemp-desiredTemp
    sum=sum+diff
    pDiff=diff*pTemp
    iDiff=sum*iTemp
    # fanSpeed=pDiff+iDiff
    fanSpeed=fanSpeed+diff 
    if fanSpeed>100:
        fanSpeed=100
    if fanSpeed<15:
        fanSpeed=0
    if sum>100:
        sum=100
    if sum<-100:
        sum=-100
    #print("actualTemp %4.2f TempDiff %4.2f pDiff %4.2f iDiff %4.2f fanSpeed %5d" % (actualTemp,diff,pDiff,iDiff,fanSpeed))
    myPWM.ChangeDutyCycle(fanSpeed)
    return()

def setPin(mode): # A little redundant function but useful if you want to add logging
    GPIO.output(fanPin, mode)
    return()

try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(fanPin, GPIO.OUT)
    myPWM=GPIO.PWM(fanPin,20) # was (fanpin,15)
    myPWM.start(50)
    GPIO.setwarnings(False)
    fanOFF()
    while True:
        handleFan()
        sleep(5) # Read the temperature every x sec, increase or decrease this limit if you want
except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
    fanOFF()
    GPIO.cleanup() # resets all GPIO ports used by this program
