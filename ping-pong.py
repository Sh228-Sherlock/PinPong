from pygame import *
from random import randint

win_width = 700 # window
win_height = 500
window = display.set_mode((win_width, win_height))

direction = 1
display.set_caption('Pin-Pong')
background =(200, 200, 200)
font.init() # font
font = font.Font(None, 70)
lose = font.render('YOU LOSE!', True, (180, 0, 0))

game = True # переменные
finish = False
clock = time.Clock() # таймер
FPS = 60 # фпс

class GameSprite(sprite.Sprite): # основной класс

    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, direction):
        super(). __init__()

        self.image = transform.scale(image.load(player_image), (size_x, size_y))#, (55, 55))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.direction = direction

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_passed = key.get_pressed()
        if keys_passed[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_passed[K_DOWN] and self.rect.y < win_height -80:
            self.rect.y += self.speed
    def updatetwo(self):
        keys_passed = key.get_pressed()
        if keys_passed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_passed[K_s] and self.rect.y < win_height -80:
            self.rect.y += self.speed

class Ball(GameSprite):
    def update(self): # вверх вправо/вверх влево/вниз вправо/вниз влево
        if self.direction == 1:
            self.rect.x += 5
            self.rect.y -=5
        elif self.direction == 4:
            self.rect.x -= 5
            self.rect.y -=5
        elif self.direction == 2:
            self.rect.x += 5
            self.rect.y +=5
        elif self.direction == 3:
            self.rect.x -= 5
            self.rect.y +=5
        if self.rect.y < 0:
            if self.direction == 1:
                self.direction = 2
            elif self.direction == 4:
                self.direction = 3
        if self.rect.y > 450:
            if self.direction == 2:
                self.direction = 1
            elif self.direction == 3:
                self.direction = 4

# наследники
player1 = Player('platforma.png', 10, 120, 10, 60, 10, 0)
player2 = Player('platforma.png', 670, 120, 10, 60, 10, 0)
game_ball = Ball('game_ball.jpg', 200, 200, 80, 80, 10, randint(1, 4))

while game: # игровой цикл
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.fill(background)
        player1.updatetwo()
        player2.update()
        player1.reset()
        player2.reset()
        game_ball.update()
        game_ball.reset()
        if sprite.collide_rect(game_ball, player1): # мяч отскакивает от платформ
            if game_ball.direction == 4:
                game_ball.direction = 1
            elif game_ball.direction == 3:
                game_ball.direction = 2
        if sprite.collide_rect(game_ball, player2):
            if game_ball.direction == 2:
                game_ball.direction = 3
            elif game_ball.direction == 1:
                game_ball.direction = 4
        if game_ball.rect.x < 0 or game_ball.rect.x > 610:
            window.blit(lose, (200, 200))
            finish = True
    display.update() # завершение
    clock.tick(FPS)
