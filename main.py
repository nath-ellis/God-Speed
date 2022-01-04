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
game_icon = pygame.image.load(os.path.join("assets", "car1.png"))
pygame.display.set_icon(game_icon)

blue = (25, 99, 145)
white = (255, 255, 255)
black = (0, 0, 0)
red = (250, 9, 18)

# The Car
car_import = [
    pygame.image.load(os.path.join("assets", "car1.png")),
    pygame.image.load(os.path.join("assets", "car2.png"))
]
car_stage = 0
car = []
for c in car_import:
    car.append(pygame.transform.scale(c, (64, 64)))
# The car change timer
pygame.time.set_timer(USEREVENT + 1, 150)

# The background
road = pygame.transform.scale(pygame.image.load(os.path.join("assets", "road.png")), (270, 600))  # 270 x 478
bgy1 = 0
bgy2 = road.get_height() * -1

# Obstacles
enemy_car_1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemycar1.png")), (46, 96))
enemy_car_2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemycar2.png")), (46, 96))
enemy_car_3 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemycar3.png")), (46, 96))
enemy_car_4 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemycar4.png")), (46, 96))
truck1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "truck1.png")), (46, 96))
obstacles = []
pygame.time.set_timer(USEREVENT + 2, 1000)
pygame.time.set_timer(USEREVENT + 4, 3000, 5000)
pygame.time.set_timer(USEREVENT + 5, 2000, 3000)
pygame.time.set_timer(USEREVENT + 6, 1500, 2000)
pygame.time.set_timer(USEREVENT + 7, 1000, 1500)
enemy_speed = 5

explosion_sfx = pygame.mixer.Sound(os.path.join("assets", "explosion.flac"))

# Lives
life = pygame.image.load(os.path.join("assets", "lives.png"))

ticks = 0
pygame.time.set_timer(USEREVENT + 3, 1000)

credit_timer = 0

# Text
text = pygame.font.Font(os.path.join("assets", "kenpixel_blocks.ttf"), 50)
small_text = pygame.font.Font(os.path.join("assets", "kenpixel_blocks.ttf"), 20)
medium_text = pygame.font.Font(os.path.join("assets", "kenpixel_blocks.ttf"), 25)

# Music
pygame.mixer.music.load(os.path.join("assets", "MenuSong.mp3"))
pygame.mixer.music.play(-1)

# MD Renderer
md = MarkdownRenderer()
md.set_markdown(os.path.join("assets", "credit.md"))

# Score
score = 0
high_score_1 = open(os.path.join("assets", "highscore.txt"), "r")
high_score_1_contents = high_score_1.readlines()
high_score = int(high_score_1_contents[0])
high_score_1.close()


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        self.speed = 1
        self.lives = 3

    def draw(self):
        screen.blit(car[car_stage], (self.x, self.y))


char = Player(153, 400)


class Car:
    def __init__(self, x, y, style):
        self.x = x
        self.y = y
        self.width = 46
        self.height = 96
        self.type = style

    def draw(self):
        if self.type == "blue1":
            screen.blit(enemy_car_1, (self.x, self.y))
        elif self.type == "green":
            screen.blit(enemy_car_2, (self.x, self.y))
        elif self.type == "blue2":
            screen.blit(enemy_car_3, (self.x, self.y))
        elif self.type == "pink":
            screen.blit(enemy_car_4, (self.x, self.y))

    def move(self):
        self.y += enemy_speed


def redraw():
    global bgy1, bgy2, obstacles, gameOver, score
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
        screen.blit(medium_text.render(str(score), True, white), (5, 0))
        # Lives
        if char.lives == 0:
            gameOver = True
        else:
            if char.lives == 3:
                screen.blit(life, (5, 43))
                screen.blit(life, (5, 84))
                screen.blit(life, (5, 125))
            if char.lives == 2:
                screen.blit(life, (5, 43))
                screen.blit(life, (5, 84))
            if char.lives == 1:
                screen.blit(life, (5, 43))
        # Obstacles
        for o in obstacles:
            opos = Rect(o.x, o.y, o.width, o.height)
            playerpos = Rect(char.x, char.y, char.width, char.height)
            o.draw()
            if playerpos.colliderect(opos):
                explosion()
                obstacles = []
                char.lives -= 1
                score -= 500
                break
            o.move()
    elif gameOver:
        lose()
    elif menuOpen:
        menu()


