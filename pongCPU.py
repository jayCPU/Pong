import pygame
from pygame.locals import *

pygame.init()

SCR_WIDTH = 600
SCR_HEIGHT = 500

fpsClock = pygame.time.Clock()

screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
pygame.display.set_caption('Pong')



#game var
font = pygame.font.SysFont('comicsansms', 30)

liveBall = False
margin = 50
cpuScore = 0
playerScore = 0
fps = 90

winner = 0


#colors
bg = (50, 25, 50)
white = (255, 255, 255)



#functions
def drawBoard():
    screen.fill(bg)
    pygame.draw.line(screen, white, (0, margin), (SCR_WIDTH, margin))

def drawText(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))

class paddle():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, 20, 100)
        self.speed = 5

    def move(self):
        key = pygame.key.get_pressed()
        if (key[pygame.K_UP] or key[pygame.K_w]) and self.rect.top > margin + 25:
            self.rect.move_ip(0, -1 * self.speed)
        if (key[pygame.K_DOWN] or key[pygame.K_s]) and self.rect.bottom < SCR_HEIGHT - 25:
            self.rect.move_ip(0, 1 * self.speed)

    def AI(self):
        if self.rect.centery < pong.rect.top and self.rect.bottom < SCR_HEIGHT - 25:
            self.rect.move_ip(0, self.speed)
        if self.rect.centery > pong.rect.bottom and self.rect.top > margin + 25:
            self.rect.move_ip(0, -1 * self.speed)
            

    def draw(self):
        pygame.draw.rect(screen, white, self.rect)

class ball():
    def __init__(self, x, y):
        self.reset(x, y)
        
    def draw(self):
        
        #collision
        #height colliders
        if self.rect.top < margin + 25:
            self.speed_y *= -1
        if self.rect.bottom > SCR_HEIGHT - 25:
            self.speed_y *= -1
        
        #collision with paddles
        if self.rect.colliderect(playerPaddle) or self.rect.colliderect(cpuPaddle):
            self.speed_x *= -1
            
            
        #score update
        if self.rect.left < 0:
            self.winner = 1
        if self.rect.right > SCR_WIDTH:
            self.winner = -1
        
        pygame.draw.circle(screen, white, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        
    def move(self):
        
        #update ball pos
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        return self.winner
    
    def reset(self, x, y):
        self.x = x
        self.y = y
        self.ball_rad = 8
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = -4
        self.speed_y = 4
        self.winner = 0 #1 means player scored, - 1 means cpu scored


#create paddles & ball
playerPaddle = paddle(SCR_WIDTH - 40, SCR_HEIGHT // 2)
cpuPaddle = paddle(20, SCR_HEIGHT // 2)
    
pong = ball(SCR_WIDTH - 60, SCR_HEIGHT // 2 + 50)    

        

#display
on = True
while on:

    fpsClock.tick(fps)

    drawBoard()
    drawText('CPU: ' + str(cpuScore), font, white, 20, 2)
    drawText('You: ' + str(playerScore), font, white, SCR_WIDTH - 100, 2)

    #draw
    playerPaddle.draw()
    cpuPaddle.draw()
    
    if liveBall == True:
        #move ball
        winner = pong.move()
        if winner == 0:
            #move paddle 
            playerPaddle.move()
            cpuPaddle.AI()
            #draw ball          
            pong.draw()
        else:
            liveBall = False
            if winner == 1:
                playerScore += 1
            elif winner == -1:
                cpuScore += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False
        if event.type == pygame.MOUSEBUTTONDOWN and liveBall == False:
            liveBall = True
            pong.reset(SCR_WIDTH - 60, SCR_HEIGHT // 2 + 50)    
            
    pygame.display.update()

pygame.quit()