import pygame
import random
import globals as gl
import funcs as f
import button as but
import spike_class as spikee
import pipe_class as pipee

pygame.init()

clock = pygame.time.Clock()


screen = pygame.display.set_mode((gl.screen_width, gl.screen_height))
pygame.display.set_caption('Flappy Brawl')
# Определяем цвета


# Загружаем изображения
bg = pygame.image.load('files/bg.jpg')
ground_img = pygame.image.load('files/ground.jpg')
button_img = pygame.image.load('files/restart.png')

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()


flappy = spikee.Spike(100, int(gl.screen_height / 2))

bird_group.add(flappy)

# создаем экземпляр кнопки перезапуска
button = but.Button(gl.screen_width // 2 - 50, gl.screen_height // 2 - 100, button_img)
pygame.mixer.music.load('files/win_screen_loop_4x_01.mp3')
pygame.mixer.music.play(-1)

run = True
while run:
    clock.tick(gl.fps)

    # рисуем фон
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    # рисуем землю
    screen.blit(ground_img, (gl.ground_scroll, 420))

    # проверяем счет
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and gl.pass_pipe == False:
            gl.pass_pipe = True
        if gl.pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                gl.score += 1
                gl.pass_pipe = False

    f.draw_text(str(gl.score), gl.font, gl.white, int(gl.screen_width / 2), 20)

    # проверяем столкновения
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        gl.game_over = True

    # проверяем, не ударил ли птица о землю
    if flappy.rect.bottom >= 420:
        gl.game_over = True
        gl.flying = False

    if gl.game_over == False and gl.flying == True:
        # создаем новые трубы
        time_now = pygame.time.get_ticks()
        if time_now - gl.last_pipe > gl.pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = pipee.GasPipe(gl.screen_width, int(gl.screen_height / 2) + pipe_height, -1)
            top_pipe = pipee.GasPipe(gl.screen_width, int(gl.screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            gl.last_pipe = time_now

        # рисуем и прокручиваем землю
        gl.ground_scroll -= gl.scroll_speed
        if abs(gl.ground_scroll) > 35:
            gl.ground_scroll = 0

        pipe_group.update()

    if gl.game_over and not gl.game_over_music:
        pygame.mixer.music.stop()  # Останавливаем фоновую музыку
        pygame.mixer.music.load('files/brawl_goal_02.mp3')  # Загружаем музыку проигрыша
        pygame.mixer.music.play(1)  # Воспроизводим музыку проигрыша
        gl.game_over_music = True  # Устанавливаем флаг, чтобы музыка проигрыша воспроизводилась только один раз

    # проверяем конец игры и сбрасываем
    if gl.game_over == True:
        if button.draw() == True:
            gl.game_over = False
            gl.game_over_music = False  # Сбрасываем флаг, чтобы музыка проигрыша воспроизводилась в следующий раз
            gl.score = f.reset_game(pipe_group, flappy)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and gl.flying == False and gl.game_over == False:
            gl.flying = True

    pygame.display.update()

pygame.quit()
