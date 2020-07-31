import pygame
import random
import math
from pygame import mixer

#initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode([800,600])

#title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('.\sprites\invd1.png')
pygame.display.set_icon(icon)

#background
background = pygame.image.load('.\sprites\spaceinvbackg.png')
#background sound
mixer.music.load('.\sounds\mainmusic.wav')
mixer.music.play(-1)
#general sounds
laser_Sound = mixer.Sound('.\sounds\laser.wav')
explosion_sound = mixer.Sound('.\sounds\explosion.wav')


#player
playerimg = pygame.image.load('.\sprites\plr.png')
playerX = 370
playerY = 550
playerX_change = 0

#laser
laserimg = pygame.image.load('.\sprites\laser.png')
laserX = 0
laserY = playerY
laserY_change = 15
laser_state = "ready"


#enemy1
enemyimg1 = []
enm1X = []
enm1Y = []
enm1X_change = []
enm1Y_change = []
num_of_enemies1 = 6

for i in range(num_of_enemies1):
    enemyimg1.append(pygame.image.load('.\sprites\invd2.png'))
    enm1X.append(random.randint(0,770))
    enm1Y.append(random.randint(50,150))
    enm1X_change.append(1.50)
    enm1Y_change.append(40)
#enemy2
enemyimg2 = []
enm2X = []
enm2Y = []
enm2X_change = []
enm2Y_change = []
num_of_enemies2 = 4

for i in range(num_of_enemies2):
    enemyimg2.append(pygame.image.load('.\sprites\invd3.png'))
    enm2X.append(random.randint(0,770))
    enm2Y.append(random.randint(50,150))
    enm2X_change.append(4)
    enm2Y_change.append(0.2)


#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#Game Over text
over_font = pygame.font.Font('freesansbold.ttf',120)

def game_over_text():
    over_text = font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text,(300,300))

def show_score(x,y):
    score = font.render("Score:" + str(score_value), True, (255,255,255))
    screen.blit(score,(x,y))

def player(x,y):
    screen.blit(playerimg, (round(x),round(y)))

###
def enemy1(x,y,i):
    screen.blit(enemyimg1[i], (round(x),round(y)))
def enemy2(x,y,i):
    screen.blit(enemyimg2[i], (round(x),round(y)))


def fire_laser(x,y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserimg, (x,y))


###
def isCollision1(enm1X,enm1Y,laserX,laserY):
    distance = math.hypot(enm1X - laserX, 2) + math.pow(enm1Y - laserY, 2)

    if distance < 50:
        return True
    else:
        return False
def isCollision2(enm2X,enm2Y,laserX,laserY):
    distance = math.hypot(enm2X - laserX, 2) + math.pow(enm2Y - laserY, 2)

    if distance < 40:
        return True
    else:
        return False


#game loop
running = True
while running:

    #RGB - Red, Green, Blue
    screen.fill([0,0,0])
    #background image
    screen.blit(background,(0,0))

    #events sequence
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if laser_state is "ready":
                    laser_Sound.play()
                    laserX = playerX
                    fire_laser(laserX, laserY)
                         
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 770:
        playerX = 769 


    ##enemy movement and boundaries 1
    for i in range(num_of_enemies1):

        #Game over
        if enm1Y[i] > 550:
            for j in range(num_of_enemies1):
                enm1Y[j] = 2000
                enm2Y[j] = 2000
            game_over_text()
            break

        enm1X[i] += enm1X_change[i]
        if enm1X[i] <=0:
            enm1X_change[i] = 1.50
            enm1Y[i] += enm1Y_change[i]

        if enm1X[i] >= 770:
            enm1X_change[i] = -1.50
            enm1Y[i] += enm1Y_change[i]

        #Collision 1
        collision1 = isCollision1(enm1X[i],enm1Y[i],laserX,laserY)
        if collision1:
            explosion_sound.play()
            laserY = 480
            laser_state = "ready"
            score_value += 1
            print(score_value)
            enm1X[i] = random.randint(0,770)
            enm1Y[i] = random.randint(50,150)

        enemy1(enm1X[i],enm1Y[i],i)
    ##enemy movement and boundaries 2
    for i in range(num_of_enemies2):

        #Game over
        if enm2Y[i] > 550:
            for j in range(num_of_enemies2):
                enm2Y[j] = 2000
                enm1Y[j] = 2000
            game_over_text()
            break

        enm2Y[i] += enm2Y_change[i]
        enm2X[i] += enm2X_change[i]
        if enm2X[i] <=0:
            enm2X_change[i] = 4
            

        if enm2X[i] >= 770:
            enm2X_change[i] = -4
            

        #Collision 2
        collision2 = isCollision2(enm2X[i],enm2Y[i],laserX,laserY)
        if collision2:
            explosion_sound.play()
            laserY = 480
            laser_state = "ready"
            score_value += 1
            print(score_value)
            enm2X[i] = random.randint(0,770)
            enm2Y[i] = random.randint(50,150)

        enemy2(enm2X[i],enm2Y[i],i)

    #laser movement
    if laserY < 0:
        laserY = 550
        laser_state = "ready"

    if laser_state is "fire":
        fire_laser(laserX,laserY)
        laserY -=laserY_change
    

    player(playerX,playerY)
    show_score(textX,textY)

    pygame.display.update()