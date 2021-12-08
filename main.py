import pygame
from pygame import *
import random
import os
from pygame_markdown import MarkdownRenderer
pygame.init()

running = True
gameOver = False
menuOpen = True
credit = False

clock = pygame.time.Clock()

screen = pygame.display.set_mode((500, 478))
pygame.display.set_caption("God Speed")
gameicon = pygame.image.load(os.path.join("assets", "car1.png"))
pygame.display.set_icon(gameicon)

blue = (25, 99, 145)
white = (255, 255, 255)
black = (0, 0, 0)
red = (250, 9, 18)

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
road = pygame.transform.scale(pygame.image.load(os.path.join("assets", "road.png")), ((270, 600))) #270 x 478
bgy1 = 0
bgy2 = road.get_height() * -1

#Obstacles
enemycar1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemycar1.png")), ((46, 96)))
enemycar2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemycar2.png")), ((46, 96)))
enemycar3 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemycar3.png")), ((46, 96)))
enemycar4 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemycar4.png")), ((46, 96)))
truck1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "truck1.png")), ((46, 96)))
obstacles = []
pygame.time.set_timer(USEREVENT+2, 1000)
pygame.time.set_timer(USEREVENT+4, 3000, 5000)
pygame.time.set_timer(USEREVENT+5, 2000, 3000)
pygame.time.set_timer(USEREVENT+6, 1500, 2000)
pygame.time.set_timer(USEREVENT+7, 1000, 1500)
enemyspeed = 5

explosionsfx = pygame.mixer.Sound(os.path.join("assets", "explosion.flac"))

#Lives
life = pygame.image.load(os.path.join("assets", "lives.png"))

ticks = 0
pygame.time.set_timer(USEREVENT+3, 1000)

credittimer = 0

#Text
text = pygame.font.Font(os.path.join("assets", "kenpixel_blocks.ttf"), 50)
smalltext = pygame.font.Font(os.path.join("assets", "kenpixel_blocks.ttf"), 20)

#Music
pygame.mixer.music.load(os.path.join("assets", "MenuSong.mp3"))
pygame.mixer.music.play(-1)

#MD Renderer
md = MarkdownRenderer()
md.set_markdown(os.path.join("assets", "credit.md"))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.speed = 1
        self.lives = 3
    def draw(self):
        screen.blit(car[carstage], (self.x, self.y))

char = Player(153, 400)

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
        self.y += enemyspeed

def redraw():
    global bgy1, bgy2, obstacles, gameOver
    clock.tick(30)
    pygame.display.update()
    screen.fill(blue)
    screen.blit(road, (105, bgy1))
    screen.blit(road, (105, bgy2))
    if not gameOver and not menuOpen:
        if bgy1 >= 468:
            bgy1 = (road.get_height() - char.speed * 3) * -1
        if bgy2 >= 468:
            bgy2 = (road.get_height() - char.speed * 3) * -1
        char.draw()
        #Lives
        if char.lives == 0:
            gameOver = True
        else:
            if char.lives == 3:
                screen.blit(life, (10, 10))
                screen.blit(life, (10, 56))
                screen.blit(life, (10, 102))
            if char.lives == 2:
                screen.blit(life, (10, 10))
                screen.blit(life, (10, 56))
            if char.lives == 1:
                screen.blit(life, (10, 10))
        #Obstacles
        for o in obstacles:
            opos = Rect(o.x, o.y, o.width, o.height)
            playerpos = Rect(char.x, char.y, char.width, char.height)
            o.draw()
            if playerpos.colliderect(opos):
                explosion()
                obstacles = []
                char.lives -= 1
                break
            o.move()
    elif gameOver:
        lose()
    elif menuOpen:
        menu()

def movement():
    keypressed = pygame.key.get_pressed()

    if keypressed[K_RIGHT] and char.x == 153 or keypressed[K_d] and char.x == 153:
        char.x += 109
    if keypressed[K_LEFT] and char.x == 262 or keypressed[K_a] and char.x == 262:
        char.x -= 109

def obstacle():
    global obstacles
    roadside = random.randint(1, 2)
    t = random.randint(1, 4)

    if len(obstacles) >= 20:
        del obstacles[0]
        del obstacles[1]
        del obstacles[2]
        del obstacles[3]
        del obstacles[4]
        del obstacles[5]
        del obstacles[6]
        del obstacles[7]
        del obstacles[8]
        del obstacles[9]

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

def lose():
    global gameOver, obstacles, ticks, enemyspeed, bgy1, bgy2

    screen.blit(text.render("Game", True, (red)), (165, 50))
    screen.blit(text.render("Over", True, (red)), (170, 100))
    screen.blit(smalltext.render("Click to play", True, (white)), (152, 350))

    bgy1 = 0
    bgy2 = road.get_height() * -1

    obstacles = []

    char.lives = 3

    ticks = 0

    char.speed = 1
    enemyspeed = 5

    mouseclick = pygame.mouse.get_pressed()

    if mouseclick[0]:
        gameOver = False

def menu():
    global menuOpen, enemyspeed, credit, credittimer
    mouseclick = pygame.mouse.get_pressed()
    mousex, mousey = pygame.mouse.get_pos()

    if not credit:
        screen.blit(text.render("God", True, (white)), (185, 50))
        screen.blit(text.render("Speed", True, (white)), (150, 100))
        screen.blit(smalltext.render("Click to play", True, (white)), (152, 350))
        screen.blit(smalltext.render("Credit", True, (white)), (5, 448))
    else:
        screen.fill(blue)
        screen.blit(smalltext.render("The following work was used", True, (white)), (55, 10))
        screen.blit(smalltext.render("Go Back", True, (white)), (5, 448))
        md.set_area(screen, 0, 40, width=500, height=415)
        md.set_color_background(25, 99, 145)
        md.set_color_font(255, 255, 255)
        md.display(pygame.event.get(), mousex, mousey, mouseclick)

    char.speed = 1
    enemyspeed = 5
    credittimer -= 1

    if credittimer <= 0:
        credittimer = 0

    if mouseclick[0]:
        pos = pygame.mouse.get_pos()
        if pos[0] < 90 and pos[1] > 450 and not credit and credittimer <= 0:
            credittimer += 10
            credit = True
        elif pos[0] < 100 and pos[1] > 450 and credit and credittimer <= 0:
            credittimer += 10
            credit = False
        elif not credit and credittimer <= 0:
            pygame.mixer.music.stop()
            menuOpen = False

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == USEREVENT+1:
            carstage += 1
        if e.type == USEREVENT+2:
            if char.speed < 6.9:
                char.speed += 0.1
            if enemyspeed < 10:
                enemyspeed += 0.1
        if e.type == USEREVENT+4 and ticks <= 40 and not gameOver and not menuOpen:
            obstacle()
        if e.type == USEREVENT+5 and ticks >= 41 and ticks <= 80 and not gameOver and not menuOpen:
            obstacle()
        if e.type == USEREVENT+6 and ticks >= 81 and ticks <= 99 and not gameOver and not menuOpen:
            obstacle()
        if e.type == USEREVENT+7 and ticks >= 100 and not gameOver and not menuOpen:
            obstacle()
        if e.type == USEREVENT+3 and not menuOpen and not gameOver:
            ticks += 1

    if not gameOver and not menuOpen:
        bgy1 += char.speed
        bgy2 += char.speed

        if carstage >= 2:
            carstage = 0

        movement()

    redraw()

pygame.quit()
quit()