""" PracticeGame4.py
    Ibrahim Sardar
--------------------------------------
info: Virus Shooter
      Shooter Type Game
      CSCI 23000
--------------------------------------
"""

#load modules
import pygame, sys, random, time, shelve, tkinter
from pygame.locals import *

#initialize pygame
pygame.init()


# --- start resources --- #

#COLORS
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
GREY   = (192, 192, 192)
GREEN  = (  0, 255,   0)
PINK   = (255, 183, 234)
RED    = (255,   0,   0)
ORANGE = (255, 128,   0)
BLUE   = (  0,   0, 255)
BROWN  = (102,  51,   0)
PURPLE = (102,   0, 102)
YELLOW = (255, 255,   0)

#FONTS
font1 = pygame.font.SysFont("aharoni", 72)
font2 = pygame.font.SysFont("comicsansms", 28)
font3 = pygame.font.SysFont("miriamfixed", 12)

#SOUND/MUSIC
sndwin   = pygame.mixer.Sound("win.wav")
sndlose  = pygame.mixer.Sound("lose.wav")
sndshoot = pygame.mixer.Sound("shoot.wav")
sndbomb  = pygame.mixer.Sound("bomb.wav")
sndeat   = pygame.mixer.Sound("eat.wav")
sndcoin  = pygame.mixer.Sound("coin.wav")
sndgrunt = pygame.mixer.Sound("grunt.wav")
sndhit   = pygame.mixer.Sound("hit.wav")

#WINDOW
WINDOWWIDTH   = 720
WINDOWHEIGHT  = 380
WINDOWCENTER  = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Virus Shooter")

#GROUPS
bulletList  = pygame.sprite.Group()
bombList    = pygame.sprite.Group()
redGroup    = pygame.sprite.Group()
whiteGroup  = pygame.sprite.Group()
brownGroup  = pygame.sprite.Group()
purpleGroup = pygame.sprite.Group()
infoGroup   = pygame.sprite.Group()

#LISTS
enemyNames  = ["Red Virus",
               "White Defender Cell",
               "Cancer Cell",
               "Purple Bubonic (Boss)"]

#'timer' gets time Clock object
timer = pygame.time.Clock()

# --- end resources --- #
#CLASSES#-------------------------------------------------------------------------------#CLASSS#------------------------------------#
#SUPERSPRITE ***inherit this class
class superSprite(pygame.sprite.Sprite):
    #initializer
    def __init__(self, color, speed):
        #attributes
        pygame.sprite.Sprite.__init__(self)
        self.color  = color
        self.speed  = speed
        self.loaded = False
        self.setImage(12, 12)

    # --- update method --- #
    def update(self):
        windowSurface.blit(self.image, (self.rect.x, self.rect.y))
        self.image.fill(self.color)

    # --- get/set methods --- #
    def setPosition(self, xPos, yPos):
        self.rect.x = xPos
        self.rect.y = yPos

    def setImage(self, width, height):
        self.image = pygame.Surface((width, height))
        self.rect  = self.image.get_rect()

    # --- other methods --- #
    def load(self, player):
        #places sprite beneath the player
        self.rect.center = player.rect.center
        self.loaded = True

    def hide(self):
        #places sprite out of the screen
        self.rect.center = (-20, -20)
        self.loaded = False

    def changeSize(self, inc):
        xP = self.rect.centerx
        yP = self.rect.centery
        w  = self.rect.width  + inc
        h  = self.rect.height + inc
        self.setImage(w, h)
        self.rect.centerx = xP
        self.rect.centery = yP

#PLAYER
class player(superSprite):
    #initializer
    def __init__(self, color, speed):
        #attributes
        superSprite.__init__(self, color, speed)
        self.setPosition((WINDOWWIDTH/2) + self.rect.width/2, WINDOWHEIGHT - self.rect.height)
        self.color  = color
        self.speed  = speed
        self.health = 100

    # --- update method --- #
    def update(self):
        windowSurface.blit(self.image, (self.rect.x, self.rect.y))
        self.image.fill(self.color)
        self.collideScreen()

    # --- other methods --- #
    def move(self, direction):
        #Moves the sprite at a certain speed
        if direction == "up":
            self.rect.y -= self.speed
        if direction == "down":
            self.rect.y += self.speed
        if direction == "right":
            self.rect.x += self.speed
        if direction == "left":
            self.rect.x -= self.speed

    def stop(self, direction):
        #makes the sprite go the opposite direction
        if direction == "up":
            self.rect.y += self.speed
        if direction == "down":
            self.rect.y -= self.speed
        if direction == "right":
            self.rect.x -= self.speed
        if direction == "left":
            self.rect.x += self.speed

    def collideScreen(self):
        #stops sprite if it touches the screen edges
        if self.rect.x < 0:
            self.stop("left")
        if self.rect.x + self.rect.width > WINDOWWIDTH:
            self.stop("right")
        if self.rect.y + self.rect.height > WINDOWHEIGHT:
            self.stop("down")
        if self.rect.y < 0:
            self.stop("up")
    # --- end other methods --- #

