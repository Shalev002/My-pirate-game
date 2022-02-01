
from msilib.schema import Class
from operator import le
import pygame
import os 
import time
import random

pygame.font.init()

WIDTH = 750
HEIGHT = 750

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pirate Ship')


#טעינת תמונות
RED_MONSTER = pygame.image.load(os.path.join('assests', 'pixel_ship_red_small.png'))
GREEN_MONSTER = pygame.image.load(os.path.join('assests', 'pixel_ship_green_small.png'))
BLUE_MONSTER = pygame.image.load(os.path.join('assests', 'pixel_ship_blue_small.png'))

#שחקן 
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join('assests', 'pixel_ship_yellow.png'))

#יריות
RED_LASER = pygame.image.load(os.path.join('assests', 'pixel_laser_red.png'))
YELLOW_LASER = pygame.image.load(os.path.join('assests', 'pixel_laser_yellow.png'))
BLUE_LASER = pygame.image.load(os.path.join('assests', 'pixel_laser_blue.png'))
GREEN_LASER = pygame.image.load(os.path.join('assests', 'pixel_laser_green.png'))

#קרע
BG = pygame.transform.scale(pygame.image.load(os.path.join('assests', 'background-black.png')), (WIDTH, HEIGHT))

class Ship:
    def __init__(self,x , y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.laser = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


class Enemy(Ship):
    COLOR_MAP = {
                'red': (RED_MONSTER, RED_LASER),
                'green': (GREEN_MONSTER, GREEN_LASER),
                'blue': (BLUE_MONSTER, BLUE_LASER)
                }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont('arial.ttf', 50)
    lost_font = pygame.font.SysFont('arial.ttf', 60)


    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 6
    
    player = Player(300, 650)

    clock = pygame.time.Clock()

    lost = False

    def redraw_window():
        WIN.blit(BG, (0,0))

        lives_label = main_font.render(f'Lives: {lives}', 1, (229,229,17))
        level_label = main_font.render(f'Level: {level}', 1, (229,229,17))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10,10))

        for enemy in enemies:
            enemy.draw(WIN)        

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render('You Die Loser!!', 1, (229,229,17))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()


    while run:
        clock.tick(FPS)

        if lives <= 0 or player.health <= 0:
            lost = True

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500*level/5, -100), random.choice(['red', 'green', 'blue']))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key = pygame.key.get_pressed()
        if key[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if key[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel

        for enemy in enemies:
            enemy.move(enemy_vel)
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        redraw_window()



main()