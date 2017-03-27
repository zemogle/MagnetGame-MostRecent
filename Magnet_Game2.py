'''Simple Game'''

'''import libraries'''
import pygame, sys          #import pygame
import numpy as np          #import numpy

pygame.init()               #initialise pygame

screen_size = [750, 750]    #define screen size

screen = pygame.display.set_mode(screen_size) #open window

pygame.mouse.set_visible(0) #make mouse invisible

clock = pygame.time.Clock() #initialise clock

'''Define variables'''
BALL_SIZE = [22, 22]
MAGNET_SIZE = [100, 25]

x, y = 0, 0                       #define x and y position of Ball

x_direction, y_direction = 1, 1   #define x and y direction of ball velocity

mov_x, mov_y = 0, 0                #define x and y velocity of magnet

p1, p2 = 325, 375                 #define position of magnet

#define colours
YELLOW = [255,255,0]
ORANGE = [230,126,32]
RED = [255,0,0]

q = 1e4
d=50
k = 1
m = 1
ep0 = 1
pi = 1  # np.pi
# myriadProFont=pygame.font.SysFont("Myriad Pro", 48)
# Text=myriadProFont.render("YOU WIN",1,(250,250,250))
#
# MENU = pygame.image.load("MenuButton.png").convert_alpha()
position = [300, 200]
# MENU_SIZE = [200, 50]

class Ball(pygame.sprite.Sprite):

    def __init__(self, color, width, height, xpos,ypos):
        super().__init__()
        self.image = pygame.image.load("Ball.png").convert_alpha()
        self.image.set_colorkey([255,255,255])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x_direction = 1
        self.y_direction = 1
        self.centreX = (self.rect.x + (self.rect.x + BALL_SIZE[0])) / 2.
        self.centreY = (self.rect.y + (self.rect.y + BALL_SIZE[1])) / 2.

    def render(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    #def update(self):
        #self.rect.x += self.x_direction
        #self.rect.y += self.y_direction

    def accel(self, sprite_list, q, d, m):
        for magnet in sprite_list:
            self.centreX = (self.rect.x + (self.rect.x + BALL_SIZE[0])) / 2.
            self.centreY = (self.rect.y + (self.rect.y + BALL_SIZE[1])) / 2.
            z = np.sqrt(abs(self.centreX - magnet.centreX)**2 + (self.centreY - magnet.centreY)**2) #use pythag
            E = (q * d) / (2 * pi * ep0 * (z ** 3))  # E field
            a =  q * E / m
            a = max(0, min(a,5))
            print(a)
            self.rect.x += a*self.x_direction
            self.rect.y += a*self.y_direction

    def limit(self, screensize, objectsize):
        if self.rect.x  + objectsize[0] > screensize[0] or self.rect.x < 0 :
            self.x_direction *= -1
        if self.rect.y + objectsize[1] > screensize[1] or self.rect.y < 0:
            self.y_direction *= -1

    def collide(self, sprite_list):
        if pygame.sprite.spritecollide(self,sprite_list,False):
            self.x_direction *= -1
            self.y_direction *= -1


class Magnet(pygame.sprite.Sprite):

    def __init__(self, color, width, height, xpos,ypos):
        super().__init__()
        self.image = pygame.image.load("Magnet.png").convert_alpha()
        self.image.set_colorkey([255, 255, 255])
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        self.centreX = (self.rect.x + (self.rect.x + MAGNET_SIZE[0])) / 2
        self.centreY = (self.rect.y + (self.rect.y + MAGNET_SIZE[1])) / 2

    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = 6
        if key[pygame.K_d]:
            self.rect.x += dist
        elif key[pygame.K_a]:
            self.rect.x -= dist
        if key[pygame.K_s]:
            self.rect.y += dist
        elif key[pygame.K_w]:
            self.rect.y -= dist
        self.rect.x = max(0,min(self.rect.x, screen_size[0]-MAGNET_SIZE[0]))
        self.rect.y = max(0, min(self.rect.y, screen_size[1]- MAGNET_SIZE[1]))

    def render(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
'''
def GetMenuScreen(screen, button, position):
    screen.fill([255, 255, 255])
    screen.blit(button, position)
    pygame.mouse.set_visible(1)

def GetGameScreen(screen, ball,position1, magnet, position2, target, position3):
    screen.fill([255, 255, 255])
    pygame.mouse.set_visible(0)
    screen.blit(ball, position1)
    screen.blit(magnet, position2)
    screen.blit(target, position3)

def GetWinScreen(screen, text,position, button1, position1, button2, position2):
    screen.fill([0,0,0])
    screen.blit(text, position)
    screen.blit(button1, position1)
    screen.blit(button2, position2)
'''

'''Function to Plot Electric Field'''
def Plot(Ex,Ey,X_pixel,Y_pixel):
    Efield=np.sqrt(Ex**2 + Ey**2)
    np.clip(Efield, 0, 70)
    for i in X_pixel:
        for j in Y_pixel:
            if 0 <= Efield <= 25:
                screen.set_at(X_pixel[i], Y_pixel[j], YELLOW)
            if 26 <= Efield <= 50:
                screen.set_at(X_pixel[i], Y_pixel[j], ORANGE)
            else:
                screen.set_at(X_pixel[i], Y_pixel[j], RED)
    return Efield


BALL = Ball([255,255,255], BALL_SIZE[0], BALL_SIZE[1],x,y)

MAGNET = Magnet([255,255,255], MAGNET_SIZE[0], MAGNET_SIZE[1], p1,p2)

magnet_list = pygame.sprite.Group()
magnet_list.add(MAGNET)
ball_list = pygame.sprite.Group()
ball_list.add(BALL)

'''Main game loop'''
while 1:

    clock.tick(60)                   #set clock

    screen.fill([255,255,255])       #set background to white

    for event in pygame.event.get():
        if event.type == pygame.QUIT:sys.exit()     #if close pressed then quit game

    MAGNET.render(screen)
    BALL.render(screen)
    MAGNET.handle_keys()
    BALL.accel(magnet_list,q,d,m)
    BALL.limit(screen_size,BALL_SIZE)
    BALL.collide(magnet_list)

    pygame.display.update()
