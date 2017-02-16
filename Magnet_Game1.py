'''Simple Game'''

import pygame, sys      #import pygame
import numpy as np

pygame.init()      #initialise pygame

screen_size = [800, 600] #define screen size

screen = pygame.display.set_mode(screen_size) #open window

pygame.mouse.set_visible(0)  #make mouse invisible

clock = pygame.time.Clock() #initialise clock

BALL = pygame.image.load("Ball.png").convert_alpha()  #load image of ball
BALL.set_colorkey([255,255,255])                        #set background to white
PLUS = pygame.image.load("PostiveCharge.png")
MINUS = pygame.image.load("NegativeCharge.png")


BALL_SIZE = [22, 22]
PLUS_SIZE = [22,22]
MINUS_SIZE =[22,22]

x, y = 0, 0         #define x and y

x_direction, y_direction = 1, 1   #define x and y directions

myriadProFont=pygame.font.SysFont("Myriad Pro", 48)
Text=myriadProFont.render("YOU WIN",1,(250,250,250))

'''For an electric dipole the equation for the electric field is 1/2pie0* qd/z^3
where d is the distance between the charges and z is the distance between the point
and the centre of the dipole'''

#make it so they are 100 pixels apart i.e 50 pixels either side of centre of screen
#centre of screen is 400,300 so need to be 350-half width and 450 plus half width
#y is 300-half height
p_xpos, p_ypos =339, 289
m_xpos, m_ypos = 461, 289
#call 1/2pie0 constant which is 2 times coulombs constant
K = 2* 8.988e9 #coulombs constant*2
d=100
q=1.6e-19
PLUS_LEFT = p_xpos
PLUS_RIGHT = p_xpos + PLUS_SIZE[0]
PLUS_TOP = p_ypos
PLUS_BOTTOM = p_ypos + PLUS_SIZE[1]
PLUS_CENTRE = [(PLUS_LEFT+PLUS_RIGHT)/2, (PLUS_TOP+PLUS_BOTTOM)/2]
MINUS_LEFT = m_xpos
MINUS_RIGHT = m_xpos + MINUS_SIZE[0]
MINUS_TOP = m_ypos
MINUS_BOTTOM = m_ypos + MINUS_SIZE[1]
MINUS_CENTRE = [(MINUS_LEFT+MINUS_RIGHT)/2, (MINUS_TOP+MINUS_BOTTOM)/2]
DIPOLE_CENTRE = [400,300]

def z(x,y,x1,y1):
    xdif = abs(x1-x1)
    ydif = abs(y1-y)
    return np.sqrt(xdif**2 + ydif**2)

def E(z,K,q,d):
    return K*q*d/z**3

#main game loop
while 1:

    clock.tick(60)

    screen.fill([255,255,255])       #set background to white

    screen.blit(BALL, (x, y))        #put images on screen
    screen.blit(PLUS, (p_xpos,p_ypos))
    screen.blit(MINUS, (m_xpos,m_ypos))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:sys.exit()     #if close pressed then quit game

    x += 1.5*x_direction              #set velocity of ball
    y += 1.5*y_direction
    BALL_VEL = np.array([x,y])            #vector for ball velocity


    #field around magnet based on electric dipole equation

    #then use F=qE to find force on ball to put it in now direction

    # define edges of images
    # ball
    BALL_LEFT = x
    BALL_RIGHT = x + BALL_SIZE[0]
    BALL_TOP = y
    BALL_BOTTOM = y + BALL_SIZE[1]
    B_CENTRE_X = (BALL_LEFT+BALL_RIGHT)/2
    B_CENTRE_Y = (BALL_TOP+BALL_BOTTOM)/2
    BALL_CENTRE = [B_CENTRE_X, B_CENTRE_Y]

    #stop ball going off screen
    if BALL_RIGHT >= 800 or BALL_LEFT <= 0:
        x_direction *= -1
    if BALL_BOTTOM >= 600 or BALL_TOP <= 0:
        y_direction *= -1

    Z = z(B_CENTRE_X, B_CENTRE_Y, DIPOLE_CENTRE[0], DIPOLE_CENTRE[1])
    E_field = E(Z,K,q,d)
    print(E_field)

    pygame.display.update()