#ENEMY
class enemy(superSprite):
    #initialize
    def __init__(self, color, speed):
        #attributes
        superSprite.__init__(self, color, speed)
        self.color  = color
        self.speed  = speed
        self.health = 100
        self.rndDir = random.randint(-4, 4)

    # --- update method --- #
    def update(self):
        self.move(self.rndDir)
        windowSurface.blit(self.image, (self.rect.x, self.rect.y))
        self.image.fill(self.color)
        self.collideBoundaries()

    # --- other methods --- #
    def move(self, direction):
        #moves the block in a direction
        #east
        if direction == 0:
            self.rect.x += self.speed
        if direction == 1:
            self.rect.x += self.speed
        #northeast
        if direction == 2:
            self.rect.x += self.speed
            self.rect.y -= self.speed
        #north
        if direction == 3:
            self.rect.y -= self.speed
        #northwest
        if direction == 4:
            self.rect.x -= self.speed
            self.rect.x -= self.speed
        #west
        if direction == -1:
            self.rect.x -= self.speed
        #southwest
        if direction == -2:
            self.rect.x -= self.speed
            self.rect.y += self.speed
        #south
        if direction == -3:
            self.rect.y += self.speed
        #southeast
        if direction == -4:
            self.rect.x += self.speed
            self.rect.y += self.speed

    def collideBoundaries(self):
        #change enemy direction if touching edge of window
        if self.rect.right >= WINDOWWIDTH:
            dirList = [3, 4, -1, -2, -3]
            self.rndDir = random.choice(dirList)
        if self.rect.top <= 0:
            dirList = [1, -1, -2, -3, -4]
            self.rndDir = random.choice(dirList)
        if self.rect.left <= 0:
            dirList = [1, 2, 3, -3, -4]
            self.rndDir = random.choice(dirList)
        if self.rect.bottom >= WINDOWHEIGHT:
            dirList = [1, 2, 3, 4, -1]
            self.rndDir = random.choice(dirList)
    # --- end other methods --- #

#BULLET
class bullet(superSprite):
    #initialize
    def __init__(self, color, speed):
        #attributes
        superSprite.__init__(self, color, speed)
        self.color = color
        self.speed = speed
        self.dir   = -1
        self.setImage(4, 4)

        self.loaded = False
        self.hide()

    # --- update method --- #
    def update(self):
        if self.loaded == True:
            self.moveBullet()
        windowSurface.blit(self.image, self.rect.topleft)
        self.image.fill(self.color)

    # --- other methods --- #
    def moveBullet(self):
        #moves the bullet in one of four directions
        if self.dir == 0:
            self.rect.centerx += self.speed
        if self.dir == 1:
            self.rect.centery -= self.speed
        if self.dir == 2:
            self.rect.centerx -= self.speed
        if self.dir == 3:
            self.rect.centery += self.speed

#BOMB
class bomb(superSprite):
    #initialize
    def __init__(self, color, speed):
        #attributes
        superSprite.__init__(self, color, speed)
        self.color  = color
        self.speed  = speed
        self.count  = -49
        
        self.setImage(10, 10)

    def update(self):
        self.actionFrame()
        windowSurface.blit(self.image, self.rect.topleft)
        self.image.fill(self.color)

    def actionFrame(self):
        #runs the animation for bomb explosion

        #increment
        self.count += 1

        #frame 1
        if self.count == 1:
            self.color = BLACK

        #frame 2
        if self.count == 2:
            self.changeSize(5)
            self.color = RED
            sndbomb.play()

        #frame 3
        if self.count == 4:
            self.changeSize(15)
            self.color = ORANGE

        #frame 4
        if self.count == 6:
            self.changeSize(50)
            self.color = YELLOW

        #frame 5
        if self.count == 8:
            self.changeSize(-10)
            self.color = GREY

        #frame 6
        if self.count == 10:
            self.changeSize(-30)
            self.color = WHITE

        #frame 7
        if self.count == 11:
            self.kill()
    
#LABEL
class label(pygame.sprite.Sprite):
    #initialize
    def __init__(self, txt, color, pos, font, centered):
        #attributes
        pygame.sprite.Sprite.__init__(self)
        self.txt   = txt
        self.color = color
        self.pos   = pos
        self.font  = font

        self.image = self.font.render(self.txt, True, self.color)
        self.rect  = self.image.get_rect()
        
        #centered text
        if centered == True:
            self.rect.center = self.pos

        #left - aligned text
        if centered == False:
            self.rect.topleft = self.pos
        
        windowSurface.blit(self.image, self.rect)
