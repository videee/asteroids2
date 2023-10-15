from pygame import *
from random import *

w, h = 700, 500
window = display.set_mode((w, h))
display.set_caption('Asteroids')

game = True
finish = False
clock = time.Clock()
FPS = 60
background = transform.scale(image.load("galaxy.jpg"), (w, h))

class GameSprite(sprite.Sprite):
    def __init__(self, pImage, px, py, sizeX, sizeY, pSpeed):
        super().__init__()
        self.image = transform.scale(image.load(pImage), (sizeX, sizeY))
        self.speed = pSpeed
        self.rect = self.image.get_rect()
        self.rect.x = px
        self.rect.y = py
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx-7, self.rect.top, 15, 30, 15)
        bullets.add(bullet)
    

ship = Player("rocket.png", 10, h-100, 65, 95, 4)

lost = 0
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        global heart
        if self.rect.y > h:
            try:
                hearts.pop(0)
            except:
                pass
            self.rect.y = 0
            self.rect.x = randint(0, w-50)
            lost += 1

asteroids = sprite.Group()

for i in range(2):
    pics = ["asteroid.png", "ufo.png"]
    asteroid = Enemy(choice(pics), randint(0, w-50), -40, 50, 50, randint(1, 5))
    asteroids.add(asteroid)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

bullets = sprite.Group()        
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.2)
score = 0

font.init()
mainfont = font.Font("Super Corn.ttf", 40)
'''mainfont = font.Font(None, 40 ) #для тих хто не скачує'''

from time import time as timer
reload_time = False
num_fire = 0

hearts = []
lives = 10
hX = 300
for i in range(lives):
    heart = GameSprite("heart.png", hX, 10, 40, 37, 0)
    hearts.append(heart)
    hX += 40

restart = GameSprite("restart.png", 240, 200, 222, 125, 0)
start = GameSprite("start.png", 240, 250, 222, 100, 0)
exit = GameSprite("exit.png", 5, 5, 60, 60, 0)
finish = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and reload_time == False:
                    ship.fire()
                    fire_sound.play()
                    num_fire += 1
                if num_fire >= 5 and reload_time == False:
                    reload_time = True
                    reload_start = timer()
            if e.key == K_r:
                for a in asteroids:
                    a.rect.y = -100
                    a.rect.x = randint(0, w-100)
                finish, score, lost, = 0,0,0
                hearts = []
                lives = 10
                hx = 170
                for i in range(lives):
                    heart = GameSprite("heart.png", hx, 10, 40, 37, 0)
                    hearts.append(heart)
                    hx += 40

        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                x, y = e.pos 
                if restart.rect.collidepoint(x, y) and finish:
                    for a in asteroids:
                        a.rect.y = -100
                        a.rect.x = randint(0, w-100)
                    finish, score, lost, = 0,0,0
                    hearts = []
                    lives = 10
                    hx = 170
                    for i in range(lives):
                        heart = GameSprite("heart.png", hx, 10, 40, 37, 0)
                        hearts.append(heart)
                        hx += 40

    if finish:
        window.blit(background, (0,0))
        start.draw()
        exit.draw()


    if not finish:
        window.blit(background, (0, 0))
        score_text = mainfont.render("Killed: "+str(score), True, (0,255,0))
        lost_text = mainfont.render("Missed: "+str(lost), True, (0,255,0))
        window.blit(score_text, (5, 10))
        window.blit(lost_text, (5, 50))

        if reload_time:
            reload_end = timer()
            if reload_end - reload_start < 3:
                reload = mainfont.render("RELOADING...", True, (0,255,0))
                window.blit(reload, (200, 200))
            else:
                num_fire = 0
                reload_time = False

        ship.draw()
        ship.update()
        asteroids.update()
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)

        if sprite.spritecollide(ship, asteroids, False):
            restart.draw()
            lose_text = mainfont.render("YOU LOSE", True, (0,255,0))
            window.blit(lose_text, (200, 200))
            finish = True

        collides = sprite.groupcollide(bullets, asteroids, True, True)
        for c in collides:
            score += 1
            pics = ["asteroid.png", "ufo.png"]
            asteroid = Enemy(choice(pics), randint(0, w-50), -40, 50, 50, randint(1, 3))
            asteroids.add(asteroid)

        if lost >= 10:
            lose_text = mainfont.render("YOU LOSE", True, (0,255,0))
            window.blit(lose_text, (200, 200))
            finish = True

        for heart in hearts:
            heart.draw()

        if len(hearts) <= 0:
            restart.draw()
            lose_text = mainfont.render("YOU LOSE", True, (0,255,0))
            window.blit(lose_text, (200, 200))
            finish = True
        

    display.update()
    clock.tick(60)
