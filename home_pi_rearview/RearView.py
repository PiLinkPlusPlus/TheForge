import tkinter as tk
import os
import pygame
pygame.mixer.init()

from subprocess import Popen #to execute unix commands wout blocking
root = tk.Tk()
root.title('RearView')

def playsound():
    pygame.mixer.music.load("./DashControl/Tink.wav")
    pygame.mixer.music.play()

def CamDisplayOn():
    Popen(["touch", "/tmp/backupcamera_manual"])
    playsound()

def CamDisplayOff():
    Popen(["rm", "/tmp/backupcamera_manual"])
    playsound()

def ButtonDown(event):
    ##event button map
    if ((0 <= event.x <= 1920) and (0 <= event.y <= 1200)):
        CamDisplayOff() #rm /tmp/backupcamera_manual
        exit()

##write the file on open and display the camera video
CamDisplayOn() #touch /tmp/backupcamera_manual

##setup the application window attributes
root.wm_attributes('-fullscreen','true') #Set window full fullscreen
root['bg'] = 'black' #set the background color
frame = tk.Frame(root, width=1920, height=1200) #set the app window size
filename = tk.PhotoImage(file = "./wallpaper.png") #set the background image file location
background_label = tk.Label(root, image=filename) #create a label to place on the Frame
background_label.place(x=0, y=0, relwidth=1, relheight=1) #place the label on frame
##bind mouse events to the background_label
background_label.bind("<Button-1>", ButtonDown)

frame.pack()
background_label.tkraise()
root.mainloop()