#END CLASSES#---------------------------------------------------------------------------#END CLASSES#-------------------------------#
#FUNCTIONS#-----------------------------------------------------------------------------#FUNCTIONS#---------------------------------#

#initialize enemys/hostiles
def readyEnemy(objGroup):
    #initializes a group's objects' positions
    for obj in objGroup:
        #sets enemy randomly on the screen
        rndPosX = random.randint(0, WINDOWWIDTH  - (obj.rect.width     ))
        rndPosY = random.randint(0, WINDOWHEIGHT - (obj.rect.height * 5))
        obj.setPosition(rndPosX, rndPosY)

#PAUSE
#set up pause/information screen
def pauseGame():
    paused = True

    #labels
    label(" GAME PAUSED ",
         BLACK,
         (WINDOWWIDTH/2, 48),
         font1,
         True)
    label("backspace to continue.",
        BLACK,
        (WINDOWWIDTH/2, 100),
        font2,
        True)
    label("esc to exit.",
        BLACK,
        (WINDOWWIDTH/2, 130),
        font2,
        True)
    label("C for controls.",
        BLACK,
        (WINDOWWIDTH/2, 160),
        font2,
        True)
    label("get points by terminating: red, brown, purple | lose points by terminating: white",
        BLACK,
        (WINDOWWIDTH/2, WINDOWHEIGHT - 24),
        font3,
        True)
    label("defeat all ten levels to win | game over if terminate all: white or touch: red, brown, purple",
        BLACK,
        (WINDOWWIDTH/2, WINDOWHEIGHT - 12),
        font3,
        True)

    #update
    pygame.display.update()

    #MINI "GAME" LOOP
    while(paused):

        #event handling
        for event in pygame.event.get():

            #QUIT
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            pressing = pygame.key.get_pressed()

            #QUIT
            if pressing[K_ESCAPE]:
                pygame.quit()
                sys.exit()

            #UN-PAUSE
            if pressing[K_BACKSPACE]:
                paused = False

            #GAME INFORMATION
            if pressing[K_i]:
                paused = False
                infoGame()

            #GAME CONTROLS
            if pressing[K_c]:
                paused = False
                controlsGame()

"""#HIGH SCORE
def highScore():
    #puts top 3 high scores in a .txt database
    
    #hsFile = open('VS High Scores', 'w')
    pass"""

#ENDGAME
#set up end score screen
def endGame(win, score, lvl):
    paused = True

    """#retrieve high scores from "VS_high_scores.txt"-------------------------here-------------------------here------------------------------
    highScores = ""
    #set the highscores according to current score
    
    
    #show high scores in new window
    top = Toplevel()
    top.title("High Scores")
    msg = Message(top, text=highScores)
    msg.pack()
    button = Button(top, text="Ok", command=top.destroy)
    button.pack()"""

    #labels
    #use 'win' to tell if won/lose screen should pop up
    if win == False:
        #background color
        windowSurface.fill(RED)
        #lose label
        label(  " *   YOU DIED.  * ",
                BLACK,
                (WINDOWWIDTH/2, 48),
                font1,
                True)
        #lose sound
        sndlose.play()
        
    if win == True:
        #background color
        windowSurface.fill(WHITE)
        #win label
        label(  " !   YOU WON   ! ",
                BLUE,
                (WINDOWWIDTH/2, 48),
                font1,
                True)
        sndwin.play()
        
    label(  "esc to quit.",
            BLACK,
            (WINDOWWIDTH/2, 100),
            font2,
            True)
    #use score to show score
    label(  "Score: " + str(score),
            GREEN,
            (WINDOWWIDTH/2, 175),
            font1,
            True)
    #show level reached
    label(  "Level reached: " + str(lvl),
            GREEN,
            (WINDOWWIDTH/2, 215),
            font2,
            True)
    lblrestart = label( "Restart? (click)",
                        GREY,
                        (WINDOWWIDTH/2, 300),
                        font2,
                        True)

    #update
    pygame.display.update()

    #MINI "GAME" LOOP
    while(paused):

        #event handling
        for event in pygame.event.get():

            #QUIT
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            pressing = pygame.key.get_pressed()
            clicking = pygame.mouse.get_pressed()

            #QUIT
            if pressing[K_ESCAPE]:
                pygame.quit()
                sys.exit()

            #RESTART
            if lblrestart.rect.collidepoint(pygame.mouse.get_pos()):
                label( "Restart? (click)",
                        GREY,
                        (WINDOWWIDTH/2, 300),
                        font2,
                        True)
                if clicking[0] == True:
                    restartGame()
                    paused = False
            else:
                label( "Restart? (click)",
                        BLACK,
                        (WINDOWWIDTH/2, 300),
                        font2,
                        True)

            #update
            pygame.display.update()

