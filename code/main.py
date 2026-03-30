import pygame
from os.path import join
from random import randint
# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  #申请了一块空间， 二乘二的矩阵
pygame.display.set_caption('Space shooter')
running = True

# surface
surf = pygame.Surface((100, 200)) #也是个内存
surf.fill('orange')
x = 100

# imporing an image
player_surf = pygame.image.load(join('../', 'images', 'player.png')).convert_alpha() #print(path) 防止mac和win的路径不同 #conver不用实时翻译
star_surf = pygame.image.load(join('..', 'images', 'star.png')).convert_alpha()


while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw the game
    display_surface.fill('darkgray')
    x += 0.1
    display_surface.blit(player_surf, (x, 150)) #盖章
    for i in range(0, 20):
        display_surface.blit(star_surf, (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))
    pygame.display.update()

pygame.quit()
