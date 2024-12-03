import pygame
from pygame.locals import *
import time
import random

pygame.init()
pygame.mixer.init()

# Window
screen_width = 1080
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Unwelcome School")

# Constants
game_started = False
started = False
paused = False
game_over = False
score = 0
tile_size = 180
white = (255, 255, 255)
black = (0, 0, 0)
fps = 60

# Media
bg = pygame.image.load("imgs/bg.jpg")
aru = pygame.transform.scale(pygame.image.load("imgs/test.jpg"), (180, 180))
# /------------------------------------------------------------------------/
aru_jumped = pygame.image.load("imgs/aru_jumped.jpg")
aru_dead = pygame.image.load("imgs/aru_dead.jpg")
road = pygame.image.load("imgs/road.jpg")
obs_imgs = [
    pygame.image.load("imgs/obs_test_0.jpg"),
    pygame.image.load("imgs/obs_test_1.jpg"),
    pygame.image.load("imgs/obs_test_2.jpg")
]
pause_img = pygame.image.load("imgs/pause.jpg")
resume_img = pygame.image.load("imgs/resume.jpg")
restart_img = pygame.image.load("imgs/restart.jpg")
main_menu_img = pygame.image.load("imgs/main_menu.jpg")

font = pygame.font.Font(("fonts\PixeloidSans.ttf"), 74)

main_bgm = ("bgm & sfx\Blue Archive OST - Unwelcome School (ZumaTK Remix) [Hardcore].mp3")

# Classes
class Player():
    def __init__(self, x, y):
        self.image = aru
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.t_pressed = 0
        self.jumped = False
        self.first_jump = False

    def update(self):
        dx = 0
        dy = 0
        global game_over
        global t
        interval = 500

        # Controls
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.first_jump == False:
            self.first_jump = True
        if key[pygame.K_SPACE] and self.first_jump and self.jumped == False:
            if t - self.t_pressed >= interval:
                self.image = aru_jumped # Sprite for jump
                self.vel_y = -17
                self.jumped = True
                self.t_pressed = t
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_a]:
            dx -= 10
        if key[pygame.K_d]:
            dx += 10

        # Gravity
        self.vel_y += 1
        if self.vel_y > 100:
            self.vel_y = 100
        dy += self.vel_y

        self.rect.x += dx
        self.rect.y += dy

        # Temporary bottom border
        if self.rect.bottom > 540:
            self.image = aru # Default sprite
            self.rect.bottom = 540
            dy = 0

        #if self.rect.colliderect(obstacle.rect):
            #self.image = aru_dead # Sprite for game over
            #if self.image == aru_dead:
                #game_over = True

        screen.blit(self.image, self.rect)

class Obstacle():
    def __init__(self, x, y):
        self.image = random.choice(obs_imgs)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(1200, 1400)
        self.rect.y = 540

    def update(self):
        global score
        speed = -4
        base_speed = -4
        new_speed = 0
        speed_multipier = int(score/5)

        if self.rect.x < -250:
            self.image = random.choice(obs_imgs)
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(1200, 1400)
            self.rect.y = 540
            score += 1

        if speed_multipier >= 1:
            new_speed = speed_multipier * 2
            base_speed -= new_speed
            print(base_speed)

        #self.rect.x += speed 
        self.rect.x += base_speed # Remove speed or nahh

        # Temporary bottom border
        if self.rect.bottom > 540:
            self.rect.bottom = 540

        screen.blit(self.image, self.rect)

class Kivotos():
    def __init__(self, data):
        self.tile_list = []   

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = road
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

kivotos_data = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1]
]

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self):
        action = False

        # Check mouse pos.
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)
        return action
    
# Grid lines
def draw_grid():
    for line in range (0, 6):
        pygame.draw.line(screen, (white), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (white), (line * tile_size, 0), (line * tile_size, screen_height))

# Instances
kivotos = Kivotos(kivotos_data)
player = Player(100, 540)
obstacle = Obstacle(0, 0)
pause = Button(1010, 75, pause_img)
resume = Button(540, 220, resume_img)
restart = Button(540, 360, restart_img)
main_menu = Button(540, 500, main_menu_img)

# Game loop
run = True
clock = pygame.time.Clock()
while run == True:
    # Main menu
    key = pygame.key.get_pressed()
    if key[pygame.K_x]:
        game_started = True
        pygame.mixer.music.load(main_bgm)
        pygame.mixer.music.play(loops=-1)

    # Pause
    if started == True:
        if game_started == False and pause.draw() == True: # Pause btn re-click
            game_started = True
            pygame.mixer.music.unpause()
        if pause.draw() == True:                           # Pause btn
            game_started = False
            resume.draw()
            restart.draw()
            main_menu.draw()
            pygame.mixer.music.pause()
        if resume.draw() == True:                          # Resume btn
            game_started = True
            pygame.mixer.music.unpause()
        if restart.draw() == True:                         # Restart btn
            game_started = True
            player = Player(100, 540)
            obstacle = Obstacle(0, 0)
            score = 0
            pygame.mixer.music.load(main_bgm)
            pygame.mixer.music.play(loops=-1)
        if main_menu.draw() == True:                       # Main menu btn
            started = False
            screen.fill(black)
            player = Player(100, 540)
            obstacle = Obstacle(0, 0)
            score = 0

    # Start
    if game_started == True:
        started = True
        game_over = False
        t = pygame.time.get_ticks()
        clock.tick(fps)

        # Display instances
        screen.blit(bg, (0, 0))
        kivotos.draw()
        player.update()
        obstacle.update()
        pause.draw()
        draw_grid()

        # Txt displays
        score_txt = font.render(f'SCORE: {score}', True, black)
        game_over_txt = font.render("press x to try again", True, black)

        screen.blit(score_txt, (50, 50))

    # Game over
    if game_over == True:
        game_started = False
        started = False
        player = Player(100, 540)
        obstacle = Obstacle(0, 0)
        score = 0
        screen.blit(game_over_txt, (540, 360))
        pygame.mixer.music.stop()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit