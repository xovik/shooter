
from pygame import *
from random import randint

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
fire_lose = mixer.Sound('firee.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x=60, size_y=60): 
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
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.add(bullet)
        fire_sound.play()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1
            fire_lose.play()

class Bullet(GameSprite):
    def __init__(self, x, y): 
        super().__init__("bullet.png", x, y, 15, 10, 20)
        self.speed = -15
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
asteroids = sprite.Group()
for i in range(2):
    asteroid = Asteroid("asteroid.png", randint(80, win_width - 80), 0, randint(1, 2))
    asteroids.add(asteroid)

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 72) 

enemies = sprite.Group()

for i in range(5):
    enemy = Enemy("ufo.png", randint(80, win_width - 80), 0, randint(1, 2))
    enemies.add(enemy)

player = Player("rocket.png", 300, 430, 5)
bullets = sprite.Group()

score = 0
lost = 0

lives = 3
game = True
FPS = 60
clock = time.Clock()
finish = False

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()

    window.blit(background, (0, 0))

    if finish != True:
        player.update()
        asteroids.update()
        enemies.update()
        bullets.update()

        collided_asteroids = sprite.spritecollide(player, asteroids, True)
        for asteroid in collided_asteroids:
            lives -= 1
            text_lose = font2.render("-1", 1, (255, 0, 0))
            window.blit(text_lose, (300, 400))

        if sprite.spritecollide(player, enemies, False):
            finish = True
            lives -= 3

        collisions = sprite.groupcollide(enemies, bullets, True, True)
        for enemy in collisions:
            score += 1
            enemy = Enemy("ufo.png", randint(80, win_width - 80), 0, randint(1, 2))
            enemies.add(enemy)

        if score >= 10:
            finish = True
        if lost >= 3:
            finish = True
        if lives <= 0:
            finish = True
    text_score = font1.render("Счет: " + str(score), 1, (255, 255, 255))
    window.blit(text_score, (5, 5))
    text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
    window.blit(text_lose, (5, 40))
    text_lives = font1.render("Жизни: " + str(lives), 1, (255, 255, 255))
    window.blit(text_lives, (5, 80))
    if finish:
        if score >= 10:
            text_win = font2.render("ВЫ ВЫИГРАЛИ!", 1, (0, 255, 0))
            window.blit(text_win, (200, 200))
        if lost >= 3:
            text_lose = font2.render("ВЫ ПРОИГРАЛИ!", 1, (255, 0, 0))
            window.blit(text_lose, (200, 200))
        if lives <= 0:
            text_lose = font2.render("ВЫ ПРОИГРАЛИ!", 1, (255, 0, 0))
            window.blit(text_lose, (200, 200))

           
    player.reset()
    asteroids.draw(window)
    enemies.draw(window)
    bullets.draw(window)
    display.update()
    clock.tick(FPS)