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
MAGNET= pygame.image.load("Magnet.png").convert_alpha() #load image of magnet
MAGNET.set_colorkey([255,255,255])
TARGET= pygame.image.load("Target.png").convert_alpha()
TARGET.set_colorkey([255,255,255])

BALL_SIZE = [22, 22]
MAGNET_SIZE = [100, 25]
TARGET_SIZE=[25,25]
w1,h1 =MAGNET.get_size()

x, y = 0, 0         #define x and y

x_direction, y_direction = 1, 1   #define x and y directions

p1, p2 = 350, 250       #define position of magnet

move_x, move_y = 0, 0  #define velocity of magnet

pos1, pos2 = [600,400]

myriadProFont=pygame.font.SysFont("Myriad Pro", 48)
Text=myriadProFont.render("YOU WIN",1,(250,250,250))

k=8.988e9 #coulombs constant
q=1

#main game loop
while 1:

    clock.tick(60)

    screen.fill([255,255,255])       #set background to white

    screen.blit(BALL, (x, y))        #put images on screen
    screen.blit(MAGNET, (p1, p2))
    screen.blit(TARGET, (pos1,pos2))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:sys.exit()     #if close pressed then quit game

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_d and p1 + MAGNET_SIZE[0] < 800:
                move_x += 6
            if event.key==pygame.K_a and p1 >0:
                move_x -= 6
            if event.key==pygame.K_s and p2 + MAGNET_SIZE[1] < 600:
                move_y += 6
            if event.key==pygame.K_w and p2 > 0:
                move_y -= 6
            if event.key==pygame.K_SPACE:
                MAGNET1= pygame.transform.rotate(MAGNET, 45)
                w2,h2=MAGNET1.get_size()
                screen.blit(MAGNET1,[round(p1-(w1-w2)/2), round(p2-(h1-h2)/2)])
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_d:
                move_x = 0
            if event.key==pygame.K_a:
                move_x = 0
            if event.key==pygame.K_w:
                move_y = 0
            if event.key==pygame.K_s:
                move_y = 0

    x += 1.5*x_direction              #set velocity of ball
    y += 1.5*y_direction
    BALL_VEL=np.array([x,y])            #vector for ball velocity

    p1 += move_x
    p2 += move_y

    #field around magnet based on electric dipole equation

    #then use F=qE to find force on ball to put it in now direction

    # define edges of images
    # ball
    BALL_LEFT = x
    BALL_RIGHT = x + BALL_SIZE[0]
    BALL_TOP = y
    BALL_BOTTOM = y + BALL_SIZE[1]
    # magnet
    MAGNET_LEFT = p1
    MAGNET_RIGHT = p1 + MAGNET_SIZE[0]
    MAGNET_TOP = p2
    MAGNET_BOTTOM = p2 + MAGNET_SIZE[1]
    # target
    TARGET_LEFT = pos1
    TARGET_RIGHT = pos1 + TARGET_SIZE[0]
    TARGET_TOP = pos2
    TARGET_BOTTOM = pos2 + TARGET_SIZE[1]

    #stop ball going off screen
    if BALL_RIGHT >= 800 or BALL_LEFT <= 0:
        x_direction *= -1
    if BALL_BOTTOM >= 600 or BALL_TOP <= 0:
        y_direction *= -1

    #stop magnet going off screen
    if MAGNET_RIGHT >= 800 or MAGNET_LEFT <= 0:
        move_x = 0
    if MAGNET_BOTTOM >= 600 or MAGNET_TOP <= 0:
        move_y = 0

    #collision code with magnet
    #collide on top
    if MAGNET_TOP <= BALL_BOTTOM <= MAGNET_BOTTOM  and (MAGNET_LEFT<= BALL_LEFT <= MAGNET_RIGHT or MAGNET_LEFT<= BALL_RIGHT <= MAGNET_RIGHT):
        y_direction *= -1
    #collide on bottom
    if MAGNET_TOP <= BALL_TOP <= MAGNET_BOTTOM and (MAGNET_LEFT<= BALL_LEFT <= MAGNET_RIGHT or MAGNET_LEFT<= BALL_RIGHT <= MAGNET_RIGHT):
        y_direction *= -1
    #collide on left
    if MAGNET_LEFT <= BALL_RIGHT <= MAGNET_RIGHT and (MAGNET_TOP <= BALL_TOP <= MAGNET_BOTTOM or MAGNET_TOP <= BALL_BOTTOM <= MAGNET_BOTTOM):
        x_direction *= -1
    #collide on left
    if MAGNET_LEFT <= BALL_LEFT <= MAGNET_RIGHT and (MAGNET_TOP <= BALL_TOP <= MAGNET_BOTTOM or MAGNET_TOP <= BALL_BOTTOM <= MAGNET_BOTTOM):
        x_direction *= -1

    #collision code for target
    #collide on top
    if TARGET_TOP <= BALL_BOTTOM <= TARGET_BOTTOM  and (TARGET_LEFT<= BALL_LEFT <= TARGET_RIGHT or TARGET_LEFT<= BALL_RIGHT <= TARGET_RIGHT):
        screen.fill([0, 0, 0])
        screen.blit(Text, (350, 250))
        pygame.display.update()
    #collide on bottom
    if MAGNET_TOP <= BALL_TOP <= TARGET_BOTTOM and (TARGET_LEFT<= BALL_LEFT <= TARGET_RIGHT or TARGET_LEFT<= BALL_RIGHT <= TARGET_RIGHT):
        screen.fill([0, 0, 0])
        screen.blit(Text, (350, 250))
        pygame.display.update()
    #collide on left
    if TARGET_LEFT <= BALL_RIGHT <= TARGET_RIGHT and (TARGET_TOP <= BALL_TOP <= TARGET_BOTTOM or TARGET_TOP <= BALL_BOTTOM <= TARGET_BOTTOM):
        screen.fill([0, 0, 0])
        screen.blit(Text, (350, 250))
        pygame.display.update()
    #collide on left
    if TARGET_LEFT <= BALL_LEFT <= TARGET_RIGHT and (TARGET_TOP <= BALL_TOP <= TARGET_BOTTOM or TARGET_TOP <= BALL_BOTTOM <= TARGET_BOTTOM):
        screen.fill([0, 0, 0])
        screen.blit(Text, (350, 250))
        pygame.display.update()

    pygame.display.update()


    '''Field depends on position of magnetic, i.e should move with magnet'''
    '''Need equation for shape of field in terms of p1 and p2'''