#STARTSCREEN
#set up start screen
def startScreen():
    paused = True

    #background color
    windowSurface.fill(PINK)

    #labels
    label("||   VIRUS SHOOTER   ||",
         BLUE,
         (WINDOWWIDTH/2, 48),
         font1,
         True)
    label("enter to start.",
        RED,
        (WINDOWWIDTH/2, 100),
        font2,
        True)
    label("C for controls",
        RED,
        (WINDOWWIDTH/2, 124),
        font2,
        True)
    label("You are sick",
        BLUE,
        (WINDOWWIDTH/2, 180),
        font2,
        True)
    label("You injected something in yourself",
        BLUE,
        (WINDOWWIDTH/2, 210),
        font2,
        True)
    label("Make yourself feel better or you will die",
        BLUE,
        (WINDOWWIDTH/2, 240),
        font2,
        True)
    label("Good luck!",
        BLUE,
        (WINDOWWIDTH/2, 270),
        font2,
        True)
    label("W,S,A,D to shoot.",
        GREEN,
        (WINDOWWIDTH/2, 300),
        font2,
        True)
    label("Arrow keys to move.",
        GREEN,
        (WINDOWWIDTH/2, 330),
        font2,
        True)
    label("get points by terminating: red, brown, purple | lose points by terminating: white",
        BLACK,
        (WINDOWWIDTH/2, WINDOWHEIGHT - 24),
        font3,
        True)
    label("defeat all ten levels to win | game over if terminate all: white | game over if touch: white ",
        BLACK,
        (WINDOWWIDTH/2, WINDOWHEIGHT - 12),
        font3,
        True)
    
    #update
    pygame.display.update()

    #MINI "GAME" LOOP
    while(paused):

        #event handling
        for event in pygame.event.get():

            #QUIT
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            pressing = pygame.key.get_pressed()

            #START GAME
            if pressing[K_RETURN]:
                paused = False
            
            #QUIT
            if pressing[K_ESCAPE]:
                pygame.quit()
                sys.exit()

            #GAME INFORMATION
            if pressing[K_i]:
                paused = False
                infoGame()

            #GAME CONTROLS
            if pressing[K_c]:
                paused = False
                controlsGame()

def infoGame():
    paused = True

    windowSurface.fill(GREY)

    label(  "~   INFORMATION   ~",
            BLACK,
            (WINDOWWIDTH/2, 48),
            font1,
            True)

    #game story
    label(  "Story:",
            BLACK,
            (6, 60),#0
            font2,
            False)
    label(  "Unfortunately, your sick. So instead of going to the doctor, you injected something in yourself.",
            BLACK,
            (12, 106),#46
            font3,
            False)
    label(  "Eventually you find out you weren't actually sick and the syringe had all kinds of deadly viruses.",
            BLACK,
            (12, 118),#12
            font3,
            False)
    label(  "Luckily, a mighty anti-virus, floating in your body, is in position to save you and your body.",
            BLACK,
            (12, 130),#12
            font3,
            False)
    label(  "Play as the anti-virus and take out the intruders!",
            BLACK,
            (12, 142),#12
            font3,
            False)

    #game information
    label(  "The Game:",
            BLACK,
            (6, 154),#12#0
            font2,
            False)

    label(  "There are 10 levels.",
            BLACK,
            (12, 200),#46
            font3,
            False)

    label(  "Complete a level by terminating all red, brown, and/or purple enemies",
            BLACK,
            (12, 212),#12
            font3,
            False)

    label(  "Lose a level by terminating(all) or touching white defender cells or losing all health",
            BLACK,
            (12, 224),#46
            font3,
            False)

    #enemy information
    label(  "Enemies:",
            BLACK,
            (6, 236),
            font2,
            False)

    #make enemy objects ***color and speed are irrelevant here
    red    = superSprite(RED , 0)
    white  = superSprite(WHITE   , 0)
    brown  = superSprite(BROWN , 0)
    purple = superSprite(PURPLE, 0)
    
    #add images to group
    infoGroup.add(red, white, brown, purple)
    
    #set a list of colors
    infoColors = [red.color,
                  white.color,
                  brown.color,
                  purple.color]
    
    #set increments
    dxPos = 20
    x     = 0
    #place images
    for sprite in infoGroup:
        dxPos += 140
        sprite.rect.x = dxPos
        sprite.rect.y = 282
        sprite.image.fill(infoColors[x])
        x += 1

    #image descriptions
    label(enemyNames[0] + "     " +\
          enemyNames[1] + "      " +\
          enemyNames[2] + "     " +\
          enemyNames[3],
          BLACK,
          (138, 312),
          font3,
          False)
    label("+1pt           -1pt          +5pts       +25pts",
          GREEN,
          (138, 324),
          font2,
          False)
    
    #update
    infoGroup.update()
    pygame.display.update()
    
    #clean out infoGroup
    infoGroup.empty()

    #MINI "GAME" LOOP
    while(paused):

        #event handling
        for event in pygame.event.get():

            #QUIT
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            pressing = pygame.key.get_pressed()

            #QUIT
            if pressing[K_ESCAPE]:
                pygame.quit()
                sys.exit()

            #UN-PAUSE
            if pressing[K_BACKSPACE]:
                paused = False

            #GAME CONTROLS
            if pressing[K_c]:
                paused = False
                controlsGame()

