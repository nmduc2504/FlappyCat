import pygame, sys, random
from pygame.locals import *

WINDOWWIDTH = 1080
WINDOWHEIGHT = 720

CAT1WIDTH = 155
CAT1HEIGHT = 171
G = 0.5
SPEEDFLY = -8
CAT1IMG = pygame.image.load('Desktop/Flappy Cat/img/cat1.png')

CAT2WIDTH = 155
CAT2HEIGHT = 171
CAT2IMG = pygame.image.load('Desktop/Flappy Cat/img/cat2.png')

BACKGROUND = pygame.image.load('Desktop/Flappy Cat/img/background.jpg')

COLUMNWIDTH = 60
COLUMNHEIGHT = 500
BLANK = 350
DISTANCE = 400
COLUMNSPEED = 2
COLUMNIMG = pygame.image.load('Desktop/Flappy Cat/img/column.png')

PLAYWIDTH = 100
PLAYHEIGHT = 60
PLAYIMG = pygame.image.load('Desktop/Flappy Cat/img/play.png')

pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Flappy Cat')

icon = pygame.image.load('Desktop/Flappy Cat/img/cat1.png')
pygame.display.set_icon(icon)

main_sound = pygame.mixer.music.load("Desktop/Flappy Cat/music/Sneaky-Snitch.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

flap_sound = pygame.mixer.Sound('Desktop/Flappy Cat/music/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('Desktop/Flappy Cat/music/sfx_hit.wav')
score_sound = pygame.mixer.Sound('Desktop/Flappy Cat/music/sfx_point.wav')
die_sound = pygame.mixer.Sound('Desktop/Flappy Cat/music/sfx_die.wav')

x = 50
y = 50
width = 40
height = 60
vel = 5

run = True

class Cat():
    def __init__(self):
        self.width = CAT1WIDTH
        self.height = CAT1HEIGHT
        self.x = (WINDOWWIDTH - self.width)/2
        self.y = (WINDOWHEIGHT- self.height)/2
        self.speed = 0
        self.suface = CAT1IMG

    def draw(self):
        DISPLAYSURF.blit(self.suface, (int(self.x), int(self.y)))

    def update(self, mouseClick):
        self.y += self.speed + 0.5*G
        self.speed += G
        if mouseClick == True:
            self.speed = SPEEDFLY
            flap_sound.play()

class Columns():
    def __init__(self):
        self.width = COLUMNWIDTH
        self.height = COLUMNHEIGHT
        self.blank = BLANK
        self.distance = DISTANCE
        self.speed = COLUMNSPEED
        self.surface = COLUMNIMG
        self.ls = []
        for i in range(3):
            x = WINDOWWIDTH + i*self.distance
            y = random.randrange(60, WINDOWHEIGHT - self.blank - 60, 20)
            self.ls.append([x, y])
        
    def draw(self):
        for i in range(3):
            DISPLAYSURF.blit(self.surface, (self.ls[i][0], self.ls[i][1] - self.height))
            DISPLAYSURF.blit(self.surface, (self.ls[i][0], self.ls[i][1] + self.blank))

    def update(self):
        for i in range(3):
            self.ls[i][0] -= self.speed
        if self.ls[0][0] < -self.width:
            self.ls.pop(0)
            x = self.ls[1][0] + self.distance
            y = random.randrange(60, WINDOWHEIGHT - self.blank - 60, 10)
            self.ls.append([x, y])

def rectCollision(rect1, rect2):
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False

def isGameOver(score, cat, columns):
        for i in range(3):
            rectCat = [cat.x, cat.y, cat.width, cat.height]
            rectColumn1 = [columns.ls[i][0], columns.ls[i][1] - columns.height, columns.width, columns.height]
            rectColumn2 = [columns.ls[i][0], columns.ls[i][1] + columns.blank, columns.width, columns.height]
            if rectCollision(rectCat, rectColumn1) == True or rectCollision(rectCat, rectColumn2) == True:
                hit_sound.play()
                return True
        if cat.y + cat.height < 0 or cat.y + cat.height > WINDOWHEIGHT:
            die_sound.play()
            return True
        return False

class Score():
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.addScore = True
    
    def draw(self):
        font = pygame.font.SysFont('arialblack', 40)
        scoreSuface = font.render(str(self.score), True, (0, 0, 0))
        textSize = scoreSuface.get_size()
        DISPLAYSURF.blit(scoreSuface, (int((WINDOWWIDTH - textSize[0])/2), 100))
    
    def update(self, cat, columns):
        collision = False
        for i in range(3):
            rectColumn = [columns.ls[i][0] + columns.width, columns.ls[i][1], 1, columns.blank]
            rectCat = [cat.x, cat.y, cat.width, cat.height]
            if rectCollision(rectCat, rectColumn) == True:
                collision = True
                break
        if collision == True:
            if self.addScore == True:
                self.score += 1
                self.high_score += 1
                score_sound.play()
            self.addScore = False
        else:
            self.addScore = True
    def update_score(score,high_score):
        if score > high_score:
            high_score = score
        return high_score

class Play():
    def __init__(self):
        self.width = PLAYWIDTH
        self.height = PLAYHEIGHT
        self.surface= PLAYIMG
        self.x = ((WINDOWWIDTH - self.width)/2-125)
        self.y = ((WINDOWHEIGHT- self.height)/2+50)
    def draw(self):
        DISPLAYSURF.blit(self.surface, (int(self.x), int(self.y)))

class Cat2():
    def __init__(self):
        self.width = CAT2WIDTH
        self.height = CAT2HEIGHT
        self.surface= CAT2IMG
        self.x = (WINDOWWIDTH - self.width)/2
        self.y = (WINDOWHEIGHT- self.height)/2
    def draw(self):
        DISPLAYSURF.blit(self.surface, (int(self.x), int(self.y)))

def gameStart(cat,play):
    cat.__init__()
    play.__init__()
    font = pygame.font.SysFont('consolas', 60)
    headingSuface = font.render('FLAPPY CAT', True, (255, 0, 0))
    headingSize = headingSuface.get_size()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                return

        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        cat.draw()
        play.draw()
        DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))

        pygame.display.update()
        fpsClock.tick(FPS)

