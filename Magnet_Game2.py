'''Simple Game'''

'''import libraries'''
import pygame, sys          #import pygame
import numpy as np          #import numpy
from pygame.sprite import Sprite

pygame.init()               #initialise pygame

screen_size = [750, 750]    #define screen size

screen = pygame.display.set_mode(screen_size) #open window

pygame.mouse.set_visible(0) #make mouse invisible

clock = pygame.time.Clock() #initialise clock

'''Load images'''
# BALL = pygame.image.load("Ball.png").convert_alpha()  #load image of ball
# BALL.set_colorkey([255,255,255])                      #set background to white
MAGNET= pygame.image.load("Magnet.png").convert_alpha() #load image of magnet
MAGNET.set_colorkey([255,255,255])

'''Define variables'''
BALL_SIZE = [22, 22]
MAGNET_SIZE = [100, 25]

class Ball(Sprite):
    """
    This class represents the ball.
    It derives from the "Sprite" class in Pygame.
    """
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """

        # Call the parent class (Sprite) constructor
        Sprite.__init__(self)
        self.image = pygame.image.load("Ball.png").convert_alpha()
        #self.image.set_colorkey([255,255,255])
        self.rect = self.image.get_rect()
        self.x = 0
        self.y = 0

    def blit(self, surface):
        surface.blit(self.image, (self.x, self.y))

class Magnet(Sprite):
    """This class represents the magnet.
    It derives from the Sprie class in Pygame"""

    def __init__(self, color, width, height):
        Sprite.__init__(self)
        self.image = pygame.image.load("Magnet.png").convert_alpha()
        #self.image.set_colorkey([255, 255, 255])
        self.rect = self.image.get_rect()
    def update(self):
        pass


    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = 6
        if key[pygame.K_d]:
            self.rect.x += dist
        elif key[pygame.K_a]:
            self.rect.x -= dist
        if key[pygame.K_w]:
            self.rect.y += dist
        elif key[pygame.K_s]:
            self.rect.y -= dist

    def blit(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))



'''def getsize(objectsize,position):
    LEFT=position[0]
    RIGHT=position[0] + objectsize[0]
    TOP=position[1]
    BOTTOM=position[1] + objectsize[1]
    return [LEFT,RIGHT,TOP,BOTTOM]'''


def screenlimit(size, screensize, velocity):
    if  size[1] >= screensize[0] or size[0] <= 0:
        return velocity[0] == 0
    if size[3] >= screensize[1] or size[2] <= 0:
        return velocity[1] == 0


x, y = 0, 0                       #define x and y position of Ball

x_direction, y_direction = 1, 1   #define x and y direction of ball velocity

mov_x, mov_y = 0, 0                #define x and y velocity of magnet

p1, p2 = 325, 375                 #define position of magnet

#define colours
YELLOW = [255,255,0]
ORANGE = [230,126,32]
RED = [255,0,0]

q = 1
k = 1
m = 1
# myriadProFont=pygame.font.SysFont("Myriad Pro", 48)
# Text=myriadProFont.render("YOU WIN",1,(250,250,250))
#
# MENU = pygame.image.load("MenuButton.png").convert_alpha()
position = [300, 200]
# MENU_SIZE = [200, 50]

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


'''Function to find distance between images'''
def z(x,y):
    dif = abs(y-x)
    return dif

'''Function to find electric field'''
def E(z, q, d):  # equation from haliday p564
    ep0 = 1
    pi = 1 #np.pi
    return (q * d)/(2*pi*ep0*(z**3))


def accel(q, E, m):
    return -q * E / m


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

def MovMag(objectsize, velocity, screensize):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_d and objectsize[1] < screen_size[0]:
            velocity[0] += 6
        if event.key == pygame.K_a and objectsize[0] > 0:
            velocity[0] -= 6
        if event.key == pygame.K_s and objectsize[3] < screen_size[1]:
            velocity[1] += 6
        if event.key == pygame.K_w and objectsize[2] > 0:
            velocity[1] -= 6
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_d:
            velocity[0] *= 0
        if event.key == pygame.K_a:
            velocity[0] *= 0
        if event.key == pygame.K_w:
            velocity[1] *= 0
        if event.key == pygame.K_s:
            velocity[1] *= 0


def Collide(magsize, ballsize, velocity):
    # collide on top
    if magsize[2] <= ballsize[3] <= magsize[3] and magsize[0] <= ballsize[0] <= magsize[1] or magsize[0] <= ballsize[
        1] <= magsize[1]:
        velocity[1] *= -1
    # collide on bottom
    if magsize[2] <= ballsize[2] <= magsize[3] and magsize[0] <= ballsize[0] <= magsize[1] or magsize[0] <= ballsize[
        1] <= magsize[1]:
        velocity[1] *= -1
    # collide on left
    if magsize[0] <= ballsize[1] <= magsize[1] and magsize[2] <= ballsize[2] <= magsize[3] or magsize[2] <= ballsize[
        3] <= magsize[3]:
        velocity[0] *= -1
    # collide on left
    if magsize[0] <= ballsize[0] <= magsize[1] and magsize[2] <= ballsize[2] <= magsize[3] or magsize[2] <= ballsize[
        3] <= magsize[3]:
        velocity[0] *= -1

balls = pygame.sprite.Group()

ball = Ball()

balls.update()


'''Main game loop'''
while 1:

    clock.tick(60)                   #set clock

    screen.fill([255,255,255])       #set background to white

    screen.blit(BALL, (x, y))        #put images on screen
    screen.blit(MAGNET, (p1, p2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:sys.exit()     #if close pressed then quit game

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and position[0] <= Cx <= position[0] + MENU_SIZE[0] and position[1] <= Cy <= position[1] + MENU_SIZE[1]:
                GetGameScreen(screen, BALL, [0, 0], MAGNET, [p1, p2], TARGET, [pos1, pos2])

        MovMag(getsize(MAGNET_SIZE,[p1,p2]), [mov_x,mov_y], screen_size)

    x += 1.5*x_direction                      #set velocity of ball
    y += 1.5*y_direction

    # define edges of magnet
    MAGNET_LEFT = p1
    MAGNET_RIGHT = p1 + MAGNET_SIZE[0]
    MAGNET_TOP = p2
    MAGNET_BOTTOM = p2 + MAGNET_SIZE[1]

    DIPOLE_CENTRE = [(MAGNET_LEFT + MAGNET_RIGHT)/2, (MAGNET_BOTTOM + MAGNET_TOP)/2]

    #move magnet
    p1 += mov_x
    p2 += mov_y

    n = 750
    d = 25

    X_pixel = np.linspace(0, 750, n)
    Y_pixel = np.linspace(0, 750, n)
    DIPOLE_CENTRE_X = DIPOLE_CENTRE[0]* np.ones(n)
    DIPOLE_CENTRE_Y = DIPOLE_CENTRE[1]* np.ones(n)

    z_x = 0.1 * np.floor(DIPOLE_CENTRE_X - X_pixel)
    z_y = 0.1 * np.floor(DIPOLE_CENTRE_Y - Y_pixel)

    '''Acceleration'''
    ax = accel(q,E(z_x,q,d),m)
    ay = accel(q,E(z_y,q,d),m)


    for i in range(750):
        if np.floor(x) == np.floor(X_pixel[i]):
            x += ax[i]*x_direction

    for j in range(750):
        if np.floor(y) == np.floor(Y_pixel[j]):
            y += ay[j]*x_direction

    #plot
    # Plot(Ex,Ey,X_pixel,Y_pixel)

    #define edges of balls
    BALL_LEFT = x
    BALL_RIGHT = x + BALL_SIZE[0]
    BALL_TOP = y
    BALL_BOTTOM = y + BALL_SIZE[1]
    B_CENTRE_X = (BALL_LEFT+BALL_RIGHT)/2
    B_CENTRE_Y = (BALL_TOP+BALL_BOTTOM)/2
    BALL_CENTRE = [B_CENTRE_X, B_CENTRE_Y]

    screenlimit(getsize(MAGNET_SIZE, [p1,p2]), screen_size, [mov_x,mov_y])


    #stop ball going off screen
    if BALL_RIGHT >= 750 or BALL_LEFT <= 0:
        x_direction *= -1
    if BALL_BOTTOM >= 750 or BALL_TOP <= 0:
        y_direction *= -1

    Collide(getsize(MAGNET_SIZE,[p1,p2]),getsize(BALL_SIZE,[x,y]), [x_direction,y_direction])

    pygame.display.update()
