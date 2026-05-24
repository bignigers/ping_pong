#Создай собственный Шутер!
import os
from pygame import *
from random import randint
current_dir = os.getcwd()
elos = []
try:
    with open('score.txt', 'r') as file:
        for i in file.readlines():
            elos.append(i)
        print("Успешно прочитано")
    elo1 = int(elos[0])
    elo2 = int(elos[1])
except FileNotFoundError:
    with open('score.txt', 'w') as file:
        file.write("0\n0")
        print("Создан новый файл")
    elo1 = 0
    elo2 = 0
except IOError as e:
    print(f"Произошла ошибка: {e}")
start_time = time.get_ticks()
score_for_finish = 10
number = 4
total1 = 0
total2 = 0
draw = False
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
        if keys_pressed[K_o] and self.rect.y > 0  and self.number == 2:
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
        while abs(self.x_speed) <= 4:
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
            self.x_speed += 0.1
            self.y_speed += 0.05
        if self.rect.y < 0:
            self.y_speed *= -1
            self.x_speed += 0.1
            self.y_speed += 0.05
        if self.rect.y > win_height-100:
            self.y_speed *= -1
            self.x_speed += 0.1
            self.y_speed += 0.05
        if self.rect.x < 0:
            total2+=1
            self.respawn()
            self.ball_speed += 1
        if self.rect.x > win_width:
            total1+=1
            self.respawn()
            self.ball_speed += 1
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        
        self.reset()
        
        
        



def save_elo():
    
    try:

        with open('score.txt', 'w') as file:
            
            file.write(f"{elo1}\n{elo2}")
            print(f"Сохранено {elo1}/{elo2}")
        print("Elo сохранено")
    except:
        print("Ошибка пр сохранении")


def update_status():
    text = f"Счет: {total1}"
    text_surface = font.render(text, True, Color("white"))
    text1 = f"Счет: {total2}"
    text_surface1 = font.render(text1, True, Color("white"))
    text_elo1 = f"ELO: {elo1}"
    text_surface2 = font.render(text_elo1, True, Color("white"))
    text_elo2 = f"ELO: {elo2}"
    text_surface3 = font.render(text_elo2, True, Color("white"))
    window.blit(text_surface,(0,0))
    window.blit(text_surface1,(900,0))
    window.blit(text_surface2,(0,30))
    len_text_elo2 = len(str(elo2))
    window.blit(text_surface3,(905-len_text_elo2*10,30))
    
         
    

mixer.init()
#sound1 = mixer.Sound("fon_music.mp3")  
#sound2 = mixer.Sound("fire.ogg")  
#channel1 = mixer.Channel(0)  
#channel1.play(sound1)
#channel2 = mixer.Channel(1)
window = display.set_mode((win_width, win_height))
display.set_caption("ping_pong")
background = transform.scale(image.load("fon.png"),(win_width, win_height))
player1 = Player("player1.png",110,350,30,230,11,1)
player2 = Player("player2.png",win_width-110,350,30,230,11,2)
ball1 = Ball("ball3.png",500,350,100,100,16)

game = True
clock = time.Clock()
FPS = 60
while game:
   
    
    if total1 >= score_for_finish and finished == False:
        elo1 += 50
        finished = True
        save_elo()
        
        
    elif total2 >= score_for_finish and finished == False:
        elo2 += 50
        finished = True
        save_elo()
        
        
    if finished == False:
        window.blit(background,(0,0))
        player1.update()
        player2.update()
        ball1.update()
        update_status()
    else:
        if draw:
            text = "НИЧЬЯ"
        else:

            if total1 >= score_for_finish:text = f"Победил игрок 1"
            else:text = f"Победил игрок 2"
        text_surface = font.render(text, True, Color("Green"))
        window.blit(text_surface,(400,350))
    for e in event.get():
            if e.type == QUIT:
                game = False
            
    if time.get_ticks() - start_time >= 100 * 1000:
        if total1 > total2:
            elo1 += 50
            finished = True
            save_elo()
        elif total2 > total1:
            elo2 += 50
            finished = True
            save_elo()
        else:
            finished = True          
    display.update()
    clock.tick(FPS)