def controlsGame():
    paused = True

    windowSurface.fill(GREY)

    label(  "^   CONTROLS   ^",
            BLACK,
            (WINDOWWIDTH/2, 48),
            font1,
            True)

    #game controls
    label(  "Move:                                                       ARROW KEYS",
            BLACK,
            (12, 70),
            font2,
            False)
    label(  "Attack:                                                    W, S, A, D",
            BLACK,
            (12, 110),
            font2,
            False)
    label(  "Special:                                                    SPACEBAR",
            BLACK,
            (12, 150),
            font2,
            False)
    label(  "(Unlocked after 100 score reached)",
            BLACK,
            (12, 194),
            font3,
            False)
    label(  "More information:                                   \"I\" Key",
            BLACK,
            (12, 200),
            font2,
            False)
    label(  "Controls:                                                 \"C\" Key",
            BLACK,
            (12, 240),
            font2,
            False)
    label(  "Back to game:                                          BACKSPACE",
            BLACK,
            (12, 280),
            font2,
            False)
    label(  "Pause:                                                      \"P\" Key",
            BLACK,
            (12, 310),
            font2,
            False)
    label(  "Quit:                                                        ESCAPE",
            BLACK,
            (12, 340),
            font2,
            False)
    
    pygame.display.update()

    #MINI "GAME" LOOP
    while(paused):

        #event handling
        for event in pygame.event.get():

            #QUIT
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            pressing = pygame.key.get_pressed()

            #QUIT
            if pressing[K_ESCAPE]:
                pygame.quit()
                sys.exit()

            #UN-PAUSE
            if pressing[K_BACKSPACE]:
                paused = False

            #GAME INFOMATION
            if pressing[K_i]:
                infoGame()
                paused = False

#NEXT LEVEL
#show a flashing next level screen
def nextLevel():

    #background color
    windowSurface.fill(BLACK)
    
    #flashing four times
    for x in range(4):
        lblnxt = label( ">>> NXT LVL >>>",
                        PINK,
                        WINDOWCENTER,
                        font1,
                        True)

        #update everything on next level scene
        pygame.display.update()
        pygame.time.wait(200)
        windowSurface.fill(BLACK)
        pygame.display.update()
        pygame.time.wait(200)

#DUPLICATE ENEMY
def duplicateEnemy(enemyOrig, group, color, speed):

    #add new enemy to group
    #set it to the original enemy's position
    enemy1 = enemy(color, speed)
    group.add(enemy1)
    enemy1.setPosition(enemyOrig.rect.x,
                       enemyOrig.rect.y)

#BULLET COLLISION EFFECT ***messy
def collideBulletEffect(bullet, bltType, enemy, dmg, score, scoreDiff, enTyp, oldEnemyType, oldEnemyHp):

    #vars
    enemyType = oldEnemyType
    eHp       = oldEnemyHp

    #bullet to enemy effect
    if bltType == 'bullet':
        bullet.kill()
            
    enemy.health -= dmg

    #manage enemy and score
    if enemy.health <= 0:
        enemy.health = 0
        eHp = enemy.health
        enemy.kill()
        score += scoreDiff

        #play sound
        if enTyp == 'w':
            sndgrunt.play()
        else:
            sndcoin.play()

        #score cant be negative
        if score < 0:
            score = 0
    else:
        sndhit.play()
        eHp = enemy.health

    #basically, sets values to show last enemy hit
    if enTyp == 'r':
        enemyType = enemyNames[0]
    if enTyp == 'w':
        enemyType = enemyNames[1]
    if enTyp == 'b':
        enemyType = enemyNames[2]
    if enTyp == 'p':
        enemyType = enemyNames[3]

    #return updated score, enemyType, and last enemy's hp in a tuple
    return (score, enemyType, eHp)

