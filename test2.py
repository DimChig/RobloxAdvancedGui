import random

import pygame
import time

class Place:
    x = 0
    y = 0
    size = 0
    name = ""
    sort = 0

    def __init__(self, x, y, size, name, sort):
        self.x = x
        self.y = y
        self.size = size
        self.name = name
        self.sort = sort


places = []
places.append(Place(335, 325, 80, "town", 1))
places.append(Place(465, 256, 80, "volcano", 3))
places.append(Place(233, 315, 65, "prison", 0))
places.append(Place(350, 395, 40, "tomb", 2))
places.append(Place(320, 478, 30, "bank", 3))
places.append(Place(320, 513, 30, "j-store", 2))
places.append(Place(386, 510, 55, "museum", 3))
places.append(Place(214, 471, 50, "gas station", 1))
places.append(Place(291, 530, 25, "city base", 2))
places.append(Place(320, 577, 35, "power plant", 2))
places.append(Place(301, 120, 50, "casino", 2))
places.append(Place(294, 50, 90,  "crater city", 0))
places.append(Place(215, 170, 70, "race track", 0))
places.append(Place(410, 413, 70, "sand road", 1))
places.append(Place(230, 613, 70, "airport", 0))
places.append(Place(285, 557, 30, "crime port", 0))
places.append(Place(267, 409, 70, "prison road", 0))
places.append(Place(362, 458, 40, "zone 51", 0))
places.append(Place(427, 337, 70, "jump (volcano)", 1))
places.append(Place(383, 174, 100, "desert", 0))
places.append(Place(125, 581, 45, "super prison", 1))
places.append(Place(476, 581, 100, "cargo", 0))
#max = 651 x 651

pygame.init()

img_original = pygame.image.load("jailbreak_map.png")
width, height = img_original.get_width(), img_original.get_height()
screen = pygame.display.set_mode([width, height])


pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 16)

def checkCollision(pos1, cell_size, pos2, cs):
    # pos1 => border

    s1 = cell_size
    s2 = cs
    x1 = pos1[0]
    y1 = pos1[1]
    x2 = pos2[0]
    y2 = pos2[1]

    collisionX = x1 + s1 >= x2 and x2 + s2 >= x1
    collisionY = y1 + s1 >= y2 and y2 + s2 >= y1

    return collisionX and collisionY


clock = pygame.time.Clock()
running = True
while running:
    clock.tick(30)
    screen.fill((200, 200, 200))
    screen.blit(img_original, (0, 0))
    keys = pygame.key.get_pressed()
    for p in places:
        pygame.draw.rect(screen, (255, 0, 0), (p.x - p.size / 2, p.y - p.size / 2, p.size, p.size), 2)
        #pygame.draw.circle(screen, (255, 0, 0), (p.x, p.y), 10)

        text = font.render(p.name, True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (p.x, p.y)
        screen.blit(text, textRect)

    mouseX, mouseY = pygame.mouse.get_pos()
    size = 20


    b = False
    for p in places:
        pos1 = (p.x - p.size/2, p.y - p.size/2)
        pos2 = (mouseX - size/2, mouseY - size/2)
        if checkCollision(pos1, p.size, pos2, size):
            b = True
    if b:
        pygame.draw.rect(screen, (0, 255, 0), (mouseX - size / 2, mouseY - size / 2, size, size), 2)
    else:
        pygame.draw.rect(screen, (255, 0, 0), (mouseX - size / 2, mouseY - size / 2, size, size), 2)



    for e in pygame.event.get():
        if e.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()

        if e.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()

