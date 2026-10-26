#!/usr/bin/python3
import os
import time
from subprocess import Popen
import can

Popen(["sudo", "ip", "link", "set", "can0", "down", "type", "can"])
time.sleep(.5)

Popen(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate", "500000"])

can_interface = 'can0'
bus = can.interface.Bus(bustype='socketcan', channel=can_interface, bitrate=500000)

# Only accept the start/finish message: standard frame, ID 5
bus.set_filters([{"can_id": 5, "can_mask": 0x7FF, "extended": False}])

LAP_TRIGGER_ID = 5


def canrecv():
    try:
        msg = bus.recv()
        if msg is not None and msg.arbitration_id == LAP_TRIGGER_ID and not msg.is_extended_id:
            print("Lap trigger received on {}".format(bus.channel_info))
            StartFinish()
    except can.CanError:
        print("Message NOT received")


def CloseRelay1():
    Popen(["i2cset", "-y", "1", "0x10", "0x01", "0xFF"])
def CloseRelay2():
    Popen(["i2cset", "-y", "1", "0x10", "0x02", "0xFF"])
def CloseRelay3():
    Popen(["i2cset", "-y", "1", "0x10", "0x03", "0xFF"])
def CloseRelay4():
    Popen(["i2cset", "-y", "1", "0x10", "0x04", "0xFF"])
def OpenRelay1():
    Popen(["i2cset", "-y", "1", "0x10", "0x01", "0x00"])
def OpenRelay2():
    Popen(["i2cset", "-y", "1", "0x10", "0x02", "0x00"])
def OpenRelay3():
    Popen(["i2cset", "-y", "1", "0x10", "0x03", "0x00"])
def OpenRelay4():
    Popen(["i2cset", "-y", "1", "0x10", "0x04", "0x00"])


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
