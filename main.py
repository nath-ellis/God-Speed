import pygame
from pygame import *
pygame.init()

running = True

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False