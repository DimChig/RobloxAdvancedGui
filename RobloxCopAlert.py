import math
import random
import cv2 as cv
import os
import time
from windowcapture import WindowCapture
import vision
import pygame
import win32gui, win32ui, win32con

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

RADAR_FREQUENCY = 3 #x in minute
sound_path = 'D:/Документы/PycharmProjects/RobloxScanner/sounds/pops/pop_0.mp3'
IMAGE_SCALING = 1.7



# initialize the WindowCapture class
wincap = WindowCapture('Roblox', 10, -165, 680, 0)

start_x, start_y = (-1, -1)
end_x, end_y = (-1, -1)

vision_knobs = vision.Vision('knob_full.png', (start_x, start_y), (end_x, end_y), [])
vision_map_upper_left = vision.Vision('map_upper_left.png', (start_x, start_y), (end_x, end_y), [])
vision_map_lower_right = vision.Vision('map_lower_right.png', (start_x, start_y), (end_x, end_y), [])

def map(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def playSound(volume):
    # threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()
    pygame.mixer.init()
    sound = pygame.mixer.Sound(sound_path.replace("0","" + str(random.randrange(0, 7))))
    sound.set_volume(volume)  # Now plays at 90% of full volume.
    sound.play()



#PYGAME
pygame.init()
pygame.display.set_caption("RadarHack")


width, height = 155, 155

screen = pygame.display.set_mode([width * IMAGE_SCALING, height * IMAGE_SCALING])
pygame.display.set_icon(pygame.image.load('radarIcon.png'))


def blitRotate(surf, image, pos, originPos, angle):
    angle = 360 - angle
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)

def drawCriminals():
    screen.fill((random.randrange(0, 255), 200, 200))

pygame_last_press = time.time()
def handlePygame(screenshot, shadow_criminals):
    global pygame_last_press
    #surf = pygame.surfarray.make_surface(screenshot[...,::-1].copy())
    surf = pygame.transform.flip(pygame.surfarray.make_surface(screenshot[...,::-1].copy()), True, False)
    surf = pygame.transform.scale(surf, (screen.get_width(), screen.get_height()))
    blitRotate(screen, surf, (screen.get_width()/2, screen.get_height()/2),
               (screen.get_width()/2, screen.get_height()/2), -90)

    surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

    current_time = time.time()
    for c in shadow_criminals:
        x = c[0][0] * IMAGE_SCALING
        y = c[0][1] * IMAGE_SCALING
        t = RADAR_FREQUENCY - (current_time - c[1])

        color_a = map(t, 0, RADAR_FREQUENCY, 0, 255)
        if color_a < 0: color_a = 0
        if color_a > 255: color_a = 255
        color = (255, 0, 0, color_a)

        min_r = 5 * IMAGE_SCALING
        max_r = 20 * IMAGE_SCALING
        r = map(t, 0, RADAR_FREQUENCY, max_r, min_r)

        max_thickness = 5
        thickness = int(max(1, int(map(t, 0, RADAR_FREQUENCY, 1, max_thickness) * IMAGE_SCALING)))

        pygame.draw.circle(surface, color, (x, y), r, thickness)
        pygame.draw.line(surface, (255, 0, 0, int(color[3]/2)), (x, y), (screen.get_width() / 2, screen.get_height()/2), thickness)
        screen.blit(surface, (0, 0))

    pygame.display.flip()

    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.QUIT:
            if time.time() - pygame_last_press < 0.2:
                exit(1234)
            else:
                pygame_last_press = time.time()

    win32gui.SetWindowPos(win32gui.FindWindow(None, "RadarHack"), win32con.HWND_TOPMOST, 0, 0, 0, 0,
                         win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)



prev_time = time.time()
flag = False
shadow_criminals = []
isScreenInited = False


clock = pygame.time.Clock()
running = True
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 34)
while running:
    clock.tick(30)
    screen.fill((200, 200, 200))

    text = font.render("Click to start", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (screen.get_width() / 2, screen.get_height() / 2)
    screen.blit(text, textRect)

    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.QUIT:
            running = False
    pygame.display.flip()

screen = pygame.display.set_mode([width * IMAGE_SCALING, height * IMAGE_SCALING], pygame.NOFRAME)

while True:

    # get an updated image of the game
    screenshot = wincap.get_screenshot()



    criminals = vision_knobs.find(screenshot, 0.9, 'rectangles')
    cnt_total = len(criminals)


    current_time = time.time()

    if cnt_total > 0 and flag == True:

        flag = False
        prev_time = time.time()

        min_dist = screen.get_width() * screen.get_height()
        for c in criminals:
            shadow_criminals.append((c, current_time))

            x = c[0] * IMAGE_SCALING
            y = c[0] * IMAGE_SCALING
            dist = math.sqrt(math.pow(x - screen.get_width()/2, 2) + math.pow(y - screen.get_height()/2, 2))
            min_dist = min(min_dist, dist)

        max_volume = 1
        min_volume = 0.1
        volume = map(min_dist, 20, math.sqrt(math.pow(screen.get_width()/2, 2) + math.pow(screen.get_height()/2, 2)), max_volume, min_volume)
        volume = map(volume * volume, 0, max_volume * max_volume, 0, 1)
        #print(min_dist, " => ",volume," max = ",(math.sqrt(math.pow(screen.get_width()/2, 2) + math.pow(screen.get_height()/2, 2))))
        playSound(volume)

    if cnt_total == 0 or time.time() - prev_time > RADAR_FREQUENCY:
        flag = True

    #clear steps

    for c in shadow_criminals:
        if current_time - c[1] > RADAR_FREQUENCY:
            shadow_criminals.remove(c)

    #vision_knobs.drawRect(screenshot, shadow_criminals)

    handlePygame(screenshot, shadow_criminals)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')