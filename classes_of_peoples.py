# Файл с классами юнитов
import pygame
# import math


class Unit(pygame.sprite.Sprite):  # Класс юнита
    def __init__(self, num, tower, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 30))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.BLACK = (0, 0, 0)
        self.num = num
        self.tower = tower
        self.speed = 8

    def go(self, to_x, to_y, speed):
        # Первый способ передвижения (и самый лучший!) на доработке, но и так сойдёёёт
        leg_x = abs(self.rect.x - to_x)  # один катет
        leg_y = abs(self.rect.y - to_y)  # другой катет
        hyp = (leg_x ** 2 + leg_y ** 2) ** 0.5  # Гипотенуза прямоугольного треугольника, по который мы должны двигаться
        if hyp != 0:
            speed_x = round(speed * (leg_x / hyp))
            speed_y = round(speed * (leg_y / hyp))
        else:
            return None

        # speed_x = math.cos(math.atan(leg_x / leg_y))  # Зачем-то ещё такой способ, который не работает адекватно
        # speed_y = math.sin(math.atan(leg_y / leg_x))
        if to_x > self.rect.x:
            self.rect.x += speed_x
        if to_x < self.rect.x:
            self.rect.x -= speed_x

        if to_y > self.rect.y:
            self.rect.y += speed_y
        if to_y < self.rect.y:
            self.rect.y -= speed_y

        # Второй способ, плохо работающий
        # if to_x > self.rect.x:
        #     self.rect.x += self.speed
        # if to_x < self.rect.x:
        #     self.rect.x -= self.speed
        #
        # if to_y > self.rect.y:
        #     self.rect.y += self.speed
        # if to_y < self.rect.y:
        #     self.rect.y -= self.speed


class Miner(Unit):  # Класс шахтёра, унаследованного от обычно человечка
    def __init__(self, num, tower, x, y, energy=0):
        super().__init__(num, tower, x, y)  # Выполнение инициализации обычного человечка
        self.energy = energy  # и прибавление к этому всему энергии

    def mine(self):
        pass
