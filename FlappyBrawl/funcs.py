import pygame
import globals as gl
# import game
import random


# pygame.init()
#
# clock = pygame.time.Clock()
#
#
screen = pygame.display.set_mode((gl.screen_width, gl.screen_height))
pygame.display.set_caption('Flappy Brawl')
# # Определяем цвета
# white = (255, 255, 255)
#
# # Определяем игровые переменные
#
#
# # Загружаем изображения
# bg = pygame.image.load('files/bg.jpg')
# ground_img = pygame.image.load('files/ground.jpg')
# button_img = pygame.image.load('files/restart.png')

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game(pipe_group, flappy):
    pipe_group.empty()
    flappy.rect.x = gl.rect
    flappy.rect.y = int(gl.screen_height / 2)
    gl.score = 0
    pygame.mixer.music.load('files/win_screen_loop_4x_01.mp3')
    pygame.mixer.music.play(-1)
    return gl.score
