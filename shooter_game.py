from pygame import *
from random import randint
level = 1
win_width = 700
win_height = 500
lost = 0
goal = 10
maxlost = 3
score = 0
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
display.set_caption("Шутер")
finish = False
game = True
#классы
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_LEFT] and self.rect.x <= 5:
            self.rect.x += 600
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_RIGHT] and self.rect.x >= win_width - 80:
            self.rect.x -= 600
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx-7, self.rect.centery-35, 15, 20, 15)
        bullets.add(bullet)
        fire.play()
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width-80)
            self.rect.y = 0
            lost += 1

def level_reset():
    global level
    global goal
    global score
    global finish
    global ufos
    global bullets
    global lost
    global maxlost
    level = 1
    goal = 10
    maxlost = 3
    lost = 0
    score = 0
    for ufo in ufos:
        ufo.kill()
    for bullet in bullets:
        bullet.kill()
    finish = False

def level_up():
    global level
    global goal
    global score
    global finish
    global ufos
    global bullets
    global lost
    global maxlost
    lost = 0
    level+=1
    goal += 10
    score = 0
    finish = False
    for ufo in ufos:
        ufo.kill()
    for bullet in bullets:
        bullet.kill()
    if level == 5:
        maxlost= 2
    if level == 6 or level == 9 or level == 12:
        rocket.speed-=1

#экземпляры
player = Player('rocket.png', 250, win_height - 100, 75, 120, 8)
#font
font.init()
font = font.SysFont('Arial', 36)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))
lose_two = font.render('Press "r" to restart the game', True, (160, 0, 0))
#звуки
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

ufos = sprite.Group()
for i in range(1, 6):
    ufo = Enemy('ufo.png', randint(80, win_width-80), 49, 80, 50, randint(1, 5))
    ufos.add(ufo)
bullets = sprite.Group()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    if finish != True:
        text = font.render("счёт:" + str(score), 1, (255, 255, 255))
        text_lose = font.render("пропущено:" + str(lost), 1, (255, 255, 255))
        text_lev = font.render("уровень:" + str(level), 1, (255, 255, 255))
        window.blit(background, (0, 0))
        window.blit(text, (0, 0))
        window.blit(text_lose, (0, 20))
        window.blit(text_lev, (0, 40))
        player.reset()
        player.update()
        ufos.update()
        ufos.draw(window)
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(bullets, ufos, True, True)# столкновение
        for ufo in collides:
            ufo = Enemy("ufo.png", randint(80, win_width-80), -40, 80, 50, randint(1, 5))
            ufos.add(ufo)
            score+=1
        if sprite.spritecollide(player, ufos, False) or lost >= maxlost:
            lost+=1
            finish = True
            window.blit(lose, (200, 200))
            window.blit(lose_two, (150, 240))
        if len(ufos) < 5:
            ufo = Enemy("ufo.png", randint(80, win_width-80), -40, 80, 50, randint(1, 5))
            ufos.add(ufo)
        if score >= goal:
            finish = True
            level_up()
            window.blit(win, (200, 200))
    if finish == True:
        keys = key.get_pressed()
        if keys[K_r]:
            level_reset()
    display.update()
    time.delay(25)
