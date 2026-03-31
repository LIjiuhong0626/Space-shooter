import pygame
from os.path import join
from random import randint
# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  #申请了一块空间， 二乘二的矩阵
pygame.display.set_caption('Space shooter')
running = True
clock = pygame.time.Clock()

# surface
surf = pygame.Surface((100, 200)) #也是个内存
surf.fill('orange')
x = 100

# imporing an image
player_surf = pygame.image.load(join('../', 'images', 'player.png')).convert_alpha() #print(path) 防止mac和win的路径不同 #conver不用实时翻译
player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 )) #只是返回一个位置信息， 但是是自动计算了的
player_direction = pygame.math.Vector2(2, -1)
player_speed = 100

star_surf = pygame.image.load(join('..', 'images', 'star.png')).convert_alpha() 
star_positions = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)]#

meteor_surf = pygame.image.load(join('..', 'images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 ))

laser_surf = pygame.image.load(join('..', 'images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_rect(bottomleft = (20, WINDOW_HEIGHT - 20))

while running:
    dt = clock.tick(60) / 1000 #这一帧耗时了多少秒 默认单位是千毫秒
    #print(clock.get_fps())
    # event loop
    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            running = False
        # if event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos

    #input
    #print(pygame.mouse.get_pressed()[0])
    #print(pygame.mouse.get_rel())

    key = pygame.key.get_pressed()
    print(key[pygame.K_5])

    #draw the game
    display_surface.fill('darkgray')
   
    for pos in star_positions:
        display_surface.blit(star_surf,pos)

    display_surface.blit(laser_surf, laser_rect)
    display_surface.blit(meteor_surf, meteor_rect)

    #player movement
    
    player_rect.center += player_direction * (player_speed * dt) #速度是一致的， 我们要的就是帧率不同， 但是每秒钟移动的位移是一致的 , 而这个循环是每秒钟循环的次数， 循环次数乘dt是1
    if player_rect.right >= WINDOW_WIDTH or player_rect.left <= 0:
        player_direction.x *= -1

    if player_rect.bottom >= WINDOW_HEIGHT or player_rect.top <= 0:
        player_direction.y *= -1

    display_surface.blit(player_surf, player_rect) #盖章

    pygame.display.update()

pygame.quit()
