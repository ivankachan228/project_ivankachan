import pygame
import globals as gl
class Spike(pygame.sprite.Sprite):
    """Класс, представляющий спайка из Бравл Старс"""
    def __init__(self, x, y):
        """Инициализация спайка.

               Args:
                   x (int): Положение фигурки по оси X.
                   y (int): Положение фигурки по оси Y.,
            Инициализация необходимых пераметров:
                vel (int): текущая скорость спайка.
                index (int): индекс текущего изображения спайка в анимации.
                rect : прямоугольная область, ограничивающая спрайт спайка.
                clicked (bool): флаг, указывающий на состояние нажатия левой кнопки мыши.
                downclicked (bool): флаг, указывающий на состояние нажатия правой кнопки мыши.
                music (bool): флаг, указывающий на воспроизведение музыки пока спайк летит.
        """
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'files/gif/{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
        self.downclicked = False
        self.mucic = False

    def update(self):
        """Метод обновления положения и состояния спайка.
            Обновляет положение спайка в зависимости от текущих условий игры.
            Если игра активна, применяется гравитация, обрабатывается ввод от игрока,
                проигрывается анимация (гифка спайка, движение земли), играет музыка
            Если игра завершена, спайк возвращается в начальное положение.
        """

        if gl.flying == True:
            # гравитация
            self.vel += gl.nolshest
            if self.vel > gl.map_bottom:
                self.vel = gl.map_bottom
            if self.rect.bottom < gl.sizik:
                self.rect.y += int(self.vel)

        if gl.game_over == False:
            # прыжок
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            if pygame.mouse.get_pressed()[2] == 1 and self.downclicked == False:
                self.downclicked = True
                self.vel = +15
            if pygame.mouse.get_pressed()[2] == 0:
                self.downclicked = False

            # анимация
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # вращение птицы
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], gl.tube_start)

