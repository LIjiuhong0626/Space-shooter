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

        #transform test
        # self.image = pygame.transform.rotate(self.image, 90)
        # self.image = pygame.transform.grayscale(self.image)
        
        #mask
        # self.mask = pygame.mask.from_surface(self.image)#把照片生成了一个矩阵
        # mask_surf = mask.to_surface()#矩阵转换为图片
        # mask_surf.set_colorkey((0, 0 ,0)) #指定某种特定颜色为透明 在 blit（贴图）的时候直接跳过， 不要画出来
        # self.image = mask_surf

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks() #记录从init的时间
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt): # 只有这个在一直运行 每一帧在干嘛
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
            laser_sound.play()

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
        # self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_image = surf
        self.image = self.original_image # 只是一个像素阵列，它没有坐标！

        self.rect = self.image.get_frect(center = pos) #根据这个长宽，给我造一个虚构的、隐形的矩形框 在造这个框的时候，别把它丢在默认的 (0,0) 位置

        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000

        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1) #可以有小数
        self.speed = randint(400, 500)

        self.angle = 0
        self.rotate_speed = randint(20, 50)
        # self.mask = pygame.mask.from_surface(self.image)
    
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt # 1. 物理移动

        self.angle += self.rotate_speed * dt # 2. 角度累加（绝对值）
        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 1)# 3. 旋转原图（PS 类比：每次都从干净的草稿开始旋转，防止画质烂掉）
        self.rect = self.image.get_frect(center = self.rect.center) #回到原位， 旋转之后图片会变大， 但是位置与图片无关 ，这里是说量一下图片， 给我一个矩形， 把矩形放在原来的位置

        current = pygame.time.get_ticks()
        if current - self.start_time >= self.lifetime:
            self.kill()
        
class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frames_index = 0
        self.image = frames[self.frames_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frames_index += 30 * dt
        if self.frames_index <= len(self.frames):
            self.image = self.frames[int(self.frames_index)]
        else:
            self.kill()

def collisions():
    global running
    collision_sprite = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask) #
    if collision_sprite:#返回的是列表
        damage_sound.play()
        running = False

    for laser in laser_sprites:
        collision_sprite = pygame.sprite.spritecollide(laser, meteor_sprites, True)#返回的是列表
        if collision_sprite:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True,(240, 240, 240)) #此时就是把文字变成图片
    text_rect = text_surf.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    pygame.draw.rect(display_surface, (240, 240, 240), text_rect.inflate(20, 16).move(0, -7), 5, 10)
    display_surface.blit(text_surf, text_rect) #Bit Boundary Block Transfer

# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  #申请了一块空间， 二乘二的矩阵
pygame.display.set_caption('Space shooter')
running = True
clock = pygame.time.Clock()


#import
star_surf = pygame.image.load(join('..', 'images', 'star.png')).convert_alpha()  #只需要一次
meteor_surf = pygame.image.load(join('..', 'images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('..', 'images', 'laser.png')).convert_alpha()
font = pygame.font.Font(join('..', 'images', 'Oxanium-Bold.ttf'), 40) #你只是握着一支笔，选好了粗细和样式，但还没下笔。
explosion_frames = [pygame.image.load(join('..', 'images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound(join('..', 'audio', 'laser.wav'))
laser_sound.set_volume(0.3)
explosion_sound = pygame.mixer.Sound(join('..', 'audio', 'explosion.wav'))
explosion_sound.set_volume(0.3)
damage_sound = pygame.mixer.Sound(join('..', 'audio', 'damage.ogg'))
damage_sound.set_volume(0.3)
game_music = pygame.mixer.Sound(join('..', 'audio', 'game_music.wav'))
game_music.set_volume(0.3)
game_music.play(loops= -1)


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
    all_sprites.draw(display_surface) #正式绘图 默认会找这两个固定命名 .image .rect 我不用在update中写blit
    

    pygame.display.update()

pygame.quit()
