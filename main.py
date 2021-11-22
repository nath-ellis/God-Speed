import pygame
from pygame import *
import random
import os
pygame.init()

running = True

clock = pygame.time.Clock()

screen = pygame.display.set_mode((500, 478))
pygame.display.set_caption("God Speed")
#gameicon = pygame.image.load(os.path.join("assets", "icon.ico"))
#pygame.display.set_icon(gameicon)

blue = (25, 99, 145)

#The Car
carimport = [
    pygame.image.load(os.path.join("assets", "car1.png")),
    pygame.image.load(os.path.join("assets", "car2.png"))
    ]
carstage = 0
car = []
for c in carimport:
    car.append(pygame.transform.scale(c, (64, 64)))
#The car change timer
pygame.time.set_timer(USEREVENT+1, 150)

#The background
road = pygame.image.load(os.path.join("assets", "road.png")) #270 x 478
bgy1 = 0
bgy2 = road.get_height() * -1

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 30
    def draw(self):
        screen.blit(car[carstage], (self.x, self.y))

char = Player(153, 400)

def redraw():
    global bgy1, bgy2
    clock.tick(30)
    pygame.display.update()
    screen.fill(blue)
    screen.blit(road, (105, bgy1))
    screen.blit(road, (105, bgy2))
    if bgy1 >= 478:
        bgy1 = road.get_height() * -1
    if bgy2 >= 478:
        bgy2 = road.get_height() * -1
    char.draw()

def movement():
    keypressed = pygame.key.get_pressed()

    if keypressed[K_RIGHT] and char.x == 153:
        char.x += 109
    if keypressed[K_LEFT] and char.x == 262:
        char.x -= 109

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == USEREVENT+1:
            carstage += 1
    
    bgy1 += 1
    bgy2 += 1

    if carstage >= 2:
        carstage = 0

    movement()

    redraw()