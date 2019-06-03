
# Imports
import pygame
import math
import random
import xbox360_controller

# Initialize game engine
pygame.init()


# Window
WIDTH = 1900
HEIGHT = 1000
SIZE = (WIDTH, HEIGHT)
TITLE = "Phase 4"
screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)


# Fonts

FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)
FONT_XL = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 96)


# Images
ship_img = pygame.image.load('assets/images/player.png').convert_alpha()
laser_img = pygame.image.load('assets/images/laserRed.png').convert_alpha()
enemy_img = pygame.image.load('assets/images/enemyShip.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/laserGreen.png').convert_alpha()
shieldshot_drop_img = pygame.image.load('assets/images/laserGreenShot.png').convert_alpha()
shield_img = pygame.image.load('assets/images/shield.png').convert_alpha()
HP_img = pygame.image.load('assets/images/Hp.png').convert_alpha()
earth_img = pygame.image.load('assets/images/earth.png').convert_alpha()
planet_img = pygame.image.load('assets/images/planet.png').convert_alpha()
planet2_img = pygame.image.load('assets/images/planet2.png').convert_alpha()

# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')


# Stages
START = 0
PLAYING = 1
END = 2
PAUSED = 3

controller = xbox360_controller.Controller(0)

stars = []
for i in range(230):
    x = random.randrange(0, 1900)
    y = random.randrange(0, 1000)
    
    q = random.randrange(4, 7)
    s =  [x, y, q, q]
    stars.append(s)

stars1 = []
for i in range(230):
    x1 = random.randrange(0, 1900)
    y1 = random.randrange(-1000, 0)
    
    q1 = random.randrange(4, 7)
    s1 =  [x1, y1, q1, q1]
    stars1.append(s1)
    
# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 5
        self.shield_ammo = 0
        self.health = 3
        self.score = 0
        self.value = 1
        self.kills = 0
        self.wave = 0
        

    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        print("pew")
        if len(lasers) < 10:
            laser = Laser(laser_img)
            laser.rect.centerx = self.rect.centerx
            laser.rect.bottom = self.rect.top - 5
            projectiles.add(laser)
            lasers.add(laser)

    def shoot_shield(self):
        if self.shield_ammo > 0:
            shield = Shield_shot(shield_img)
            shield.rect.centerx = self.rect.centerx
            shield.rect.bottom = self.rect.top
            shields.add(shield)
            self.shield_ammo -= 1
            
    def update(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.y < 700:
            self.rect.y = 700

        elif self.rect.bottom > 1000:
            self.rect.bottom = 1000
        hit_list = pygame.sprite.spritecollide(self, projectiles, True)

        mob_hit_list = pygame.sprite.spritecollide(self, mobs, True)

        if len(mob_hit_list) > 0:
            self.health  = 0
            
        if len(hit_list) > 0:
            self.health -= 1

        if self.health == 0:
            self.kill()
        
        power_up_list = pygame.sprite.spritecollide(self, power_ups, True)

        for p in power_up_list:
            p.apply(self)

ticks = 0
power_up_timer = 0

def timers():
    global ticks, power_up_timer
    ticks += 1
    if power_up_timer >= 0:
        power_up_timer -=1

#######################################################

class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.speed = 8

    def update(self):
        self.rect.y -= self.speed

        if self.rect.top < 0: 
            self.speed += 1
            self.speed *= -1

        elif self.rect.bottom > HEIGHT:
            self.speed -= 1
            self.speed *= -1
  
        if self.speed >= 20:
            self.speed = 20

####################################################
            
class Shield_shot(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.speed = 3
        self.shield_health = 3 
        
    def update(self):
        self.rect.y -= self.speed

        hit_list = pygame.sprite.spritecollide(self, projectiles, True)

        for hit in hit_list:
            self.shield_health -= 1

        if self.shield_health == 0:
            self.kill()
        
        
#####################################################
            
class ShieldPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 3

    def apply(self, ship):
        ship.shield_ammo += 3
        
    def update(self):
        self.rect.y += self.speed


        if self.rect.y > 1000:
            self.rect.y = random.randrange(-1700, -200)
            self.rect.x = random.randrange(0, 1900)
            self.speed += 1
                        
#####################################################

class HealthPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        
    def apply(self, ship):
        ship.health += 1
        
    def update(self):

        self.rect.y += self.speed

        if self.rect.y > 1000:
            self.rect.y = random.randrange(-1700, -200)
            self.rect.x = random.randrange(0, 1900)
            self.speed += 1
        
        
#####################################################
        
class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.speed = 7

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()
            
#####################################################
            
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 3

    def drop_bomb(self):
        print("bwamperino")
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.top = self.rect.bottom + 1 
        projectiles.add(bomb)
        
    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True)

        for hit in hit_list:
            self.health -= 1

            if self.health == 0:
                self.kill()
                fleet.speed += 1
                ship.score += (1 * ship.value)
                ship.kills += 1

#########################################################
class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 5
        self.drop = 10
        self.moving_right = True
        self.bomb_speed = 20 
        self.bomb_rate = 10
        
    def move(self):
        hits_edge = False
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right > WIDTH:
                    hits_edge = True

            else:
                m.rect.x -= self.speed

                if m.rect.left < 0 :
                    hits_edge = True
                    
        if hits_edge:
            self.reverse()
            self.move_down()

        for m in mobs:
            if m.rect.bottom > 1000:
                ship.health = 0
            
    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop
            
    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mobs_list = mobs.sprites()

        if len(mobs_list) > 0 and rand == 0:
            bomber = random.choice(mobs_list)
            bomber.drop_bomb()

    def is_defeated(self):
        return len(mobs) == 0
    
    def update(self):
        self.move()
        self.choose_bomber()

###########################################################################

# Game helper functions
def show_title_screen():
    title_text = FONT_XL.render("Space War!", 1, WHITE)
    text_width = title_text.get_width()

    x = (WIDTH/2) - (text_width/2)
    y = HEIGHT/2 - 40

    screen.blit(title_text, [x, y])

def show_end_screen(): 
    death_text = FONT_XL.render("pity, you perished", 1, WHITE)
    text_width = death_text.get_width()
    
    x = (WIDTH/2) - (text_width / 2)
    y = HEIGHT/2 - 40

    screen.blit(death_text, [x, y])

    ###
    score_text = FONT_XL.render(str(ship.score), 1, WHITE)

    score_text_width = score_text.get_width()
    
    x1 = (WIDTH/2) - (score_text_width / 2)
    y1 = HEIGHT/2 + 140


    screen.blit(score_text, [x1, y1])
                
def show_stats():
    shield_health_text = FONT_XL.render(str(ship.health), 1, WHITE)

    x = 3
    y = -10

    screen.blit(shield_health_text, [x,y])

    shield_ammo_text = FONT_XL.render(str(ship.shield_ammo), 1, WHITE)

    x1 = 0
    y1 = 50

    screen.blit(shield_ammo_text, [x1,y1])

def stars_update():
        for s in stars:
            s[1] += 3
            if s[1] > 1000:
                s[1] = -1000
        for s1 in stars1:
            s1[1] += 3
            if s1[1] > 1000:
                s1[1] = -1000

def draw_background1():
    screen.blit(earth_img, [800, 300])
    screen.blit(planet_img, [150, 200])
    screen.blit(planet2_img, [600, 700])
    for s in stars:
        pygame.draw.ellipse(screen, WHITE, s)
    for s1 in stars1:
        pygame.draw.ellipse(screen, WHITE, s1)

def fleet_set():
    global mobs, fleet, power_ups

    ' power ups'
    shield_power_up1 = ShieldPowerUp(100, 0, shieldshot_drop_img)

    health_power_up1 = HealthPowerUp(1600, 0, HP_img)
    


    mob1 = Mob(100, 100, enemy_img)
    mob2 = Mob(250, 100, enemy_img)
    mob3 = Mob(400, 100, enemy_img)
    mob4 = Mob(550, 100, enemy_img)
    mob5 = Mob(700, 100, enemy_img)
    mob6 = Mob(850, 100, enemy_img)
    mob7 = Mob(1000, 100, enemy_img)
    mob8 = Mob(1150, 100, enemy_img)
    mob9 = Mob(1300, 100, enemy_img)
    mob10 = Mob(1450, 100, enemy_img)
    que1 = Mob(150, 250, enemy_img)
    que2 = Mob(300, 250, enemy_img)
    que3 = Mob(450, 250, enemy_img)
    que4 = Mob(600, 250, enemy_img)
    que5 = Mob(750, 250, enemy_img)
    que6 = Mob(900, 250, enemy_img)
    que7 = Mob(1050, 250, enemy_img)
    que8 = Mob(1200, 250, enemy_img)
    que9 = Mob(1350, 250, enemy_img)
    que10 = Mob(1500, 250, enemy_img)

    mobs = pygame.sprite.Group()
    if ship.wave % 3 == 0:
        power_ups.add(shield_power_up1, health_power_up1)
        
    if ship.wave == 0:
        mobs.add(mob1, mob3, mob5, mob7, mob9)
    elif ship.wave == 1:
        mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10)
    elif ship.wave == 2:
        mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10,
                 que1, que3, que5, que7, que9)
    else:
        mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8, mob9, mob10,
              que1, que2, que3, que4, que5, que6, que7, que8, que9, que10)

    fleet = Fleet(mobs)

