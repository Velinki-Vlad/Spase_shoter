from random import *
from pygame import *
from time import time as timer
window = display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (700,500))

win_witdh = 700
win_height = 500

font.init()
font1 = font.SysFont(None, 36)
font2 = font.SysFont(None, 75)

lost = 0

life = 3

real_time = False

num_fire = 0

finish = False

text_score =font1.render('Cщёт: 0', 1, (255, 255, 255))

text_lose = font1.render(
    'Пропущено: ' + str(lost), 1, (255, 255, 255)
)

text_win = font2.render('Вы выйграли', 1, (0,255,0))
text_lose1 = font2.render('Вы проиграли', 1, (255, 0, 0))
tetx_death = font2.render('Вы умерли', 1, (255, 0, 0))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

score = 0

clock = time.Clock()

img_enemy = 'ufo.png'

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x,player_y,size_x,size_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys [K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_witdh - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

player = Player('rocket.png',310, 400, 80, 100, 10 )
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range (1, 3):
    asteroid = Enemy('asteroid.png', randint(30, 500 - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

for i in range (1, 6):
    monster = Enemy(img_enemy, randint(80, win_witdh - 80), 40, 80, 50, randint(1, 3) )
    monsters.add(monster)
    
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and real_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()

                if num_fire >= 5 and real_time == False:
                    last_time = timer()
                    real_time = True
                
    if not finish:
        
        window.blit(background, (0, 0))
        asteroids.update()
        asteroids.draw(window)
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        player.update()
        player.reset()
        text_lose = font1.render(
            'Пропущено: ' + str(lost), 1, (255, 255, 255)
        )
        text_score = font1.render( 
            'Убито: ' +  str(score),1,(255, 255, 255)
        )
        
        if real_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                real_time = False

        sprites_list =sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_witdh - 80), -50  , 80, 50, randint(1, 3) )
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, monsters, True)
            sprite.spritecollide(player, asteroids, True)
            life = life - 1
        if score >= 10:
            print('Вы выйграли')
            finish = True
            window.blit(text_win, (200,250))
        if lost >= 3 or life == 0:
            print('Вы проиграли')
            finish = True
            window.blit(text_lose1, (180, 250))
            
        window.blit(text_lose, (10, 50))
        window.blit(text_score, (10, 10))
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)       
        text_love = font2.render(str(life), 1, life_color)
        window.blit(text_love, (650, 10))
    
    display.update()
    clock.tick(40)
