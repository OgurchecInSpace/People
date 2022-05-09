# Основная часть программы
import pygame
from classes_of_peoples import Unit

# from tower import Tower

WIDTH = 1800
HEIGHT = 900
FPS = 30
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

all_sprites = pygame.sprite.Group()

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Peoples')
clock = pygame.time.Clock()

jim = Unit(num=0, tower=None, x=600, y=600)
all_sprites.add(jim)
# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    jim.go(to_x=800, to_y=200, speed=jim.speed)

    # Обновление
    all_sprites.update()
    # Рендеринг
    screen.fill(BLUE)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