def movement():
    key_pressed = pygame.key.get_pressed()

    if key_pressed[K_RIGHT] and char.x == 153 or key_pressed[K_d] and char.x == 153:
        char.x += 109
    if key_pressed[K_LEFT] and char.x == 262 or key_pressed[K_a] and char.x == 262:
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
    explosion_img = [
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
    pygame.mixer.Sound.play(explosion_sfx)
    for ex in explosion_img:
        screen.blit(ex, (char.x - 20, char.y - 18))
        pygame.display.update()
        clock.tick(24)


def lose():
    global gameOver, obstacles, ticks, enemy_speed, bgy1, bgy2, score, high_score

    screen.blit(text.render("Game", True, red), (165, 50))
    screen.blit(text.render("Over", True, red), (170, 100))
    screen.blit(medium_text.render(str(score), True, white), (5, 0))
    screen.blit(small_text.render("Click to play", True, white), (152, 350))

    bgy1 = 0
    bgy2 = road.get_height() * -1

    obstacles = []

    char.lives = 3

    ticks = 0

    if score > high_score:
        high_score_2 = open(os.path.join("assets", "highscore.txt"), "w")
        high_score_2.write(str(score))
        high_score_2.close()
        high_score = score

    char.speed = 1
    enemy_speed = 5

    mouseclick = pygame.mouse.get_pressed()

    if mouseclick[0]:
        score = 0
        gameOver = False


def menu():
    global menuOpen, enemy_speed, credit, credit_timer
    mouseclick = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if not credit:
        screen.blit(text.render("God", True, white), (185, 50))
        screen.blit(text.render("Speed", True, white), (150, 100))
        screen.blit(small_text.render("Click to play", True, white), (152, 350))
        screen.blit(small_text.render("Credit", True, white), (5, 448))
        screen.blit(medium_text.render(str(high_score), True, white), (5, 0))
    else:
        screen.fill(blue)
        screen.blit(small_text.render("The following work was used", True, white), (55, 10))
        screen.blit(small_text.render("Go Back", True, white), (5, 448))
        md.set_area(screen, 0, 40, width=500, height=415)
        md.set_color_background(25, 99, 145)
        md.set_color_font(255, 255, 255)
        md.display(pygame.event.get(), mouse_x, mouse_y, mouseclick)

    char.speed = 1
    enemy_speed = 5
    credit_timer -= 1

    if credit_timer <= 0:
        credit_timer = 0

    if mouseclick[0]:
        pos = pygame.mouse.get_pos()
        if pos[0] < 90 and pos[1] > 450 and not credit and credit_timer <= 0:
            credit_timer += 10
            credit = True
        elif pos[0] < 100 and pos[1] > 450 and credit and credit_timer <= 0:
            credit_timer += 10
            credit = False
        elif not credit and credit_timer <= 0:
            pygame.mixer.music.stop()
            menuOpen = False


while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == USEREVENT + 1:
            car_stage += 1
        if e.type == USEREVENT + 2:
            if char.speed < 6.9:
                char.speed += 0.1
            if enemy_speed < 10:
                enemy_speed += 0.1
        if e.type == USEREVENT + 4 and ticks <= 40 and not gameOver and not menuOpen:
            obstacle()
        if e.type == USEREVENT + 5 and 41 <= ticks <= 80 and not gameOver and not menuOpen:
            obstacle()
        if e.type == USEREVENT + 6 and 81 <= ticks <= 99 and not gameOver and not menuOpen:
            obstacle()
        if e.type == USEREVENT + 7 and ticks >= 100 and not gameOver and not menuOpen:
            obstacle()
        if e.type == USEREVENT + 3 and not menuOpen and not gameOver:
            ticks += 1

    if not gameOver and not menuOpen:
        bgy1 += char.speed
        bgy2 += char.speed

        if car_stage >= 2:
            car_stage = 0

        score += 1

        movement()

    redraw()

pygame.quit()
quit()