def gamePlay(cat, columns, score):
    cat.__init__()
    cat.speed = SPEEDFLY
    columns.__init__()
    score.__init__()
    while True:
        mouseClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouseClick = True
        
        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        columns.draw()
        columns.update()
        cat.draw()
        cat.update(mouseClick)
        score.draw()
        score.update(cat, columns)

        if isGameOver(score, cat, columns) == True:
            return
    
        pygame.display.update()
        fpsClock.tick(FPS)

def gameOver(cat2, score):
    font = pygame.font.SysFont('John Hubbard', 60)
    headingSuface = font.render('GAME OVER', True, (255, 0, 0))
    headingSize = headingSuface.get_size()
    
    font = pygame.font.SysFont('John Hubbard', 40)
    comment1Suface = font.render('>> Click "Space" to play again <<', True, (255,255,255))
    comment1Size = comment1Suface.get_size()
    
    font = pygame.font.SysFont('John Hubbard', 40)
    comment2Suface = font.render('>> Click "ESC" to exit game <<', True, (255,255,255))
    comment2Size = comment2Suface.get_size()

    font = pygame.font.SysFont('consolas', 30)
    scoreSuface = font.render('Score:' + str(score.score), True, (0, 0, 0))
    scoreSize = scoreSuface.get_size()

    font = pygame.font.SysFont('consolas', 30)
    high_scoreSuface = font.render('High Score:' + str(score.high_score), True, (0, 0, 0))
    high_scoreSize = high_scoreSuface.get_size()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    return
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    sys.exit()
        
        DISPLAYSURF.blit(BACKGROUND, (0, 0))
        cat2.draw()
        DISPLAYSURF.blit(headingSuface, (int((WINDOWWIDTH - headingSize[0])/2), 100))
        DISPLAYSURF.blit(comment1Suface, (int((WINDOWWIDTH - comment1Size[0])/2), 600))
        DISPLAYSURF.blit(comment2Suface, (int((WINDOWWIDTH - comment2Size[0])/2), 650))
        DISPLAYSURF.blit(scoreSuface, (int((WINDOWWIDTH - scoreSize[0])/2), 160))
        DISPLAYSURF.blit(high_scoreSuface, (int((WINDOWWIDTH - high_scoreSize[0])/2), 190))
        pygame.display.update()
        fpsClock.tick(FPS)

def main():
    cat = Cat()
    columns = Columns()
    score = Score()
    play = Play()
    cat2 = Cat2()
    cat = Cat()
    while True:
        gameStart(cat,play)
        gamePlay(cat, columns, score)
        gameOver(cat2, score)

if __name__ == '__main__':
    main()