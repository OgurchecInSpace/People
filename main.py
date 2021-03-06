# Основная часть программы
import asyncio
import pygame
from constants import *
from classes_of_people import *
import time
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

green_tower = Tower(GREEN, 100, 100)
red_tower = Tower(RED, WIDTH - 500, HEIGHT - 200)
towers = pygame.sprite.Group()
towers.add(green_tower)
towers.add(red_tower)

ores = pygame.sprite.Group()  # Руды
ore1 = Ore(x=700, y=200, output_energy=gold_output_energy)
ores.add(ore1)


async def update():
    for next_tower in towers.copy():
        new_task = asyncio.create_task(next_tower.update(towers, ores))
        await new_task


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

    asyncio.run(update())

    # # Обновление
    # for tower in towers.copy():
    #     tower.update(towers, ores)

    # Рендеринг
    screen.fill(BLUE)
    ores.draw(screen)
    towers.draw(screen)
    for tower in towers.copy():
        tower.miners.draw(screen)
        tower.warriors.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()
# Придуманным миром удобней управлять...
