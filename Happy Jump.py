from random import randint
import pygame
pygame.init()
WIDTH = 400
HEIGHT= 600
gameWindow = pygame.display.set_mode((WIDTH,HEIGHT))

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
SKYBLUE=(132,200,251)
PURPLE = (138,43,226)
YELLOW = (255,255,0)
outline = 0

def redrawGameWindow():
    gameWindow.fill(BLACK)
    if bottomPlat:
        pygame.draw.rect(gameWindow,SKYBLUE,(0,bottomPlatY,400,50),outline)
    for i in range(len(platforms)):
        pygame.draw.rect(gameWindow,SKYBLUE,(platforms[i][0],platforms[i][1],platformLengths[i],platformWidth),outline)
    pygame.draw.rect(gameWindow,GREEN,(characterCors[0],characterCors[1],characterDimensions,characterDimensions),outline)
    pygame.display.update()

gravity = 2
characterDimensions = 20
characterCors = [WIDTH/2 - characterDimensions/2, 550 - characterDimensions * 2]
characterMovement = [10,0]
characterLanded = True

bottomPlat = True
bottomPlatY = 550
platforms = [[30,450],[200,240],[120,400],[100,300]]
platformLengths = []
platformWidth = 20
for i in range(4):
    platformLengths.append(randint(40,60))

clock = pygame.time.Clock()
FPS = 30
inPlay = True
while inPlay:
    redrawGameWindow()
    clock.tick(FPS)
    pygame.time.delay(25)

    # character boundaries
    if characterCors[0] > WIDTH:
        characterCors[0] = 0
    elif characterCors[0] + characterDimensions < 0:
        characterCors[0] = WIDTH - characterDimensions

    # character movement
    pygame.event.get()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        if bottomPlat and characterCors[1] + characterDimensions == bottomPlatY:
            characterMovement[1] = -25
        for i in range(len(platforms)):
            if characterCors[1] + characterDimensions == platforms[i][1] and characterCors[0] <= platforms[i][0] + platformLengths[i] and characterCors[0] + characterDimensions >= platforms[i][0] and characterMovement[1] <= 0:
                characterMovement[1] = -25
    if keys[pygame.K_LEFT]:
        characterCors[0] -= characterMovement[0]
    elif keys[pygame.K_RIGHT]:
        characterCors[0] += characterMovement[0]

    characterMovement[1] = characterMovement[1] + gravity
    characterCors[1] = characterCors[1] + characterMovement[1]

    # character landing mechanisms
    if characterCors[1] + characterDimensions >= bottomPlatY and bottomPlat:
        characterCors[1] = bottomPlatY - characterDimensions
        characterMovement[1] = 0
    else:
        for i in range(len(platforms)):
            if characterCors[1] + characterDimensions >= platforms[i][1] and characterCors[0] <= platforms[i][0] + platformLengths[i] and characterCors[0] + characterDimensions >= platforms[i][0] and characterMovement[1] > 0 and characterCors[1] <= platforms[i][1]:
                characterCors[1] = platforms[i][1] - characterDimensions
                characterMovement[1] = 0

    # moves all objects at the same rate to show the character climbing higher and higher
    if characterCors[1] <= HEIGHT/4:
        characterCors[1] += abs(characterMovement[1])
        if bottomPlat:
            bottomPlatY += abs(characterMovement[1])
        for i in range(len(platforms)):
            platforms[i][1] += abs(characterMovement[1])

            # destroy platforms once they reach the bottom of the screen
            if platforms[i][1] >= HEIGHT:
                platforms.pop(i)
                platformLengths.pop(i)
            if bottomPlatY >= HEIGHT:
                bottomPlat = False

            # spawn more platforms
            while len(platforms) <= 5:
                platformLengths.append(randint(40,60))
                xCor = randint(0,WIDTH - 60)
                yCor = randint(90,115)
                platforms.append([xCor,yCor])

    # detects if it's game over
    if characterCors[1] + characterDimensions >= HEIGHT:
        while characterCors[1] + characterDimensions >= 0:
            redrawGameWindow()
            clock.tick(FPS)
            pygame.time.delay(25)
            characterCors[1] -= abs(characterMovement[1]) - 10
            print (characterCors[1])
            for i in range(len(platforms)):
                platforms[i][1] -= abs(characterMovement[1])
        inPlay = False
pygame.quit()