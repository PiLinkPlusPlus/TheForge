#!/usr/bin/python3
import os
import time #to enable sleep
from subprocess import Popen #to execute unix commands wout blocking
import can #to enable python-can

#sudo ip link set can0 down type can 
Popen(["sudo", "ip" ,"link" ,"set", "can0", "down", "type", "can"])
time.sleep(.5)

#sudo ip link set can0 up type can bitrate 500000
Popen(["sudo", "ip" ,"link" ,"set", "can0", "up", "type", "can", "bitrate", "500000"])

can_interface = 'can0'
# this uses the default configuration (for example from the config file)
# see https://python-can.readthedocs.io/en/stable/configuration.html
bus = can.interface.Bus(bustype='socketcan', channel=can_interface, bitrate=500000)
# Using specific buses works similar:
# bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
# bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=250000)
# bus = can.interface.Bus(bustype='ixxat', channel=0, bitrate=250000)
# bus = can.interface.Bus(bustype='vector', app_name='CANalyzer', channel=0, bitrate=250000)
# ...

def canrecv():

    try:
        bus.recv() #with no timeout, function blocks- waiting for any CAN signal
        print("Message recieved on {}".format(bus.channel_info))
        StartFinish()
    except can.CanError:
        print("Message NOT recieved")


def CloseRelay1():
    Popen(["i2cset", "-y" ,"1" ,"0x10", "0x01", "0xFF"])
def CloseRelay2():
    Popen(["i2cset", "-y" ,"1" ,"0x10", "0x02", "0xFF"])
def CloseRelay3():
    Popen(["i2cset", "-y" ,"1" ,"0x10", "0x03", "0xFF"])
def CloseRelay4():
    Popen(["i2cset", "-y" ,"1" ,"0x10", "0x04", "0xFF"])
def OpenRelay1():
    Popen(["i2cset", "-y" ,"1" ,"0x10", "0x01", "0x00"])
def OpenRelay2():
    Popen(["i2cset", "-y" ,"1" ,"0x10", "0x02", "0x00"])
def OpenRelay3():
    Popen(["i2cset", "-y" ,"1" ,"0x10", "0x03", "0x00"])
def OpenRelay4():
    Popen(["i2cset", "-y" ,"1" ,"0x10", "0x04", "0x00"])


def StartFinish():
    CloseRelay4()
    print("CloseRelay4")
    time.sleep(.5)
    OpenRelay4()
    print("OpenRelay4")

if __name__ == '__main__':
    while True:
        canrecv()
    print('end of program')
    
