import pygame
import globals as gl
screen = pygame.display.set_mode((gl.screen_width, gl.screen_height))
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        # получаем позицию мыши
        pos = pygame.mouse.get_pos()

        # проверяем, наведена ли мышь на кнопку
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # рисуем кнопку
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

