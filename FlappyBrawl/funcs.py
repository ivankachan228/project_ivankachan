import pygame
import globals as gl

screen = pygame.display.set_mode((gl.screen_width, gl.screen_height))
pygame.display.set_caption('Flappy Brawl')

def draw_text(text, font, text_col, x, y):
    """
    Draw a text
    :param text: needed text
    :param font: font for text
    :param text_col: color (rgb)
    :param x: koord x
    :param y: koord y
    :return: NONE
    """
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game(pipe_group, flappy):
    """
    Reset game
    :param pipe_group: pipe object
    :param flappy: spike object
    :return: score of spike
    """
    pipe_group.empty()
    flappy.rect.x = gl.rect
    flappy.rect.y = int(gl.screen_height / 2)
    gl.score = 0
    pygame.mixer.music.load('files/win_screen_loop_4x_01.mp3')
    pygame.mixer.music.play(-1)
    return gl.score
