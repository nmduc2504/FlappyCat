import pygame, sys, random
from pygame.locals import *

WINDOWWIDTH = 1280
WINDOWHEIGHT = 720

CATWIDTH = 155
CATHEIGHT = 171
G = 0.5
SPEEDFLY = -8
CATIMG = pygame.image.load('Desktop/Flappy Cat/img/cat1.png')

BACKGROUND = pygame.image.load('Desktop/Flappy Cat/img/background1.jpg')

pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Flappy Cat')

class Cat():
    def __init__(self):
        self.width = CATWIDTH
        self.height = CATHEIGHT
        self.x = (WINDOWWIDTH - self.width)/2
        self.y = (WINDOWHEIGHT- self.height)/2
        self.speed = 0
        self.suface = CATIMG

    def draw(self):
        DISPLAYSURF.blit(self.suface, (int(self.x), int(self.y)))

    def update(self, mouseClick):
        self.y += self.speed + 0.5*G
        self.speed += G
        if mouseClick == True:
            self.speed = SPEEDFLY


def main():
    cat = Cat()
    while True:
        mouseClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouseClick = True
        
        DISPLAYSURF.blit(BACKGROUND, (0, 0))

        cat.draw()
        cat.update(mouseClick)

        pygame.display.update()
        fpsClock.tick(FPS)
if __name__ == '__main__':
    main()