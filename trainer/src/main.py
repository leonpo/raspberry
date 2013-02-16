import random, sys, time, pygame
from pygame.locals import *

FPS = 5
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
TIMEOUT = 10 # seconds before game over if no right movement is performed.

#                R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
RED          = (155,   0,   0)
GREEN        = (  0, 155,   0)
BLUE         = (  0,   0, 155)
YELLOW       = (155, 155,   0)
bgColor = BLACK

# Available player moves
LEFT = "LEFT"
RIGHT = "RIGHT"
UP = "UP"
DOWN = "DOWN"

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) #pygame.FULLSCREEN
    pygame.display.set_caption('Personal Trainer')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 24)
    infoSurf = BASICFONT.render('Please Follow the movements on the screen', 1, WHITE)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10, WINDOWHEIGHT - 25)

    # Initialize some variables for a new game
    pattern = []  # stores the moves to follow
    currentStep = 0 # the movement that player should follow
    lastMoveTime = 0 # timestamp of the last movement
    score = 0
    # when False, the move is playing. when True, waiting for the player to do the move
    waitingForInput = False

    while True: # main game loop
        detectedMove = None         # the player's move: up, down, left, right
        DISPLAYSURF.fill(BLACK)
        drawPerson()

        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 100, 10)
        DISPLAYSURF.blit(scoreSurf, scoreRect)

        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        checkForMovement()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYDOWN:
                if event.key == K_a:
                    detectedMove = LEFT
                elif event.key == K_d:
                    detectedMove = RIGHT
                elif event.key == K_w:
                    detectedMove = UP
                elif event.key == K_s:
                    detectedMove = DOWN     
                    
        if not waitingForInput:
            # add new move to the pattern
            pygame.display.update()
            pygame.time.wait(1000)
            pattern = [] # currently always only one move to remember
            pattern.append(random.choice((LEFT,RIGHT,UP,DOWN)))
            for move in pattern:
                showMove(move)
            waitingForInput = True
        else:
            # wait for the player to do the movement
            if detectedMove and detectedMove == pattern[currentStep]:
                # correct movement
                currentStep += 1
                lastMoveTime = time.time()

                if currentStep == len(pattern):
                    # performed last move in the pattern
                    successAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0 # reset back to first step

            elif (detectedMove and detectedMove != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastMoveTime):
                # performed wrong move, or has timed out
                gameOverAnimation()
                # reset the variables for a new game:
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)
                
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back
        
def checkForMovement():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back        

def showMove(move):
    if move == UP:
        pygame.draw.rect(DISPLAYSURF, GREEN, (340, 20, 20, 70))
    if move == DOWN:
        pygame.draw.rect(DISPLAYSURF, GREEN, (340, 100, 20, 70))
    if move == LEFT:
        pygame.draw.rect(DISPLAYSURF, GREEN, (230, 100, 70, 20))
    if move == RIGHT:
        pygame.draw.rect(DISPLAYSURF, GREEN, (340, 100, 70, 20))
    pygame.display.update()
    pygame.time.wait(3000)    

def drawPerson():
    pygame.draw.circle(DISPLAYSURF, YELLOW, (300,60), 20)       # head
    pygame.draw.rect(DISPLAYSURF, GREEN, (270, 100, 60, 100))   # body
    pygame.draw.rect(DISPLAYSURF, BLUE, (270, 210, 20, 60))     # left leg
    pygame.draw.rect(DISPLAYSURF, BLUE, (310, 210, 20, 60))     # right

def successAnimation():
    pygame.draw.rect(DISPLAYSURF, GREEN, (10, 10, 500,400)) # success
    pygame.display.update()
    pygame.time.wait(2000)

def gameOverAnimation(color=WHITE, animationSpeed=50):
    pygame.draw.rect(DISPLAYSURF, RED, (10, 10, 500,400)) # success
    pygame.display.update()
    pygame.time.wait(3000)              

if __name__ == '__main__':
    main()
