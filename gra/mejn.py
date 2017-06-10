#LoC
#Space Tuna by Möbius is licensed under a Attribution-NonCommercial-ShareAlike License.


# Importy
import pygame
import random
import os

# Wymiary okna
WIDTH = 480
HEIGHT = 600
POWERUP_TIME = 5000
# Szybkosc gry
FPS = 60
# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Foldery z assetami

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
sfx_folder = os.path.join(game_folder, "sfx")

# Funkcje


# klasy

font_name = pygame.font.match_font('comic_sans')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGTH = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGTH)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGTH)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "LoC", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, " Arrow keys move, Z to fire", 22, WIDTH /2, HEIGHT /2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 /4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
class Gracz(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 10
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # powerupy
        if self.power >2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -=1
            self.power_time = pygame.time.get_ticks()

        # unhide
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_z]:
            self.shoot()

        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def powerup(self):
        self.power +=1
        self.power_time - pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullets(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sfx.play()
            if self.power >= 2:
                bullet1 = Bullets(self.rect.left, self.rect.centery)
                bullet2 = Bullets(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                bullets.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet2)
                shoot_sfx.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(random.choice(meteor_images), (40, 35))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 7)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = self.rot + self.rot_speed % 360
            image_copy = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = image_copy
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

# Inicjalizacja
pygame.init()
pygame.mixer.init()
# Inicjalizacja ekranu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Tytuł okna
pygame.display.set_caption("Lack of Coffins")
# Zegar gry
clock = pygame.time.Clock()


# grafika

background = pygame.image.load(os.path.join(img_folder, "background.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_folder, "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(os.path.join(img_folder, "laserBlue16.png")).convert()
meteor_images = []
meteor_list = ['meteor.png', 'meteor2.png', 'meteor3.png']

for img in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(img_folder, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(os.path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

powerup_images = {}
powerup_images['shield'] = pygame.image.load(os.path.join(img_folder, "shield_gold.png")).convert()
powerup_images['gun'] = pygame.image.load(os.path.join(img_folder, "bolt_gold.png")).convert()



##
#sfx
shoot_sfx = pygame.mixer.Sound(os.path.join(sfx_folder, 'Laser_Shoot2.wav'))
expl_sfx = []

for sfx in ['Explosion.wav', 'Explosion2.wav', 'Explosion3.wav', 'Explosion4.wav']:
    expl_sfx.append(pygame.mixer.Sound(os.path.join(sfx_folder, sfx)))
pygame.mixer.music.load(os.path.join(sfx_folder, 'menu.mp3'))
pygame.mixer.music.set_volume(0.9)

# Sprajty


pygame.mixer.music.play(-1)

# Game LOOP
game_over = True
running = True
while running:

    if game_over:
        show_go_screen()
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        gracz = Gracz()
        powerups = pygame.sprite.Group()
        all_sprites.add(gracz)
        for i in range(8):
            newmob()
        score = 0

        game_over = False

    # fpsy
    clock.tick(FPS)

    # eventy
    for event in pygame.event.get():

        # X w oknie
        if event.type == pygame.QUIT:
            running = False
    # Update
    all_sprites.update()

    # sprawdz kolizje

    # hit pociski

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 50
        random.choice(expl_sfx).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    # hit gracza
    hits = pygame.sprite.spritecollide(gracz, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        gracz.shield -= 20
        random.choice(expl_sfx).play()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if gracz.shield <= 0:
            random.choice(expl_sfx).play()
            death_explosion = Explosion(gracz.rect.center, 'player')
            all_sprites.add(death_explosion)
            gracz.hide()
            gracz.lives -= 1
            gracz.shield = 100
    # hit powerupu
    hits = pygame.sprite.spritecollide(gracz, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            gracz.shield +=20
            if gracz.shield >= 100:
                gracz.shield = 100
        if hit.type == 'gun':
            gracz.powerup()
    if gracz.lives == 0 and not death_explosion.alive():
        game_over = True

    # Draw
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, gracz.shield)
    draw_lives(screen, WIDTH - 100, 5, gracz.lives, player_mini_img)
    # Po Wszystkim
    pygame.display.flip()

pygame.quit()