#RESTART
def restartGame():
    main()

#UNLOCKING SOMETHING IF A CERTAIN SCORE IS SURPASSED ***not used in this version
def checkScore(score, rank):
    
    if score >= rank * 100:
            return rank
        
    for x in range(rank - 1):
        if score >= 100 * (x + 1):
            if score <= 100 * (x + 2):
                return x

#MAIN#----------------------------------------------------------------------------------#MAIN#--------------------------------------#
def main():

    #stop any ongoing souonds
    pygame.mixer.stop()

    #intro music
    pygame.mixer.music.load("VirusShooterIntro.ogg")
    pygame.mixer.music.play(-1)
    
    #start screen
    startScreen()

    #background music
    pygame.mixer.music.load("VirusShooter.ogg")
    pygame.mixer.music.play(-1)
    
    #get stuff (int, boolean, obj)
    score           = 0
    lvl             = 0
    bombLimit       = 20
    paused          = False
    keepGoing       = True
    bombUnlocked    = False
    p               = player(BLUE, 5)
    lbllastEnemyHit = label("Enemy Health: {}".format(0),
                            BLACK,
                            (6, 41),
                            font3,
                            False)

#---#MAIN GAME LOOP#--------------------------------------------------------------------#MAIN GAME LOOP#----------------------------#
    while(keepGoing):

        #reset some things
        p.health    = 100
        timeElapsed = 0
        enemyType   = "Enemy"
        lastEnHp    = 0
        whiteGroup.empty()
        bulletList.empty()
        redGroup.empty()
        brownGroup.empty()
        purpleGroup.empty()
        bombList.empty()
        p.setPosition((WINDOWWIDTH/2) + p.rect.width/2, WINDOWHEIGHT - p.rect.height)
        
        #next level screen
        if lvl > 1:
            nextLevel()
    
        #add red enemies
        for x in range(5 * lvl):
            re1 = enemy(RED, 2)
            redGroup.add(re1)

        #add white hostiles
        for x in range(5):
            wc1 = enemy(WHITE, 1)
            whiteGroup.add(wc1)

        #add brown enemies
        if lvl > 3:
            for x in range(lvl - 3):
                be1 = enemy(BROWN, 1)
                brownGroup.add(be1)

        #add purple enemies
        if lvl > 7:
            for x in range(lvl - 7):
                purp = enemy(PURPLE, 1)
                purpleGroup.add(purp)

        #ready 
        readyEnemy(redGroup)
        readyEnemy(whiteGroup)
        readyEnemy(brownGroup)
        readyEnemy(purpleGroup)
        
        #set the current level
        currentLevel = lvl
    
  # --- #MAIN LEVEL LOOP# --- #
        while(lvl == currentLevel):

            pressing = pygame.key.get_pressed()

            #QUIT
            if pressing[K_ESCAPE]:
                pygame.quit()
                sys.exit()

            #PLAYER MOVEMENT
            if pressing[K_UP]:
                p.move("up")
            if pressing[K_DOWN]:
                p.move("down")
            if pressing[K_RIGHT]:
                p.move("right")
            if pressing[K_LEFT]:
                p.move("left")
                
            #PAUSE
            if pressing[K_p]:
                pauseGame()

            #SHOW INFO
            if pressing[K_i]:
                infoGame()

            #SHOW CONTROLS
            if pressing[K_c]:
                controlsGame()
            
            #event handling
            for event in pygame.event.get(): 

                #QUIT
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    
              # --- #SHOOTING# --- #
                    #NORMAL bullet
                    pygame.time.set_timer(KEYDOWN, 100)
                    
                    #north
                    if pressing[K_w]:
                        b1     = bullet(ORANGE, 6)
                        b1.dir = 1
                        b1.load(p)
                        bulletList.add(b1)
                        sndshoot.play()
                        
                    #south
                    if pressing[K_s]:
                        b1     = bullet(ORANGE, 6)
                        b1.dir = 3
                        b1.load(p)
                        bulletList.add(b1)
                        sndshoot.play()
                        
                    #east
                    if pressing[K_d]:
                        b1     = bullet(ORANGE, 6)
                        b1.dir = 0
                        b1.load(p)
                        bulletList.add(b1)
                        sndshoot.play()
                        
                    #west
                    if pressing[K_a]:
                        b1     = bullet(ORANGE, 6)
                        b1.dir = 2
                        b1.load(p)
                        bulletList.add(b1)
                        sndshoot.play()

                    #BOMB
                    #if score is 100, get new weapon: bomb
                    #bomb should drop a bomb in player pos
                    #when space is pressed
                    if bombUnlocked == False:
                        if score >= 100:
                            for x in range(3):
                                lblunlock = label("Bomb Unlocked !",
                                                  BLACK,
                                                  (WINDOWCENTER),
                                                  font1,
                                                  True)
                                pygame.display.update()
                                time.sleep(.5)
                                lblunlock = label("Bomb Unlocked !",
                                                  ORANGE,
                                                  (WINDOWCENTER),
                                                  font1,
                                                  True)
                                pygame.display.update()
                                time.sleep(.5)
                            bombUnlocked = True
                            lblunlock.kill()

                    if bombUnlocked == True:
                        #limit to only 1 bomb at a time
                        if len(bombList) <= bombLimit:
                            
                            #drop bomb at player pos
                            if pressing[K_SPACE]:
                                bmb = bomb(BLACK, 0)
                                bmb.load(p)
                                bombList.add(bmb)
                
