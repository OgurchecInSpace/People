# Файл с классами человечков
import random
import pygame
from constants import *


class Unit(pygame.sprite.Sprite):  # Класс самого просто человечка
    def __init__(self, num, tower, x, y, health, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.BLACK = (0, 0, 0)
        self.num = num
        self.tower = tower
        self.speed = 8
        self.health = health
        self.diapason = 0

    def is_near(self, obj):  # Метод проверки близости к объекту
        if self.rect.x in range(obj.rect.x - self.diapason, obj.rect.x + self.diapason) \
                and self.rect.y in range(obj.rect.y - self.diapason, obj.rect.y + self.diapason):
            return True
        return False

    def go(self, to_x, to_y, speed):
        # Первый способ передвижения (и самый лучший!) на доработке, но и так сойдёт
        leg_x = abs(self.rect.x - to_x)  # один катет
        leg_y = abs(self.rect.y - to_y)  # другой катет
        hyp = (leg_x ** 2 + leg_y ** 2) ** 0.5  # Гипотенуза прямоугольного треугольника, по который мы должны двигаться
        if hyp != 0:
            speed_x = round(speed * (leg_x / hyp))
            speed_y = round(speed * (leg_y / hyp))
        else:
            return None

        if to_x > self.rect.x:  # По X
            self.rect.x += speed_x
        if to_x < self.rect.x:
            self.rect.x -= speed_x
        if to_y > self.rect.y:  # По Y
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
        super().__init__(num, tower, x, y, health=50, color=(255, 0, 0))  # Выполнение инициализации обычного человечка
        self.energy = energy  # и прибавление к этому всему энергии, скорости и диапазона, в котором шахтёр достаёт
        self.speed = 6
        self.diapason = miner_diapason

    def update(self, ores):  # Метод, в котором идёт выбор того, что шахтёр сейчас будет делать
        if self.energy >= 100:  # Если энергии больше 100 (т.е. пора отдавать башне)
            if self.is_near(self.tower):  # Если близко к башне, то отдаём ей энергию
                self.unloading_energy()
            else:  # Если нет, то идём к башне
                self.go(to_x=self.tower.rect.x, to_y=self.tower.rect.y, speed=self.speed)
        else:  # Если нет, то идём копать руду
            ore_near = sorted(ores,  # Получаем ближайшую руду
                              key=lambda ore:
                              ((ore.rect.x - self.rect.x) ** 2 + (ore.rect.y - self.rect.y) ** 2) ** 0.5)[-1]
            if self.is_near(ore_near):  # Если рядом, то копаем её
                self.mine(ore_near)
            else:  # Если далеко, то идём к ней
                self.go(ore_near.rect.x, ore_near.rect.y, self.speed)

    def mine(self, ore):  # Метод копания
        self.energy += ore.give_energy()

    def unloading_energy(self):  # Метод отправки энергии башне
        while self.energy > 10:
            self.energy -= 10
            self.tower.energy += 10


class Warrior(Unit):  # Класс воина
    def __init__(self, num, tower, x, y, energy=0, health=150):
        super().__init__(num, tower, x, y, health, color=(255, 255, 255))
        self.energy = energy
        self.speed = 10
        self.diapason = warrior_diapason
        self.image.fill((255, 255, 255))

    def update(self):
        if self.tower.status == 'Bad' and random.randrange(0, 2):
            if self.is_near(self.tower):
                pass
            else:
                self.go(self.tower.rect.x, self.tower.rect.y, self.speed)
        elif self.tower.status == 'Very bad':
            if self.is_near(self.tower):
                pass
            else:
                self.go(self.tower.rect.x, self.tower.rect.y, self.speed)

    def attack(self):
        pass
