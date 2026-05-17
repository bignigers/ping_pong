#Создай собственный Шутер!

from pygame import *
from random import randint
number = 4
total1 = 0
total2 = 0
win_width = 1000
win_height = 700
font.init()
font = font.SysFont("Arial",30)
finished = False
gameOver = False


class GameSprite(sprite.Sprite): 
    def __init__(self, player_image, player_x, player_y, size_x, size_y): 
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):    
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_y_speed,number):
        
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.y_speed = player_y_speed
        self.number = number
        self.size_y = size_y
       
        
    
    def update(self):
        keys_pressed = key.get_pressed()
       
        if keys_pressed[K_w] and self.rect.y > 0 and self.number == 1:
            self.rect.y -= self.y_speed
        if keys_pressed[K_s] and self.rect.y < win_height - self.size_y and self.number == 1:
            self.rect.y += self.y_speed
        if keys_pressed[K_o] and self.rect.y > 0 + self.size_y/2 and self.number == 2:
            self.rect.y -= self.y_speed
        if keys_pressed[K_l] and self.rect.y < win_height- self.size_y and self.number == 2:
            self.rect.y += self.y_speed
        self.reset()
class Ball(GameSprite):
    def __init__(self,ball_image,ball_x,ball_y,size_x,size_y,ball_speed):
        super().__init__(ball_image,ball_x,ball_y,size_x,size_y)
        self.x_speed  = randint(-ball_speed,ball_speed)
        self.y_speed  = randint(-ball_speed,ball_speed)
        
        self.ball_speed = ball_speed
        while self.x_speed == 0:
            self.x_speed  = randint(-ball_speed,ball_speed)
            self.y_speed  = randint(-ball_speed,ball_speed)
        
    def respawn(self):
        self.x_speed  = randint(-self.ball_speed,self.ball_speed)
        self.y_speed  = randint(-self.ball_speed,self.ball_speed)
        while self.x_speed == 0 and self.y_speed == 0:
            self.x_speed  = randint(-self.ball_speed,self.ball_speed)
            self.y_speed  = randint(-self.ball_speed,self.ball_speed)
        self.rect.x,self.rect.y = 350,350
    def update(self):
        global total1,total2
        
        if Rect.colliderect(self.rect, player1.rect) or  Rect.colliderect(self.rect, player2.rect):
            self.x_speed *= -1
        if self.rect.y < 0:
            self.y_speed *= -1
        if self.rect.y > win_height-100:
            self.y_speed *= -1
        if self.rect.x < 0:
            total2+=1
            self.respawn()
        if self.rect.x > win_width:
            total1+=1
            self.respawn()
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        self.reset()
        
        
        






def update_status():
    text = f"Счет: {total1}"
    text_surface = font.render(text, True, Color("white"))
    text1 = f"Счет: {total2}"
    text_surface1 = font.render(text1, True, Color("white"))
    window.blit(text_surface,(0,0))
    window.blit(text_surface1,(900,0))
         
    

mixer.init()
#sound1 = mixer.Sound("space.ogg")  
#sound2 = mixer.Sound("fire.ogg")  
#channel1 = mixer.Channel(0)  
#channel1.play(sound1)
#channel2 = mixer.Channel(1)
window = display.set_mode((1000, 700))
display.set_caption("Maze")
background = transform.scale(image.load("fon.png"),(1000, 700))
player1 = Player("player1.png",75,350,30,230,11,1)
player2 = Player("player2.png",win_width-75,350,30,230,11,2)
ball1 = Ball("ball3.png",500,350,100,100,16)

game = True
clock = time.Clock()
FPS = 60
while game:
   
    print(total1,total2)
    if total1 >= 2 or total2 >= 2:
        finished = True
        print("finish")
    if finished == False:
        window.blit(background,(0,0))
        player1.update()
        player2.update()
        ball1.update()
        update_status()
    else:
        if total1 >= 10:text = f"Победил игрок 1"
        else:text = f"Победил игрок 2"
        text_surface = font.render(text, True, Color("Green"))
        window.blit(text_surface,(0,0))
    for e in event.get():
            if e.type == QUIT:
                game = False
    
    display.update()
    clock.tick(FPS)
