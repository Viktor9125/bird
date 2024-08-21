import pygame as pg
import sys
import random

# fps
clock = pg.time.Clock()
FPS = 60

pg.init()

# Создание экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Flappy Bird')

# Картинки
back_ground = pg.image.load(f'Assets/Background/Background{random.randint(1, 6)}.png')
back_ground = pg.transform.scale(back_ground, (SCREEN_WIDTH, SCREEN_HEIGHT))
pipe_image = pg.image.load('Assets/Tiles/Style 1/PipeStyle1.png')
bird_image = pg.image.load(f'Assets/Player/StyleBird1/Bird1-{random.randint(1, 7)}.png')

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Шрифты
font = pg.font.Font(None, 50)
font2 = pg.font.Font(None, 10)


# Класс птицы
class Bird(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.bird_speed = 5
        self.num_images = 4
        self.bird_images = []
        self.index = 0
        self.timer = pg.time.get_ticks()
        self.bird_image = bird_image
        self.flying = False
        self.vel_y = 0
        self.active = True

        for i in range(self.num_images):
            x = i * 16
            y = 0
            rect = pg.Rect(x, y, 16, 16)
            image = self.bird_image.subsurface(rect)
            image = pg.transform.scale(image, (50, 50))
            self.bird_images.append(image)

        self.image = self.bird_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self):
        if self.active:
            if self.rect.y > SCREEN_HEIGHT or self.rect.top < 0:
                self.active = False
                return

            if game_started:
                self.bird_speed += gravity
                self.y += self.bird_speed
                # if self.vel_y > -11:
                #     self.vel_y -= gravity
                self.rect.topleft = (self.x, self.y)

            if pg.time.get_ticks() - self.timer > 150:
                self.index += 1
                if self.index >= len(self.bird_images):
                    self.index = 0
                self.image = self.bird_images[self.index]
                # self.image = pg.transform.rotate(self.image, self.vel_y)
                self.timer = pg.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def reset(self):
        self.active = True

    def fly(self):
        if not self.flying and self.active:
            self.bird_speed = -jump_force
            self.flying = True
            # self.vel_y = 11


# Класс трубы
class Pipe(pg.sprite.Sprite):
    def __init__(self, x, y, pos):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('Assets/Tiles/Style 1/pipe.png')
        # self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()

        if pos == 1:
            self.image = pg.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - pipe_gap // 2)
        else:
            self.rect.topleft = (x, y + pipe_gap // 2)

    def update(self):
        self.rect.x -= pipe_speed
        if self.rect.right < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Класс кнопки
class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.is_clicked = False

    def draw(self, screen):
        action = False

        pos = pg.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and not self.is_clicked:
                action = True
                self.is_clicked = True

        if pg.mouse.get_pressed()[0] == 0:
            self.is_clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


# Переменные для труб
pipe_width = 50
pipe_height = 300
pipe_gap = 150
pipe_x = SCREEN_WIDTH
pipe_speed = 5

pipe_group = pg.sprite.Group()
pipe_interval = 1500
pipe_timer = pg.time.get_ticks()
pass_pipe = False

# Переменные
gravity = 1
jump_force = 15
game_over = False
game_started = False
speed_time = 1500
speed_timer = pg.time.get_ticks()
active = False
keyboard_mode = True

# Птица
bird = Bird()

# Счет
score = 0

# Кнопка заново
restart_image = pg.image.load('Assets/restart.png')
restart = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, restart_image, 1)


# Функция для отрисовки текста
def draw_text(text, font, color, x, y):
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)


# Функция возращения
def reset():
    pipe_group.empty()
    bird = Bird()
    score = 0
    pipe_speed = 5
    return score, bird, pipe_speed


# Цикл игры
run = True
while run:
    # События
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                keyboard_mode = not keyboard_mode
            if event.key == pg.K_SPACE and keyboard_mode:
                if not game_started:
                    game_started = True
                bird.fly()
        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE and keyboard_mode:
                bird.flying = False

    if not keyboard_mode:
        mouse_keys = pg.mouse.get_pressed()

        if mouse_keys[0] == 1 and not active:
            if not game_started:
                game_started = True
            active = True
            bird.fly()
        if mouse_keys[0] == 0:
            active = False
            bird.flying = False

    # Отрисовка
    screen.blit(back_ground, (0, 0))

    pipe_group.draw(screen)

    bird.draw(screen)

    draw_text(str(score), font, 'white', SCREEN_WIDTH // 2, 20)
    if not game_started:
        draw_text('Нажмите E чтобы сменить режим.', font, 'grey50', SCREEN_WIDTH // 2, 300)

    # Проверка коснулась птица трубы
    if pg.sprite.spritecollide(bird, pipe_group, False, pg.sprite.collide_mask):
        game_over = True

    # Ускорение игры
    if game_started and not game_over:
        if pg.time.get_ticks() - speed_timer > speed_time:
            pipe_speed += 0.1
            speed_timer = pg.time.get_ticks()

    if not game_over:

        # Обновление
        pipe_group.update()

        if bird.active:
            bird.update()
        else:
            game_over = True

        # Счет
        if len(pipe_group) > 0:
            if bird.rect.left > pipe_group.sprites()[0].rect.left and bird.rect.right < pipe_group.sprites()[
                0].rect.right and not pass_pipe:
                pass_pipe = True

            if pass_pipe:
                if bird.rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False

        # Создание труб
        if game_started and pg.time.get_ticks() - pipe_timer > pipe_interval:
            pipe_height = random.randint(-100, 100)
            top_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + pipe_height, 1)
            btm_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT // 2 + pipe_height, -1)
            pipe_group.add(top_pipe)
            pipe_group.add(btm_pipe)
            pipe_timer = pg.time.get_ticks()
    # Начать игру заново
    if game_over:
        if restart.draw(screen):
            score, bird, pipe_speed = reset()
            game_over = False
            game_started = False

    # Добавление fps
    clock.tick(FPS)
    # Отрисовка
    pg.display.flip()

pg.quit()
sys.exit()
