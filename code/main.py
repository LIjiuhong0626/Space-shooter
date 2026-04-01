import pygame
from os.path import join

from random import randint, uniform
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('../', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 ))
        self.direction = pygame.Vector2()
        self.speed = 300

        #cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks() #记录从init的时间
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt): # 只有这个在一直运行
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt #速度是一致的， 我们要的就是帧率不同， 但是每秒钟移动的位移是一致的 , 而这个循环是每秒钟循环的次数， 循环次数乘dt是1
                                        #保障帧率不同但是每秒移动位移相同

        recent_keys = pygame.key.get_just_pressed()#如果不是这个， 那么在按下的同时会一直进行
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, star_surf):
        super().__init__(groups)
        self.image = star_surf
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1) #可以有小数
        self.speed = randint(400, 500)
    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        current = pygame.time.get_ticks()
        if current - self.start_time >= self.lifetime:
            self.kill()

def collisions():
    global running
    collision_sprite = pygame.sprite.spritecollide(player, meteor_sprites, True)
    if collision_sprite:#返回的是列表
        running = False

    for laser in laser_sprites:
        collision_sprite = pygame.sprite.spritecollide(laser, meteor_sprites, True)#返回的是列表
        if collision_sprite:
            laser.kill()

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True,(240, 240, 240)) #此时就是把文字变成图片
    text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    pygame.draw.rect(display_surface, (240, 240, 240), text_rect.inflate(20, 16).move(0, -7), 5, 10)
    display_surface.blit(text_surf, text_rect)

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  #申请了一块空间， 二乘二的矩阵
pygame.display.set_caption('Space shooter')
running = True
clock = pygame.time.Clock()

#inport
star_surf = pygame.image.load(join('..', 'images', 'star.png')).convert_alpha()  #只需要一次
meteor_surf = pygame.image.load(join('..', 'images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('..', 'images', 'laser.png')).convert_alpha()
font = pygame.font.Font(join('..', 'images', 'Oxanium-Bold.ttf'), 40) #你只是握着一支笔，选好了粗细和样式，但还没下笔。

#sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)


#custom event - > meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500) #定个闹钟，每 500 毫秒发送一次这个信号。

while running:
    dt = clock.tick(60) / 1000 #这一帧耗时了多少秒 默认单位是千毫秒
    #print(clock.get_fps())
    # event loop
    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            running = False
        if event.type == meteor_event:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))

    #update
    all_sprites.update(dt)#逻辑计算

    #collion test
    collisions()

    #draw the game
    display_surface.fill('#3a2e3f')
    display_score()
    all_sprites.draw(display_surface) #正式绘图
    

    pygame.display.update()

pygame.quit()
