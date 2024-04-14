import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Brawl')

# Определяем шрифт
font = pygame.font.SysFont('arial', 70)

# Определяем цвета
white = (255, 255, 255)

# Определяем игровые переменные
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

# Загружаем изображения
bg = pygame.image.load('bg.jpg')
ground_img = pygame.image.load('ground.jpg')
button_img = pygame.image.load('restart.png')


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0
    pygame.mixer.music.load('win_screen_loop_4x_01.mp3')
    pygame.mixer.music.play(-1)
    return score


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'gif/{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
        self.downclicked = False
        self.mucic = False

    def update(self):

        if flying == True:
            # гравитация
            self.vel += 0.6
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 420:
                self.rect.y += int(self.vel)

        if game_over == False:
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
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class GasPipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('gas.png')
        self.rect = self.image.get_rect()
        # позиция 1 - сверху, -1 - снизу
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


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


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()


flappy = Spike(100, int(screen_height / 2))

bird_group.add(flappy)

# создаем экземпляр кнопки перезапуска
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)
pygame.mixer.music.load('win_screen_loop_4x_01.mp3')
pygame.mixer.music.play(-1)

run = True
while run:
    clock.tick(fps)

    # рисуем фон
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    # рисуем землю
    screen.blit(ground_img, (ground_scroll, 420))

    # проверяем счет
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False

    draw_text(str(score), font, white, int(screen_width / 2), 20)

    # проверяем столкновения
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # проверяем, не ударил ли птица о землю
    if flappy.rect.bottom >= 420:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        # создаем новые трубы
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = GasPipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = GasPipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # рисуем и прокручиваем землю
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()

    if game_over and not game_over_music:
        pygame.mixer.music.stop()  # Останавливаем фоновую музыку
        pygame.mixer.music.load('brawl_goal_02.mp3')  # Загружаем музыку проигрыша
        pygame.mixer.music.play(1)  # Воспроизводим музыку проигрыша
        game_over_music = True  # Устанавливаем флаг, чтобы музыка проигрыша воспроизводилась только один раз

    # проверяем конец игры и сбрасываем
    if game_over == True:
        if button.draw() == True:
            game_over = False
            game_over_music = False  # Сбрасываем флаг, чтобы музыка проигрыша воспроизводилась в следующий раз
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()