# ----------#COLLISION#-----------------------------------------------------------------#COLLISION#---------------------------------#

            #red enemies
            for red in redGroup:
                #player health to zero if collided
                if red.rect.colliderect(p.rect) == True:
                    p.health -= 5

                #red enemies reacting to each other by changing direction
                for redOther in redGroup:
                    if red.rect.colliderect(redOther.rect) == True:
                        red.rndDir      = -redOther.rndDir
                        redOther.rndDir = -red.rndDir

            #white hostiles
            for white in whiteGroup:
                #player health to zero if collided
                if white.rect.colliderect(p.rect) == True:
                    p.health = 0

            #brown enemies
            for brown in brownGroup:
                #player health to zero if collided
                if brown.rect.colliderect(p.rect) == True:
                    p.health -= 15
                
            #purple enemies
            for purp in purpleGroup:
                #player health -30 if collided
                if purp.rect.colliderect(p.rect) == True:
                    p.health -= 30

                #increase size or relocate if eats red
                for red in redGroup:
                    if purp.rect.colliderect(red.rect) == True:
                        sndeat.play()
                        if purp.rect.width < 50:
                            red.kill()
                            purp.changeSize(5)
                        else:
                            red.setPosition(random.randint(0,WINDOWWIDTH),random.randint(0,WINDOWHEIGHT))
                            b1     = bullet(PURPLE, 4)
                            b1.dir = 0
                            b1.load(purp)
                            bulletList.add(b1)
                            b2     = bullet(PURPLE, 4)
                            b2.dir = 1
                            b2.load(purp)
                            bulletList.add(b2)
                            b3     = bullet(PURPLE, 4)
                            b3.dir = 2
                            b3.load(purp)
                            bulletList.add(b3)
                            b4     = bullet(PURPLE, 4)
                            b4.dir = 3
                            b4.load(purp)
                            bulletList.add(b4)

                #inc health and speed (max:player speed) if eats brown
                for brown in brownGroup:
                    if purp.rect.colliderect(brown.rect) == True:
                        brown.kill()
                        sndeat.play()
                        purp.health += 100
                        if purp.speed < p.speed - 1:
                            purp.speed  += 1
            
            #orange bullets (normal) ***messy
            for bullets in bulletList:

                #if purple bullet hits player
                if bullets.rect.colliderect(p.rect) == True:
                    if bullets.color == PURPLE:
                        p.health -= 1

                #kill bullets if touch edge of window
                if bullets.rect.right >= WINDOWWIDTH + bullets.rect.width:
                    bullets.kill()
                if bullets.rect.top <= 0 - bullets.rect.height:
                    bullets.kill()
                if bullets.rect.left <= 0 - bullets.rect.width:
                    bullets.kill()
                if bullets.rect.bottom >= WINDOWHEIGHT + bullets.rect.height:
                    bullets.kill()

                #ONLY if bullets are orange
                if bullets.color == ORANGE:
                
                    #bullets hitting red enemies
                    for red in redGroup:
                        
                        #collision detection
                        if bullets.rect.colliderect(red.rect) == True:
                            info = collideBulletEffect(bullets, 'bullet', red, 100, score, 1, "r", enemyType, lastEnHp)
                        
                            #set information to variables in this loop
                            score     = info[0]
                            enemyType = info[1]
                            lastEnHp  = info[2]
                                
                    #bullets hitting white hostiles
                    for white in whiteGroup:
                        
                        #collision detection
                        if bullets.rect.colliderect(white.rect) == True:
                            info = collideBulletEffect(bullets, 'bullet', white, 100, score, -1, "w", enemyType, lastEnHp)
                        
                            #set information to variables in this loop
                            score     = info[0]
                            enemyType = info[1]
                            lastEnHp  = info[2]
                        
                    #bullets hitting brown enemies
                    for brown in brownGroup:
                        
                        #collision detection
                        if bullets.rect.colliderect(brown.rect) == True:
                            info = collideBulletEffect(bullets, 'bullet', brown, 15, score, 5, "b", enemyType, lastEnHp)
                            
                            #set information to variables in this loop
                            score     = info[0]
                            enemyType = info[1]
                            lastEnHp  = info[2]
                            
                    #bullets hitting purple enemies
                    for purp in purpleGroup:
                        
                        #collision detection
                        if bullets.rect.colliderect(purp.rect) == True:
                            info = collideBulletEffect(bullets, 'bullet', purp, 1, score, 25, "p", enemyType, lastEnHp)
                        
                            #set information to variables in this loop
                            score     = info[0]
                            enemyType = info[1]
                            lastEnHp  = info[2]

            #bomb collision ***messy
            for bmb in bombList:

                #doesn't collide if it hasn't started exploding
                if bmb.count >= 2:

                    #bullets hitting red enemies
                    for red in redGroup:
                        
                        #collision detection
                        if bmb.rect.colliderect(red.rect) == True:
                            info = collideBulletEffect(bmb, 'bomb', red, 100, score, 1, "r", enemyType, lastEnHp)
                        
                            #set information to variables in this loop
                            score     = info[0]
                            enemyType = info[1]
                            lastEnHp  = info[2]
                                
                    #bullets hitting white hostiles
                    for white in whiteGroup:
                        
                        #collision detection
                        if bmb.rect.colliderect(white.rect) == True:
                            info = collideBulletEffect(bmb, 'bomb', white, 100, score, -1, "w", enemyType, lastEnHp)
                        
                            #set information to variables in this loop
                            score     = info[0]
                            enemyType = info[1]
                            lastEnHp  = info[2]
                        
                    #bullets hitting brown enemies
                    for brown in brownGroup:
                        
                        #collision detection
                        if bmb.rect.colliderect(brown.rect) == True:
                            info = collideBulletEffect(bmb, 'bomb', brown, 100, score, 5, "b", enemyType, lastEnHp)
                            
                            #set information to variables in this loop
                            score     = info[0]
                            enemyType = info[1]
                            lastEnHp  = info[2]

                    #bullets hitting purple enemies
                    for purp in purpleGroup:
                        
                        #collision detection
                        if bmb.rect.colliderect(purp.rect) == True:
                            info = collideBulletEffect(bmb, 'bomb', purp, 10, score, 25, "p", enemyType, lastEnHp)
                        
                            #set information to variables in this loop
                            score     = info[0]
                            enemyType = info[1]
                            lastEnHp  = info[2]

