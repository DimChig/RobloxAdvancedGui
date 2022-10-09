import random

import cv2 as cv
import numpy as np
import os
import time
from windowcapture import WindowCapture
import vision

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

UPDATE_FREQUENCY = 60 #x in minute

class Place:
    x = 0
    id = 0
    y = 0
    size = 0
    name = ""
    sort = 0
    found = 0

    def __init__(self, id, x, y, size, name, sort):
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        self.name = name
        self.sort = sort
        self.found = 0


places = []
places.append(Place(1, 335, 325, 80, "town", 1))
places.append(Place(2, 465, 256, 80, "volcano", 3))
places.append(Place(3, 233, 315, 65, "prison", 0))
places.append(Place(4, 350, 395, 40, "tomb", 2))
places.append(Place(5, 320, 478, 30, "bank", 3))
places.append(Place(6, 320, 513, 30, "j-store", 2))
places.append(Place(7, 386, 510, 55, "museum", 3))
places.append(Place(8, 214, 471, 50, "gas station", 1))
places.append(Place(9, 291, 530, 25, "city base", 2))
places.append(Place(10, 320, 577, 35, "power plant", 2))
places.append(Place(11, 301, 120, 50, "casino", 2))
places.append(Place(12, 294, 50, 90,  "crater city", 0))
places.append(Place(13, 215, 170, 70, "race track", 0))
places.append(Place(14, 410, 413, 70, "sand road", 1))
places.append(Place(15, 230, 613, 70, "airport", 0))
places.append(Place(16, 285, 557, 30, "crime port", 0))
places.append(Place(17, 267, 409, 70, "prison road", 0))
places.append(Place(18, 362, 458, 40, "zone 51", 0))
places.append(Place(19, 427, 337, 70, "jump (volcano)", 1))
places.append(Place(20, 383, 174, 100, "desert", 0))
places.append(Place(21, 125, 581, 45, "super prison", 1))
places.append(Place(22, 476, 581, 100, "cargo", 0))
map_max_x = 651
map_max_y = 651

#GUI
from tkinter import *

win = Tk()
win.geometry("400x400+500+100")

text_main = Text(win, padx=5, pady=5, font=25)
text_main.grid(row=3)

def setText(s):
    text_main.delete(1.0, END)
    text_main.insert(1.0, s)

setText("lol")




# initialize the WindowCapture class
wincap = WindowCapture('Roblox')

wincap.list_window_names()

start_x, start_y = (-1, -1)
end_x, end_y = (-1, -1)

start_x, start_y = (248, 121)
end_x, end_y = (771, 643)


vision_knobs = vision.Vision('knob.png', (start_x, start_y), (end_x, end_y), places)
vision_map_upper_left = vision.Vision('map_upper_left.png', (start_x, start_y), (end_x, end_y), places)
vision_map_lower_right = vision.Vision('map_lower_right.png', (start_x, start_y), (end_x, end_y), places)

def map(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def log_data(places):
    s = "newline" + str(time.time()) + ";&&;"
    for p in places:
        s += str(p.id) + "-" + str(p.found) + ";"
    print(s)
    file_object = open('log.txt', 'a')
    file_object.write(s + "\n")
    file_object.close()

loop_time = time.time()
while True:

    # get an updated image of the game
    screenshot = wincap.get_screenshot()


    #print(points)

    if False: #Calibrate Map
        map_start = vision_map_upper_left.find(screenshot, 0.8, 'rectangles')
        if start_x == -1 and len(map_start) > 0:
            print("KNOW START FOUND ", map_start[0])
            start_x, start_y = map_start[0]
            start_x -= 90
            start_y -= 90

        map_start = vision_map_lower_right.find(screenshot, 0.8, 'rectangles')
        if end_x == -1 and len(map_start) > 0:
            print("KNOW END FOUND ", map_start[0])
            end_x, end_y = map_start[0]

        # display the processed image

    criminals = vision_knobs.find(screenshot, 0.95, 'rectangles')
    cnt_total = len(criminals)


    criminals_recognized = []

    for p in places:
        p.found = 0
        for c in criminals:
            isColliding = False

            cx = int(map(c[0], start_x, end_x, 0, map_max_x))
            cy = int(map(c[1], start_y, end_y, 0, map_max_y))
            if cx < 0 or cy < 0:
                continue
            #print(c[0],'=',cx,",  ",c[1],'=',cy)

            if p.x - p.size/2 < cx < p.x + p.size/2 and p.y - p.size / 2 < cy < p.y + p.size / 2:
                p.found += 1
                criminals_recognized.append(c)
                #criminals.remove(c)

        #s += p.name + "->" + str(p.found) + "\n"

    vision_knobs.drawRect(screenshot, criminals_recognized)

    places.sort(key=lambda x: (x.found, x.sort), reverse=True)

    s = ""
    for p in places:
        if p.found > 0:
            s += p.name + ": " + str(p.found) + "\n"
    s += "\nTotal: " + str(cnt_total) + "\nNot found: " + str(cnt_total - len(criminals_recognized))

    setText(s)
    win.update()

    if time.time() - loop_time > 60 / UPDATE_FREQUENCY:
        loop_time = time.time()
        if cnt_total < 7:
            print("\033[95mNOT ENOUGH PEOPLE!\033[0m")
        else:
            log_data(places)



    #points = vision_gunsnbottle.find(screenshot, 0.7, 'points')

    # debug the loop rate
    #print('FPS {}'.format(1 / (time() - loop_time)))

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')