def setup():
    global stage, done
    global player, ship, lasers, mobs, fleet, bombs, power_ups, shields, projectiles
    
    ''' Make game objects '''
    ship = Ship(364, 936, ship_img)

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    ship.health = 3

    
    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    shields = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()

    projectiles.add(lasers, bombs)

    mobs = pygame.sprite.Group()
    
    power_ups = pygame.sprite.Group()
    'fleet'
    fleet = Fleet(mobs)

    ''' set stage '''
    stage = START
    done = False
    
# Game loop
setup()
fleet_set()
while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
                if event.key == pygame.K_c:
                    ship.shoot_shield()
            elif stage == END:
                if event.key == pygame.K_SPACE:
                    setup()

        ''' more controller crap yay '''
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == xbox360_controller.BACK:
                done = True
            if stage == START:
                if event.button == xbox360_controller.START:
                    stage = PLAYING
                    
            if stage == PLAYING:
                if event.button == xbox360_controller.A:
                    ship.shoot()
                if event.button == xbox360_controller.X:
                    ship.shoot_shield()

                if event.button == xbox360_controller.Y:
                    stage = PAUSED

            elif stage == PAUSED:
                if event.button == xbox360_controller.Y:
                    stage = PLAYING
                    
            elif stage == END:
                if event.button == xbox360_controller.START:
                    setup()


    pressed = pygame.key.get_pressed()
    
    left_x, left_y = controller.get_left_stick()
    
    # Game logic (Check for collisions, update points, etc.)
    screen.fill(BLACK)
    
    if stage == START:
        show_title_screen()

    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        ship.rect.x += int(left_x * ship.speed * 1.6)
        ship.rect.y += int(left_y * ship.speed)
        
        timers()
        player.update()
        projectiles.update()
        fleet.update()
        mobs.update()
        power_ups.update()
        shields.update()
        if fleet.is_defeated():
            ship.wave += 1
            ship.value += 1
            fleet_set()
        if ship.health == 0:
            stage = END


     
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    if stage == PAUSED:
        pass
    
    if stage == PLAYING or stage == PAUSED:
        stars_update()
        draw_background1()
        projectiles.draw(screen)
        player.draw(screen)
        mobs.draw(screen)
        power_ups.draw(screen)
        shields.draw(screen)
        show_stats()

        
    if stage == END:
        show_end_screen()
            
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
