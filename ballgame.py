import sys
import pygame


white=(255,255,255)
grey=(150,150,150)
pcolor=(208,32,144)
bcolor=(200,200,0)
bwidth=70
bheight=18
bdiam=25
scrsize=720,560
pheight=17
bradius=bdiam//2
maxballxdim=scrsize[0] - bdiam
mballydim=scrsize[1] - bdiam
boardydim=scrsize[1] - pheight - 10
pwidth=100
maxpxdim=scrsize[0]-pwidth
ball_board=0
game_time=1
win=2
lost=3

class ballplay:

    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(scrsize)
        pygame.display.set_caption("BALL PLAY")
        
        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font(None,30)
        else:
            self.font = None

        self.init_game()

        
    def init_game(self):
        self.chance = 3
        self.exp = 0
        self.state = ball_board

        self.paddle   = pygame.Rect(300,boardydim,pwidth,pheight)
        self.ball     = pygame.Rect(300,boardydim - bdiam,bdiam,bdiam)

        self.ball_vel = [5,-5]

        self.cbr()
        

    def cbr(self):
        yspc = 40
        self.bricks = []
        for i in range(10):
            xspc = 40
            for j in range(i):
                self.bricks.append(pygame.Rect(xspc,yspc,bwidth,bheight))    
                xspc += bwidth + 5
            yspc += bheight + 10

    def drbr(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, bcolor, brick)
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.paddle.left -= 5
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT]:
            self.paddle.left += 5
            if self.paddle.left > maxpxdim:
                self.paddle.left = maxpxdim

        if keys[pygame.K_SPACE] and self.state == ball_board:
            self.ball_vel = [5,-5]
            self.state = game_time
        elif keys[pygame.K_RETURN] and (self.state == lost or self.state == win):
            self.init_game()

    def ballmotion(self):
        self.ball.left += self.ball_vel[0]
        self.ball.top  += self.ball_vel[1]

        if self.ball.left <= 0:
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= maxballxdim:
            self.ball.left = maxballxdim
            self.ball_vel[0] = -self.ball_vel[0]
        
        if self.ball.top < 0:
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= mballydim:            
            self.ball.top = mballydim
            self.ball_vel[1] = -self.ball_vel[1]

    def collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.exp += 3
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                break

        if len(self.bricks) == 0:
            self.state = win
            
        if self.ball.colliderect(self.paddle):
            self.ball.top = boardydim - bdiam
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top > self.paddle.top:
            self.chance -= 1
            if self.chance > 0:
                self.state = ball_board
            else:
                self.state = lost

    def shexp(self):
        if self.font:
            font_surface = self.font.render("chance- " + str(self.chance)+"                              exp--- " + str(self.exp), False, grey)
            self.screen.blit(font_surface, (205,5))

    def shmessage(self,message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message,False, grey)
            x = (scrsize[0] - size[0]) / 2.2 
            y = (scrsize[1] - size[1]) / 1.2
            self.screen.blit(font_surface, (x,y))
        
            
    def play(self):
        while 1:            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.clock.tick(50)
            self.screen.fill(white)
            self.input()

            if self.state == game_time:
                self.ballmotion()
                self.collisions()
            elif self.state == ball_board:
                self.ball.left = self.paddle.left + self.paddle.width / 2
                self.ball.top  = self.paddle.top - self.ball.height
                self.shmessage("Ready to play!!!! ")
            elif self.state == lost:
                self.shmessage("Better luck next time"+"       total exp:"+ str(self.exp))
            elif self.state == win:
                self.shmessage("CONGRATULATIONS!"+"       total exp:"+ str(self.exp))
                
            self.drbr()

            
            pygame.draw.rect(self.screen, pcolor, self.paddle)
            pygame.draw.circle(self.screen, grey, (self.ball.left + bradius, self.ball.top + bradius), bradius)

            self.shexp()

            pygame.display.flip()

if __name__ == "__main__":
    ballplay().play()
