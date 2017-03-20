#!/usr/bin/env python

# fake additive blending.  Using NumPy.  it doesn't clamp.
# press r,g,b

import os, pygame
from pygame.locals import *

try:
    import pygame.surfarray
    import numpy
except:
    print("no surfarray for you!  install numpy")

import time

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')


def main():
    pygame.init()
    pygame.mixer.quit()  # remove ALSA underflow messages for Debian squeeze
    screen = pygame.display.set_mode((640, 480))

    im1 = pygame.Surface(screen.get_size())
    # im1= im1.convert()
    im1.fill((100, 0, 0))

    im2 = pygame.Surface(screen.get_size())
    im2.fill((0, 50, 0))
    # we make a srcalpha copy of it.
    # im3= im2.convert(SRCALPHA)
    im3 = im2
    im3.set_alpha(127)

    screen.blit(im1, (0, 0))
    pygame.display.flip()
    clock = pygame.time.Clock()
    print("one pixel is:%s:" % [im1.get_at((0, 0))])

    going = True
    while going:
        clock.tick(60)



        screen.blit(im1, (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()