#-----------#END COLLISION#-------------------------------------------------------------#END COLLISION#-----------------------------#

      # --- #SPECIAL EFFECTS# --- #
      
            #BROWN ENEMY (DUPLICATE)
            for brown in brownGroup:

                #increment this counter
                timeElapsed += 1

                #duplicate at # of increments
                if timeElapsed >= 1000:
                    duplicateEnemy(brown, brownGroup, BROWN, 1)

                    #reset increment counter
                    timeElapsed = 0
                    
      # --- #END SPECIAL EFFECTS# --- #
            
            #UPDATE
            windowSurface.fill(PINK)
            bombList.update()
            bulletList.update()
            p.update()
            purpleGroup.update()
            redGroup.update()
            brownGroup.update()
            whiteGroup.update()

            #update game scene health label
            lblhealth = label("Health: " + str(p.health),
                              BLACK,
                              (6, 5),
                              font3,
                              False)
            #update game scene score label
            lblscore = label("Score: " + str(score),
                             BLACK,
                             (6, 17),
                             font3,
                             False)
            #update game scene level label
            lbllevel = label("Level: " + str(lvl),
                             BLACK,
                             (6, 29),
                             font3,
                             False)
            #update game scene lastEnemyHit label
            lbllastEnemyHit = label(enemyType + " Health: " + str(lastEnHp),
                                    BLACK,
                                    (6, 41),
                                    font3,
                                    False)
            
            #update display
            pygame.display.update()
            
            #lose conditions
            if p.health <= 0:
                endGame(False, score, lvl)
            if len(whiteGroup) == 0:
                endGame(False, score, lvl)
                
            #next level
            if len(redGroup) == 0:
                if len(brownGroup) == 0:
                    if len(purpleGroup) == 0:
                        lvl += 1
            #level data
            if lvl > 10:
                endGame(True, score, lvl)
                
            #limit fps to 60fps
            timer.tick(60)

#---#END MAIN GAME LOOP#----------------------------------------------------------------#END MAIN GAME LOOP#------------------------#
#---#END MAIN#--------------------------------------------------------------------------#END MAIN#----------------------------------#



#if this is file running, run this main
if __name__ == "__main__":
    main()
