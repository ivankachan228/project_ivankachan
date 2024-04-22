import pygame
import globals as gl
screen = pygame.display.set_mode((gl.screen_width, gl.screen_height))
class Button():
    """Класс, представляющий кнопку рестарта"""

    def __init__(self, x, y, image):
        """
            :param x:  положение по оси х
            :param y: положение по оси у
            :param image: фото кнопки рестарта
        """
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        """

        :return: true если нажали на рестарт левой кнопкой мышки
        """

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

