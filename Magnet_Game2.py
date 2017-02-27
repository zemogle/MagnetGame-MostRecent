'''Simple Game'''

'''import libraries'''
import pygame, sys          #import pygame
import numpy as np          #import numpy


screen_size = [750, 750]    #define screen size


'''Define variables'''
BALL_SIZE = [22, 22]
MAGNET_SIZE = [100, 25]

x, y = 0, 0                       #define x and y position of Ball

x_direction, y_direction = 1, 1   #define x and y direction of ball velocity

mov_x, mov_y = 0, 0                #define x and y velocity of magnet

p1, p2 = 325, 375                 #define position of magnet
#define colours
YELLOW = [0,255,0]
ORANGE = [0,0,255]
RED = [255,0,0]

pygame.init()               #initialise pygame
screen = pygame.display.set_mode(screen_size) #open window
im1= pygame.Surface(screen.get_size())
im1.fill((100, 0, 0))

pygame.mouse.set_visible(0) #make mouse invisible

clock = pygame.time.Clock() #initialise clock

'''Load images'''
BALL = pygame.image.load("Ball.png").convert_alpha()  #load image of ball
BALL.set_colorkey([255,255,255])                      #set background to white
MAGNET= pygame.image.load("Magnet.png").convert_alpha() #load image of magnet
MAGNET.set_colorkey([255,255,255])



'''Function to find distance between images'''
def z(x,y):
    dif = abs(y-x)
    return dif

'''Function to find electric field'''
def E(z, q, d):  # equation from haliday p564
    ep0 = 1
    pi = 1 #np.pi
    return (q * d)/(2*pi*ep0*z)


'''Function to Plot Electric Field'''
def Plot(screen):
    gridx=(np.linspace(0,750,750))
    gridy=(np.linspace(0,750,750))
    Efield = np.sqrt(Ex ** 2 + Ey ** 2)
    np.clip(Efield, 0, 70)
    for i in range(750):
        for j in range(750):
            Ef = E(np.sqrt(z_x[i] ** 2 + z_y[j] ** 2), q,d)
            if 0 <= Ef <= 1:
                screen.set_at([int(gridx[i]), int(gridy[j])], YELLOW)
            if 1 < Ef <= 10:
                screen.set_at([int(gridx[i]), int(gridy[j])], ORANGE)
            else:
                screen.set_at([int(gridx[i]), int(gridy[j])], RED)

    return




'''Main game loop'''
while 1:

    clock.tick(60)                   #set clock

    screen.fill([255,255,255])       #set background to white

    screen.blit(im1, (0, 0))
    screen.blit(BALL, (x, y))        #put images on screen
    screen.blit(MAGNET, (p1, p2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:sys.exit()     #if close pressed then quit game
        if event.type==pygame.KEYDOWN:              #moving dipole
            if event.key==pygame.K_d and MAGNET_RIGHT < 750:
                mov_x += 6
            if event.key==pygame.K_a and MAGNET_LEFT >0:
                mov_x -= 6
            if event.key==pygame.K_s and MAGNET_BOTTOM < 750:
                mov_y += 6
            if event.key==pygame.K_w and MAGNET_TOP > 0:
                mov_y -= 6
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_d:
                mov_x *= 0
            if event.key==pygame.K_a:
                mov_x *=0
            if event.key==pygame.K_w:
                mov_y *=0
            if event.key==pygame.K_s:
                mov_y *=0
            Plot(screen)


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

    q=1
    k=1
    m=1

    '''electric field'''
    Ex=E(z_x,q,d)
    Ey=E(z_y,q,d)

    '''Acceleration'''
    ax = (-q * Ex/m)
    ay = (-q*Ey/m)


    for i in range(750):
        if np.floor(x) == np.floor(X_pixel[i]):
            x += ax[i]*x_direction

    for j in range(750):
        if np.floor(y) == np.floor(Y_pixel[j]):
            y += ay[j]*x_direction

    q=1
    k=1
    m=1

    '''electric field'''
    Ex=E(z_x,q,d)
    Ey=E(z_y,q,d)

    '''Acceleration'''
    ax = (-q * Ex/m)
    ay = (-q*Ey/m)


    for i in range(750):
        if np.floor(x) == np.floor(X_pixel[i]):
            x += ax[i]*x_direction

    for j in range(750):
        if np.floor(y) == np.floor(Y_pixel[j]):
            y += ay[j]*x_direction

    gridx=(np.linspace(0,750,50))
    gridy=(np.linspace(0,750,50))
    Efield = np.sqrt(Ex ** 2 + Ey ** 2)
    np.clip(Efield, 0, 70)
    for i in range(50):
        for j in range(50):
            if 0 <= Efield[i] <= 1:
                screen.set_at([int(gridx[i]), int(gridy[j])], YELLOW)
            if 1 < Efield[i] <= 10:
                screen.set_at([int(gridx[i]), int(gridy[j])], ORANGE)
            else:
                screen.set_at([int(gridx[i]), int(gridy[j])], RED)

    #define edges of ballaa
    BALL_LEFT = x
    BALL_RIGHT = x + BALL_SIZE[0]
    BALL_TOP = y
    BALL_BOTTOM = y + BALL_SIZE[1]
    B_CENTRE_X = (BALL_LEFT+BALL_RIGHT)/2
    B_CENTRE_Y = (BALL_TOP+BALL_BOTTOM)/2
    BALL_CENTRE = [B_CENTRE_X, B_CENTRE_Y]

    #stop magnet going off screen
    if MAGNET_RIGHT >= 750 or MAGNET_LEFT <= 0:
        mov_x = 0
    if MAGNET_BOTTOM >= 750 or MAGNET_TOP <= 0:
        mov_y = 0

    #stop ball going off screen
    if BALL_RIGHT >= 750 or BALL_LEFT <= 0:
        x_direction *= -1
    if BALL_BOTTOM >= 750 or BALL_TOP <= 0:
        y_direction *= -1

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

    pygame.display.update()
