import tkinter as tk
import os
import pygame
pygame.mixer.init()
from datetime import datetime
from subprocess import Popen #to execute unix commands wout blocking
root = tk.Tk()
root.title('DashControl')
pygame.mixer.music.load("./DashControl/Tink.wav")

P = 0
ox = 0
oy = -40
#-- search in OAP system file for sunrise and sunset values --
with open("/home/pi/.openauto/config/openauto_system.ini", 'r',encoding = 'utf-8') as f:
    for line in f:
        keyword = 'SunriseTime'
        if line.startswith(keyword):
            try:
                sunrise = (line.split('=')[1].rstrip())
            except:
                print ("Error finding SunriseTime in openauto_system.ini")

        keyword = 'SunsetTime'
        if line.startswith(keyword):
            try:
                sunset = (line.split('=')[1].rstrip())
            except:
                print ("Error reading SunsetTime in openauto_system.ini")

def TimeCheck():
    night = "./DashControl/night"
    day = "./DashControl/day"
    global sunrise #sunrise time from ini file
    global sunset #sunset time from ini file
    global files # final path to files
    global refreshcount #timer value to refresh the UI

    now = datetime.now() #full datetime
    current_time = now.strftime('%H:%M')
    sunr = datetime.strptime(sunrise,'%H:%M') #sunrise time from ini without date
    suns = datetime.strptime(sunset,'%H:%M') #sunset time from ini without date
    curt = datetime.strptime(current_time,'%H:%M') #current time winthout date

    if (curt > sunr) and (curt < suns):
        files = day
        refreshcount = (suns-curt)
        print ('time till sunset',refreshcount, refreshcount.seconds)
    else:
        files = night
        refreshcount = (sunr-curt)
        print ('time till sunrise',refreshcount, refreshcount.seconds)

def refresh():
    Popen(["/home/pi/dashcontrol_startup.sh"])
    print('let my people go')
    exit()

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

def playsound():
    pygame.mixer.music.play()

def PeakDown(event):
    global P
    global ox
    global oy
    playsound()
    if ((88+ox <= event.x <= 458+ox) and (90+oy <= event.y <= 500+oy)):
        P = 0
        #print("Peak OFF") #Did you click PEAK_w S1?

    if ((1462+ox <= event.x <= 1832+ox) and (90+oy <= event.y <= 500+oy)):
        P = 0
        SETUP_w_label.tkraise()
        CloseRelay2()
        #print("Close Relay 2") #Did you click S2?

    if ((1004+ox <= event.x <= 1374+ox) and (90+oy <= event.y <= 500+oy)):
        P = 0
        MPHKPH_w_label.tkraise()
        CloseRelay3()
        #print("Close Relay 3") #Did you click S3?

    if ((1004+ox <= event.x <= 1374+ox) and (592+oy <= event.y <= 1002+oy)):
        P = 0
        PEAKRESET_w_label.tkraise()
        CloseRelay4()
        #print("Close Relay 4") #Did you click S4?

    if ((1462+ox <= event.x <= 1832+ox) and (592+oy <= event.y <= 1002+oy)):
        EXIT_w_label.tkraise()
        #print("Exit")#Did you click EXIT?

def ButtonDown(event):
    global P
    global ox
    global oy
    playsound()
    ##event button map
    if ((88+ox <= event.x <= 458+ox) and (90+oy <= event.y <= 500+oy)):
        #P=1 #uncomment for peak hold
        #print("Peak On")
        PEAK_w_label.tkraise()
        CloseRelay1()
        #print("Close Relay 1") #Did you click S1?

    if ((547+ox <= event.x <= 917+ox) and (90+oy <= event.y <= 500+oy)):
        LASTALERT_w_label.tkraise()
        CloseRelay2()
        #print("Close Relay 2") #Did you click S2?

    if ((88+ox <= event.x <= 458+ox) and (592+oy <= event.y <= 1002+oy)):
        NEXT_w_label.tkraise()
        CloseRelay3()
        #print("Close Relay 3") #Did you click S3?

    if ((547+ox <= event.x <= 917+ox) and (592+oy <= event.y <= 1002+oy)):
        LAPTRIP_w_label.tkraise()
        CloseRelay4()
        #print("Close Relay 4") #Did you click S4?

    if ((1004+ox <= event.x <= 1374+ox) and (90+oy <= event.y <= 500+oy)):
        #PEAK_w_label.tkraise()
        MPHKPH_w_label.tkraise()
        #NEXT_w_label.tkraise()
        CloseRelay3()
        CloseRelay1()
        #print("Close Relay 1 3") #Did you click MPH KPH?

    if ((1004+ox <= event.x <= 1374+ox) and (592+oy <= event.y <= 1002+oy)):
        #PEAK_w_label.tkraise()
        PEAKRESET_w_label.tkraise()
        #LAPTRIP_w_label.tkraise()
        CloseRelay1()
        CloseRelay4()
        #print("Close Relay 1 4") #Did you click RESET PEAK?

    if ((1462+ox <= event.x <= 1832+ox) and (90+oy <= event.y <= 500+oy)):
        #PEAK_w_label.tkraise()
        SETUP_w_label.tkraise()
        #LASTALERT_w_label.tkraise()
        CloseRelay1()
        CloseRelay2()
        #print("Close Relay 1 2") #Did you click SETUP?

    if ((1462+ox <= event.x <= 1832+ox) and (592+oy <= event.y <= 1002+oy)):
        EXIT_w_label.tkraise()
        #print("Exit")#Did you click EXIT?


