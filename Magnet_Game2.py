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

q = 1
k = 1
m = 1
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
        self.x = 0
        self.y = 0
        self.x_direction = 1
        self.y_direction = 1

    def render(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def update(self):
        self.x += self.x_direction
        self.y += self.y_direction

    def limit(self, screensize, objectsize):
        if self.x  + objectsize[0] >= screensize[0] or self.x <= 0 :
            self.x_direction *= -1
        if self.y + objectsize[1] >= screensize[1] or self.y <= 0:
            self.y_direction *= -1

    def collide(self, sprite):
        if pygame.sprite.spritecollide(self, sprite, False):
            self.x_direction *= -1
            self.y_direction *= -1


class Magnet(pygame.sprite.Sprite):

    def __init__(self, color, width, height, xpos,ypos):
        super().__init__()
        self.image = pygame.image.load("Magnet.png").convert_alpha()
        self.image.set_colorkey([255, 255, 255])
        self.rect = self.image.get_rect()
        self.x = xpos
        self.y = ypos

    def handle_keys(self):
        key = pygame.key.get_pressed()
        dist = 6
        if key[pygame.K_d]:
            self.x += dist
        elif key[pygame.K_a]:
            self.x -= dist
        if key[pygame.K_s]:
            self.y += dist
        elif key[pygame.K_w]:
            self.y -= dist

    def render(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def limit(self, screensize, objectsize):
        if self.x + objectsize[0] >= screensize[0] or self.x <= 0:
            self.x += 0
        if self.y + objectsize[1] >= screensize[1] or self.y <= 0:
            self.y += 0
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

def accel(z,q, d, m):
    ep0 = 1
    pi = 1 #np.pi
    E = (q * d)/(2*pi*ep0*(z**3)) #E field
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


BALL = Ball([255,255,255], BALL_SIZE[0], BALL_SIZE[1],x,y)

MAGNET = Magnet([255,255,255], MAGNET_SIZE[0], MAGNET_SIZE[1], p1,p2)

magnet_list = pygame.sprite.Group()
magnet_list.add(MAGNET)
ball_list = pygame.sprite.Group()
ball_list.add(BALL)
all_sprites = pygame.sprite.Group()
all_sprites.add(MAGNET)
all_sprites.add(BALL)



'''Main game loop'''
while 1:

    clock.tick(60)                   #set clock

    screen.fill([255,255,255])       #set background to white

    for event in pygame.event.get():
        if event.type == pygame.QUIT:sys.exit()     #if close pressed then quit game

    MAGNET.render(screen)
    BALL.render(screen)
    MAGNET.handle_keys()
    BALL.update()
    BALL.limit(BALL_SIZE,screen_size)
    MAGNET.limit(MAGNET_SIZE,screen_size)
    BALL.collide(MAGNET)

    '''
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

    #Acceleration
    ax = accel(z_x,q,d,m)
    ay = accel(z_y,q,d,m)


    for i in range(750):
        if np.floor(x) == np.floor(X_pixel[i]):
            x += ax[i]*x_direction

    for j in range(750):
        if np.floor(y) == np.floor(Y_pixel[j]):
            y += ay[j]*x_direction

    #plot
    # Plot(Ex,Ey,X_pixel,Y_pixel)

    '''
    pygame.display.update()
