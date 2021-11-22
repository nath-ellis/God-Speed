import pygame
from pygame import *
import random
import os
pygame.init()

running = True

clock = pygame.time.Clock()

screen = pygame.display.set_mode((500, 505))
pygame.display.set_caption("God Speed")
#gameicon = pygame.image.load(os.path.join("assets", "icon.ico"))
#pygame.display.set_icon(gameicon)

blue = (25, 99, 145)

road = pygame.image.load(os.path.join("assets", "road.svg"))

def redraw():
    clock.tick(30)
    pygame.display.update()
    screen.fill(blue)
    screen.blit(road, (200, 0))

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    
    redraw()