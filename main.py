import pygame
from pygame import *
import random
import time
import os
pygame.init()

running = True
gameOver = False

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

#Obstacles
enemycar1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemycar1.png")), ((46, 96)))
enemycar2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemycar2.png")), ((46, 96)))
enemycar3 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemycar3.png")), ((46, 96)))
enemycar4 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemycar4.png")), ((46, 96)))
truck1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "truck1.png")), ((46, 96)))
obstacles = []
pygame.time.set_timer(USEREVENT+2, 5000)

explosionsfx = pygame.mixer.Sound(os.path.join("assets", "explosion.flac"))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
    def draw(self):
        screen.blit(car[carstage], (self.x, self.y))

class Car:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.width = 46
        self.height = 96
        self.type = type
    def draw(self):
        if self.type == "blue1":
            screen.blit(enemycar1, (self.x, self.y))
        elif self.type == "green":
            screen.blit(enemycar2, (self.x, self.y))
        elif self.type == "blue2":
            screen.blit(enemycar3, (self.x, self.y))
        elif self.type == "pink":
            screen.blit(enemycar4, (self.x, self.y))
    def move(self):
        self.y += 5

char = Player(153, 400)

def redraw():
    global bgy1, bgy2, obstacles, gameOver
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
    for o in obstacles:
        opos = Rect(o.x, o.y, o.width, o.height)
        playerpos = Rect(char.x, char.y, char.width, char.height)
        o.draw()
        if playerpos.colliderect(opos):
            explosion()
            obstacles = []
            gameOver = True
            break
        o.move()

def movement():
    keypressed = pygame.key.get_pressed()

    if keypressed[K_RIGHT] and char.x == 153:
        char.x += 109
    if keypressed[K_LEFT] and char.x == 262:
        char.x -= 109

def obstacle():
    global obstacles
    roadside = random.randint(1, 2)
    t = random.randint(1, 4)

    if roadside == 1:
        if t == 1:
            obstacles.append(Car(162, -100, "blue1"))
        elif t == 2:
            obstacles.append(Car(162, -100, "green"))
        elif t == 3:
            obstacles.append(Car(162, -100, "blue2"))
        elif t == 4:
            obstacles.append(Car(162, -100, "pink"))
    elif roadside == 2:
        if t == 1:
            obstacles.append(Car(271, -100, "blue1"))
        elif t == 2:
            obstacles.append(Car(271, -100, "green"))
        elif t == 3:
            obstacles.append(Car(271, -100, "blue2"))
        elif t == 4:
            obstacles.append(Car(271, -100, "pink"))

obstacle()

def explosion():
    explosionimg = [
        pygame.image.load(os.path.join("assets", "explosion1.png")),
        pygame.image.load(os.path.join("assets", "explosion2.png")),
        pygame.image.load(os.path.join("assets", "explosion3.png")),
        pygame.image.load(os.path.join("assets", "explosion4.png")),
        pygame.image.load(os.path.join("assets", "explosion5.png")),
        pygame.image.load(os.path.join("assets", "explosion6.png")),
        pygame.image.load(os.path.join("assets", "explosion7.png")),
        pygame.image.load(os.path.join("assets", "explosion8.png")),
        pygame.image.load(os.path.join("assets", "explosion9.png")),
        pygame.image.load(os.path.join("assets", "explosion10.png")),
        pygame.image.load(os.path.join("assets", "explosion11.png")),
        pygame.image.load(os.path.join("assets", "explosion12.png"))
    ]
    pygame.mixer.Sound.play(explosionsfx)
    for e in explosionimg:
        screen.blit(e, (char.x - 20, char.y - 18))
        pygame.display.update()
        clock.tick(24)
        

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == USEREVENT+1:
            carstage += 1
        if e.type == USEREVENT+2:
            obstacle()
    
    bgy1 += 1
    bgy2 += 1

    if carstage >= 2:
        carstage = 0

    movement()

    redraw()