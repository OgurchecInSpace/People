# Основная часть программы
import pygame
from constants import *
from classes_of_peoples import *
from builds_classes import *

WIDTH = 1800
HEIGHT = 900

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

Green_tower = Tower(GREEN, 100, 100)
towers = pygame.sprite.Group()
towers.add(Green_tower)

ores = pygame.sprite.Group()  # Руды
ore1 = Ore(x=700, y=200, output_energy=gold_output_energy)
ores.add(ore1)

# Цикл симуляции
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверяем закрытие окна
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    for tower in towers:
        tower.update()
        for miner in tower.miners:
            miner.update(ores)

    # Рендеринг
    screen.fill(BLUE)
    ores.draw(screen)
    towers.draw(screen)
    for tower in towers:
        tower.miners.draw(screen)
        tower.warriors.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
