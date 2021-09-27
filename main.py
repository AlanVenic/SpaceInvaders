import pygame
from random import randint
from math import sqrt
from pygame import mixer

# iniciar o pygame
pygame.init()

#musica de fundo
mixer.music.load('background.wav')
mixer.music.play(-1)

# criar a tela (largura, altura)
screen = pygame.display.set_mode((800, 600))

#pontuação
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#game over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# fundo
background = pygame.image.load('background.jpg')

# titulo e icone
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# nave do jogador
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# bala
# ready: voce nao pode ver a bala
# fire: a bala está se movendo
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.2
bullet_state = 'ready'

# multiplos inimigos
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemies_num = 6

# nave do inimigo
for i in range(enemies_num):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(randint(0, 735))
    enemyY.append(randint(20, 100))
    enemyX_change.append(0.3)
    enemyY_change.append(40)


def game_over():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


# colisão da bala
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = sqrt(((enemyX - bulletX) ** 2) + ((enemyY - bulletY) ** 2))
    if distance < 27:
        return True
    else:
        return False


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fireBullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# game loop
running = True
while running:
    # Cor de fundo RGB - vermelho, verde, azul: 0 a 255
    screen.fill((0, 0, 0))
    # imagem de fundo
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # se uma tecla for pressionada, verifique se é esquerda ou direita
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # verificando os limites para que as naves não saiam da tela
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # movimento do inimigo
    for i in range(enemies_num):
        #GAME OVER
        if enemyY[i] > 440:
            for j in range(enemies_num):
                enemyY[j] = 2000
            game_over()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # colisão
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = randint(0, 735)
            enemyY[i] = randint(20, 100)
        enemy(enemyX[i], enemyY[i], i)

    # movimento da bala
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'
    if bullet_state == 'fire':
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change
    show_score(textX, textY)

    player(playerX, playerY)
    pygame.display.update()
