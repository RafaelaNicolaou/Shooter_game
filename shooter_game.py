#Create your own shooter
from random import randint
from datetime import datetime
from pygame import *
from PyQt5 import *

class GameSprite(sprite.Sprite):
    def __init__(self,image_file, w, h, x, y):
        super().__init__()

        print('Initializing gamesprite...'+image_file)

        self.width = w
        self.height = h
        self.image = image.load(image_file)
        self.image = transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def show(self, window):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):

    def __init__(self, image_file, w, h, x1, y1):
        super().__init__(image_file, w, h, x1, y1)

        print('Initializing player...')
        self.rocket_x = self.rect.x
        self.bullets = sprite.Group()
        self.num_fire = 0
        self.reloading = False

    def Player_con(self):
        now = datetime.now()
        keys_pressed = key.get_pressed()
        #creating the controles
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= 1
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += 1
        if keys_pressed[K_SPACE]:
            if self.num_fire < 10:
                self.bullets.add(Bullet("bullet.png", 10, 30, self.rect.centerx, self.rect.centery))
                self.num_fire = self.num_fire + 1
                print(self.num_fire)
            else:
                if self.reloading == False:
                    self.rel_start_time = datetime.now()
                
                self.reloading = True

        if self.reloading == True:
            self.d_time = now - self.rel_start_time
            print("Time Gone:", self.d_time.seconds)
            if self.d_time.seconds >= 3:
                self.num_fire = 0
                self.reloading = False
                    
lost = 0
shot = 0
class Enemy(GameSprite):
    
    def __init__(self, image_file, w, h, x, y):
        super().__init__(image_file, w, h, x, y)

        print("In Enemy class")
        self.iteration = 0
        self.direction = -1
        self.speed = randint(1, 5)
        print("Speed: ",self.speed)

    def update(self):
        global lost

        self.iteration = (self.iteration + 1)

        if self.iteration >= 15/self.speed:
            self.rect.y += 1
            direction = randint(-1,1)
            self.rect.x += direction*randint(1,5)
            self.iteration = 0
        
        if self.direction == 1:
            self.rect.x += randint(1, 10)
        
        if self.rect.y == 500:
            self.rect.y += randint(1, 10) 
            self.rect.y = 0
            lost = lost + 1

# Sprite_x = Player.rect.x
# Sprite_y = Player.rect.y

class Bullet(GameSprite):
    def __init__(self, image_file, w, h, x, y):
        super().__init__(image_file, w, h, x, y)

        self.speed = 5
    # self.Sprite_center_x = Player.rect.centerx
    # self.Sprite_top = Player.rect.top

    def update(self):
        self.rect.centery -= self.speed

#background
window = display.set_mode((700, 500))
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

#sprites
monsters = sprite.Group()
asteroids = sprite.Group()
rocket = Player("rocket.png", 75, 100, 300, 375)
monster1 = Enemy("ufo.png", 50, 50, 300, 0)
monster2 = Enemy("ufo.png", 50, 50, 260, 0)
monster3 = Enemy("ufo.png", 50, 50, 140, 0)
monster4 = Enemy("ufo.png", 50, 50, 290, 0)
monster5 = Enemy("ufo.png", 50, 50, 230, 0)
asteroid1 = Enemy("asteroid.png", 50, 50, 230, 0)
asteroid2 = Enemy("asteroid.png", 50, 50, 230, 0)
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)
asteroids.add(asteroid1)
asteroids.add(asteroid2)

clock = time.Clock()
FPS = 60
clock.tick(FPS)

# Setup Messages
font.init()
my_font = font.SysFont('Comic Sans MS', 100)
win_txt = my_font.render('YOU WIN!', False, (255, 215, 0))
lose_txt = my_font.render('YOU LOSE!', False, (45, 0, 215))
rel_font = font.SysFont('Comic Sans MS', 25)
font.init()
style = font.SysFont("Arial", 36)

#music
mixer.init()
mixer.music.load("space.ogg")
fire = mixer.Sound("fire.ogg")
mixer.music.play()

finish = False
run = True
while run:
    
    #putting the sprite and the backgraound in the screne
    text_lose = style.render("Missed: " + str(lost), 1, (255, 255, 255))
    text_shot = style.render("Shooted: " + str(shot), 1, (255, 255, 255))
    window.blit(background,(0, 0))
    window.blit(text_shot, (10, 20))
    window.blit(text_lose, (10, 50))
    rocket.show(window)
    rocket.bullets.draw(window)
    monsters.draw(window)
    asteroids.draw(window)

    if rocket.reloading == True:
        rel_txt = rel_font.render('reloading bullets...('+str(3-rocket.d_time.seconds)+' sec)', False, (255, 0, 0))
        window.blit(rel_txt, (200, 460))

    # if sprite.collide_rect(bullet1, monster1) or sprite.collide_rect(bullet1, monster2) or sprite.collide_rect(bullet1, monster3) or sprite.collide_rect(bullet1, monster4) or sprite.collide_rect(bullet1, monster5):
    #    shot = shot + 1
    #    print("Hit")

    for bullet1 in rocket.bullets:
        gets_hit = sprite.spritecollide(bullet1, monsters, True)
        if len(gets_hit) > 0:
            fire.play()
            rocket.bullets.remove(bullet1)
            shot = shot + len(gets_hit)
            print(gets_hit)
            monsters.add(Enemy("ufo.png", 50, 50, randint(0, 700), 0))

    #win or lose
    for e in event.get():
        # print(e)
        if e.type == QUIT:
            run = False

    if shot >= 10 and finish == False:
        txt = win_txt
        finish = True

    elif sprite.spritecollide(rocket, monsters, False) or lost == 3 and finish == False:#or sprite.spritecollide(rocket, asteroid1, False) or sprite.spritecollide(rocket, asteroid2, False)
        txt = lose_txt
        finish = True  

    elif sprite.spritecollide(rocket, asteroids, False):
        txt = lose_txt
        finish = True     

    if finish == False:
        # enemy.move_BF()
        rocket.bullets.update()
        monsters.update()
        rocket.Player_con()
        asteroid1.update()
        asteroid2.update()
    else:
        window.blit(txt, (100, 200))


    display.update()