'''Simple Game'''

'''import libraries'''
import pygame, sys          #import pygame
import numpy as np          #import numpy

pygame.init()               #initialise pygame

screen_size = [750, 750]    #define screen size

screen = pygame.display.set_mode(screen_size) #open window

pygame.mouse.set_visible(0) #make mouse invisible

clock = pygame.time.Clock() #initialise clock

'''Load images'''
BALL = pygame.image.load("Ball.png").convert_alpha()  #load image of ball
BALL.set_colorkey([255,255,255])                      #set background to white
PLUS = pygame.image.load("PostiveCharge.png")         #load positive charge
MINUS = pygame.image.load("NegativeCharge.png")       #load negative charge
MAGNET= pygame.image.load("Magnet.png").convert_alpha() #load image of magnet
MAGNET.set_colorkey([255,255,255])

# INitialising variables
PLUS_LEFT = 0
PLUS_RIGHT = 0
PLUS_TOP = 0
PLUS_BOTTOM = 0
PLUS_CENTRE = 0
MINUS_LEFT = 0
MINUS_RIGHT = 0
MINUS_TOP = 0
MINUS_BOTTOM = 0
MINUS_CENTRE = 0
DIPOLE_CENTRE = 0

'''Define variables'''
BALL_SIZE = [22, 22]
PLUS_SIZE = [22,22]
MINUS_SIZE =[22,22]
MAGNET_SIZE = [100, 25]

x, y = 0, 0                       #define x and y position of Ball

x_direction, y_direction = 1, 1   #define x and y direction of ball velocity

Pmove_y, Pmove_x = 0, 0           #define x and y velocity of plus
Mmove_y, Mmove_x = 0, 0           #define x and y velocity of minus

mov_x, mov_y = 0, 0                #define x and y velocity of magnet

p_xpos, p_ypos = 325, 375         #define a and y position of plus
m_xpos, m_ypos = 425, 375         #define a and y position of minus
p1, p2 = 325, 375                 #define position of magnet


'''Function to find distance between images'''
def z(x,y):
    dif = abs(y-x)
    return dif


def E(z, q, d):  # equation from haliday p564
    ep0 = 8.85e-12
    return q * d / (2 * np.pi * ep0 * z ** 3)

'''Plot Electric Field'''
#define grid
n = 50
x_pixel = np.linspace(0, 6, n)
y_pixel = np.linspace(0, 6, n)
q=1
d=50
CENTRE = [3,3]
S_x = CENTRE[0] - x_pixel
S_y = CENTRE[1] - y_pixel
Ex = np.floor(abs(E(S_x, q, d))/1e10)
Ey = np.floor(abs(E(S_y, q, d))/1e10)
#EX=np.clip(Ex,0,750)
#EY=np.clip(Ey, 0, 750)
E_mag = np.sqrt(Ex ** 2 + Ey ** 2)

pos=np.zeros(n)





