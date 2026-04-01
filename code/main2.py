import pygame
from os.path import join
from random import randint, uniform

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load(join('..', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2((0, 0))
        self.speed = 500

        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 200

    def laser_timer(self):
        if self.can_shoot == False and pygame.time.get_ticks() - self.laser_shoot_time >= self.cooldown_duration:
            self.can_shoot = True
            
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = star_surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0,  WINDOW_HEIGHT)))

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = meteor_surf
        self.rect = self.image.get_frect(midbottom = (randint(0, WINDOW_WIDTH), -50))
        self.direction = pygame.math.Vector2(uniform(-1, 1), uniform(0, 1))
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.speed = 300


    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
        
class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = laser_surf
        self.rect = self.image.get_frect(midbottom = pos)
        self.speed = 500
    
    def update(self, dt):
        self.rect.centery -= self.speed * dt
        if self.rect.centery <= 0:
            self.kill()

class AnimatedExplosion(pygame.sprite.Sprite): #一个对象会有多个图片
    def __init__(self, pos, group):
        super().__init__(group)
        self.fames_index = 0
        self.image = explosion_frames[0]
        self.rect = self.image.get_frect(center = pos)
    
    def update(self, dt):
        self.fames_index += (100 * dt) #一定是加法， 保证连续， 但是一帧中会包含许多个相同的一副画面
        if self.fames_index < len(explosion_frames):
            self.image = explosion_frames[int(self.fames_index)]
        else:
            self.kill()


def collisions():
    global running
    collision_sprite = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask) #
    if collision_sprite:#返回的是列表
        running = False

    for laser in laser_sprites:
        collision_sprite = pygame.sprite.spritecollide(laser, meteor_sprites, True)#返回的是列表
        if collision_sprite:
            laser.kill()
            AnimatedExplosion(laser.rect.midtop, all_sprites)


# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space shooter')
running = True
clock = pygame.time.Clock()

#import
star_surf = pygame.image.load(join('..', 'images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('..', 'images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('..', 'images', 'laser.png')).convert_alpha()
explosion_frames = [pygame.image.load(join('..', 'images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

#sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites =  pygame.sprite.Group()
for i in range(0, 21):
    Star(all_sprites)
player = Player(all_sprites) 

#custom event - > meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 250) #定个闹钟，每 500 毫秒发送一次这个信号。

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor((all_sprites, meteor_sprites))

    #update
    all_sprites.update(dt)

    collisions()

    #draw the game
    display_surface.fill('#3a2e3f')
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()