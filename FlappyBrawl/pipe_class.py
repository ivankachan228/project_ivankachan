import pygame
import globals as gl
class GasPipe(pygame.sprite.Sprite):
    """Класс, представляющий газовую трубу."""
    def __init__(self, x, y, position):
        """Инициализация трубы.

                Args:
                    x (int): Положение трубы по оси X.
                    y (int): Положение трубы по оси Y.
                    position (int): Позиция трубы (1 - сверху, -1 - снизу).
                """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('files/gas.png')
        self.rect = self.image.get_rect()
        # позиция 1 - сверху, -1 - снизу
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(gl.pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(gl.pipe_gap / 2)]

    def update(self):
        """Обновляет состояние трубы. Если мы уже не видим трубу, то удаляем объект"""
        self.rect.x -= gl.scroll_speed
        if self.rect.right < 0:
            self.kill()