'''Main game loop'''
while 1:

    clock.tick(60)                   #set clock

    screen.fill([255,255,255])       #set background to white

    screen.blit(BALL, (x, y))        #put images on screen
    screen.blit(PLUS, (p_xpos,p_ypos))
    screen.blit(MINUS, (m_xpos,m_ypos))
    screen.blit(MAGNET, (p1, p2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:sys.exit()     #if close pressed then quit game
        if event.type==pygame.KEYDOWN:              #moving dipole
            if event.key==pygame.K_d and MINUS_RIGHT < 750:
                Mmove_x += 6
                Pmove_x += 6
                mov_x += 6
            if event.key==pygame.K_a and PLUS_LEFT >0:
                Mmove_x -= 6
                Pmove_x -= 6
                mov_x -= 6
            if event.key==pygame.K_s and MINUS_BOTTOM < 750:
                Mmove_y += 6
                Pmove_y += 6
                mov_y += 6
            if event.key==pygame.K_w and MINUS_TOP > 0:
                Mmove_y -= 6
                Pmove_y -= 6
                mov_y -= 6
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_d:
                Mmove_x *= 0
                Pmove_x *= 0
                mov_x *= 0
            if event.key==pygame.K_a:
                Mmove_x *= 0
                Pmove_x *= 0
                mov_x *=0
            if event.key==pygame.K_w:
                Mmove_y *= 0
                Pmove_y *= 0
                mov_y *=0
            if event.key==pygame.K_s:
                Mmove_y *= 0
                Pmove_y *= 0
                mov_y *=0


    x += 1.5*x_direction                      #set velocity of ball
    y += 1.5*y_direction

    BALL_VEL=np.array([x_direction, y_direction])  #velocity of ball as vector

    #move dipole
    p_xpos += Pmove_x
    p_ypos += Pmove_y
    m_xpos += Mmove_x
    m_ypos += Mmove_y

    #define edges of ball
    BALL_LEFT = x
    BALL_RIGHT = x + BALL_SIZE[0]
    BALL_TOP = y
    BALL_BOTTOM = y + BALL_SIZE[1]
    B_CENTRE_X = (BALL_LEFT+BALL_RIGHT)/2
    B_CENTRE_Y = (BALL_TOP+BALL_BOTTOM)/2
    BALL_CENTRE = [B_CENTRE_X, B_CENTRE_Y]

    # define edges of dipole
    PLUS_LEFT = p_xpos
    PLUS_RIGHT = p_xpos + PLUS_SIZE[0]
    PLUS_TOP = p_ypos
    PLUS_BOTTOM = p_ypos + PLUS_SIZE[1]
    PLUS_CENTRE = [(PLUS_LEFT + PLUS_RIGHT) / 2, (PLUS_TOP + PLUS_BOTTOM) / 2]
    MINUS_LEFT = m_xpos
    MINUS_RIGHT = m_xpos + MINUS_SIZE[0]
    MINUS_TOP = m_ypos
    MINUS_BOTTOM = m_ypos + MINUS_SIZE[1]
    MINUS_CENTRE = [(MINUS_LEFT + MINUS_RIGHT) / 2, (MINUS_TOP + MINUS_BOTTOM) / 2]
    DIPOLE_CENTRE = [(MINUS_CENTRE[0] + PLUS_CENTRE[0]) / 2, ((MINUS_TOP + MINUS_BOTTOM) / 2)]

    d = z(MINUS_CENTRE[0], DIPOLE_CENTRE[0])  # distance between plus and minus

    # define edges of magnet
    MAGNET_LEFT = p1
    MAGNET_RIGHT = p1 + MAGNET_SIZE[0]
    MAGNET_TOP = p2
    MAGNET_BOTTOM = p2 + MAGNET_SIZE[1]

    #stop magnet going off screen
    if MAGNET_RIGHT >= 800 or MAGNET_LEFT <= 0:
        move_x = 0
    if MAGNET_BOTTOM >= 600 or MAGNET_TOP <= 0:
        move_y = 0

    #stop ball going off screen
    if BALL_RIGHT >= 750 or BALL_LEFT <= 0:
        x_direction *= -1
    if BALL_BOTTOM >= 750 or BALL_TOP <= 0:
        y_direction *= -1

    #stop dipole going off screen
    if MINUS_RIGHT >= 750 or PLUS_LEFT <= 0:
        Pmove_x *= 0
        Mmove_x *= 0
    if PLUS_BOTTOM >= 750 or PLUS_TOP <= 0:
        Pmove_y *= 0
        Mmove_y *= 0

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

    '''For an electric dipole the equation for the electric field is 1/2pie0* qd/z^3
    where d is the distance between the charges and z is the distance between the point
    and the centre of the dipole'''

    #find separation
    z_x = z(DIPOLE_CENTRE[0],B_CENTRE_X)    #separation in x direction
    z_y = z(DIPOLE_CENTRE[1],B_CENTRE_Y)    #separation in y direction
    Z = np.sqrt(z_x**2 + z_y**2)            #separation

    n=50
    X_pixel = np.linspace(0, 750, n)
    Y_pixel = np.linspace(0, 750, n)

    '''Define array for each distance from each pixel to dipole centre'''

    r = np.zeros(n)

    '''Find E field at each pixel'''
    q=1
    k=1e9
    m=1e8
    Eyy=np.zeros(n)
    Exx=np.zeros(n)
    a_x=np.zeros(n)
    a_y=np.zeros(n)
    S_X=np.zeros(n)
    S_Y=np.zeros(n)

    '''Use Haliday equation to calculate magnitude of field at each pixel'''

    aX=np.ones(n)
    aY=np.ones(n)

    for i in range(n):
        S_X[i] = DIPOLE_CENTRE[0]-X_pixel[i]
        Exx[i] = E(S_X[i],q,d)
        a_x[i] = abs(-q * Exx[i] / m)
        if -2.0<=a_x[i]<=2.0:
           aX[i]=a_x[i]

        x_direction *= aX[i]

    for j in range(n):
        S_Y[j] = DIPOLE_CENTRE[1] - Y_pixel[j]
        Eyy[i] = E(S_Y[i],q,d)
        a_y[i] = abs(-q * Eyy[i] / m)
        if -2.0<=a_y[i]<=2.0:
            aY[j]=a_y[j]

        y_direction *= aY[j]

    pygame.display.update()