def PeakRelease(event):
    global P
    global ox
    global oy
    background_label.tkraise()

    if ((1462+ox <= event.x <= 1832+ox) and (592+oy <= event.y <= 1002+oy)):
        background_label.tkraise()
        OpenRelay1()
        OpenRelay2()
        OpenRelay3()
        OpenRelay4()
        #print("Open Relay 1 2 3 4")
        os.system('DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool search --desktop 0 --name "DashControl" windowminimize; DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool mousemove 5 100; DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool click 1')

    else:
        background_label.tkraise()
        OpenRelay4()
        OpenRelay3()
        OpenRelay2()
        #print("Open Relay 4 3 2") #Open Relays 4 3 2
        if (P==1):
            PEAK_w_label.tkraise()
        else:
            OpenRelay1()
            #print("Open Relay 1") #Open Relay 1


def ButtonRelease(event):
    global P
    global ox
    global oy
    if ((1724+ox <= event.x <= 1880+ox) and (1044+oy <= event.y <= 1160+oy)):
        refresh()

    if ((1462+ox <= event.x <= 1832+ox) and (592+oy <= event.y <= 1002+oy)):
        background_label.tkraise()
        OpenRelay1()
        OpenRelay2()
        OpenRelay3()
        OpenRelay4()
        #print("Open Relay 1 2 3 4")
        os.system('DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool search --desktop 0 --name "DashControl" windowminimize; DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool mousemove 5 100; DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool click 1')
    else:
        background_label.tkraise()
        OpenRelay4()
        OpenRelay3()
        OpenRelay2()
        #print("Open Relay 4 3 2") #Open Relays 4 3 2
        if (P==1):
            PEAK_w_label.tkraise()
        else:
            OpenRelay1()
            #print("Open Relay 1") #Open Relay 1

TimeCheck() #setup file path for day or night images
root.after ((refreshcount.seconds) * 1000, refresh)

##setup the application window attributes
root.wm_attributes('-fullscreen','false') #Set window full fullscreen
root['bg'] = 'black' #set the background color
frame = tk.Frame(root, width=1920, height=1080) #set the app window size
filename = tk.PhotoImage(file = files+"/Background.png") #set the background image file location
background_label = tk.Label(root, image=filename) #create a label to place on the Frame
background_label.place(x=0, y=0, relwidth=1, relheight=1) #place the label on frame
##bind mouse events to the background_label
background_label.bind("<Button-1>", ButtonDown)
background_label.bind("<ButtonRelease-1>", ButtonRelease)

##button select images
PEAK_w = tk.PhotoImage(file = files+"/PEAK_w.png")
PEAK_w_label = tk.Label(root, image=PEAK_w, background='black')
##bind mouse events to the PEAK_w_label
PEAK_w_label.bind("<Button-1>", PeakDown)
PEAK_w_label.bind("<ButtonRelease-1>", PeakRelease)
PEAK_w_label.place(x=88+ox, y=90+oy) #PEAK_w3.png x=-1, y=-1  originally PEAK_w.png x=88, y=90

LASTALERT_w = tk.PhotoImage(file = files+"/LASTALERT_w.png")
LASTALERT_w_label = tk.Label(root, image=LASTALERT_w, background='black')
LASTALERT_w_label.place(x=547+ox, y=90+oy)

MPHKPH_w = tk.PhotoImage(file = files+"/MPHKPH_w.png")
MPHKPH_w_label = tk.Label(root, image=MPHKPH_w, background='black')
MPHKPH_w_label.place(x=1004+ox, y=90+oy)

SETUP_w = tk.PhotoImage(file = files+"/SETUP_w.png")
SETUP_w_label = tk.Label(root, image=SETUP_w, background='black')
SETUP_w_label.place(x=1462+ox, y=90+oy)

NEXT_w = tk.PhotoImage(file = files+"/NEXT_w.png")
NEXT_w_label = tk.Label(root, image=NEXT_w, background='black')
NEXT_w_label.place(x=88+ox, y=592+oy)

LAPTRIP_w = tk.PhotoImage(file = files+"/LAPTRIP_w.png")
LAPTRIP_w_label = tk.Label(root, image=LAPTRIP_w, background='black')
LAPTRIP_w_label.place(x=547+ox, y=592+oy)

PEAKRESET_w = tk.PhotoImage(file = files+"/PEAKRESET_w.png")
PEAKRESET_w_label = tk.Label(root, image=PEAKRESET_w, background='black')
PEAKRESET_w_label.place(x=1004+ox, y=592+oy)

EXIT_w = tk.PhotoImage(file = files+"/EXIT_w.png")
EXIT_w_label = tk.Label(root, image=EXIT_w, background='black')
EXIT_w_label.place(x=1462+ox, y=592+oy)

frame.pack()
background_label.tkraise()
root.mainloop()
