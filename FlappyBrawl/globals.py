import pygame
pygame.init()
clock = pygame.time.Clock()
rect = 100
nolshest = 0.6
map_bottom = 8
sizik = 420
tube_start = -90
white = (255, 255, 255)
fps = 60
# Определяем шрифт
font = pygame.font.SysFont('arial', 70)
screen_width = 864
screen_height = 500
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
game_over_music = False