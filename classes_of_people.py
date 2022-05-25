# Файл с классами человечков
import random
import pygame
from constants import *


class Unit(pygame.sprite.Sprite):  # Класс самого простого человечка
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
        self.position = 'tower'
        self.on_position = 0

    def is_near(self, obj):  # Метод проверки близости к объекту
        if self.rect.x in range(obj.rect.x - self.diapason, obj.rect.x + self.diapason) \
                and self.rect.y in range(obj.rect.y - self.diapason, obj.rect.y + self.diapason):
            return True
        return False

    def get_nearest(self, collection):  # Метод получения ближайшего чего-то из коллекции
        if len(collection) > 0:
            obj_near = sorted(collection,  # Получаем это нечто ближайшее
                              key=lambda obj:
                              ((obj.rect.x - self.rect.x) ** 2 + (obj.rect.y - self.rect.y) ** 2) ** 0.5)[-1]
            return obj_near

    def go(self, to_x, to_y, speed):
        self.position = 'space'
        self.on_position = 0
        # Первый способ передвижения на доработке, но и так сойдёт
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


class Miner(Unit):  # Класс шахтёра, унаследованного от обычно человечка
    def __init__(self, num, tower, x, y, energy=0):
        super().__init__(num, tower, x, y, health=50, color=(255, 0, 0))  # Выполнение инициализации обычного человечка
        self.energy = energy  # и прибавление к этому всему энергии, скорости и диапазона, в котором шахтёр достаёт
        self.speed = 6
        self.diapason = miner_diapason
        self.position = 'tower'

    def update(self, ores):  # Метод, в котором идёт выбор того, что шахтёр сейчас будет делать
        if self.energy >= 100:  # Если энергии больше 100 (т.е. пора отдавать башне)
            if self.is_near(self.tower):  # Если близко к башне, то отдаём ей энергию
                self.unloading_energy()
            else:  # Если нет, то идём к башне
                self.go(to_x=self.tower.rect.x, to_y=self.tower.rect.y, speed=self.speed)
        else:  # Если нет, то идём копать руду
            ore_near = self.get_nearest(ores)
            if self.is_near(ore_near):  # Если рядом, то копаем её
                self.mine(ore_near)
            else:  # Если далеко, то идём к ней
                self.go(ore_near.rect.x, ore_near.rect.y, self.speed)

    def mine(self, ore):  # Метод копания
        self.position = 'ore'
        self.energy += ore.give_energy()

    def unloading_energy(self):  # Метод отправки энергии башне
        self.position = 'tower'
        while self.energy > 10:
            self.energy -= 10
            self.tower.energy += 10


class Warrior(Unit):  # Класс воина
    def __init__(self, num, tower, x, y, energy=0, health=150, damage=20):
        super().__init__(num, tower, x, y, health, color=(255, 255, 255))
        self.energy = energy
        self.speed = 10
        self.diapason = warrior_diapason
        self.damage = damage
        self.position = 'tower'
        self.status = None
        self.on_position = 0
        self.commands = {}

    def __repr__(self):
        return f'Воин башни {self.tower}'

    def update(self, towers, ores):
        from builds_classes import Tower, Ore
        for tower in towers:
            for warrior in tower.warriors:
                if self.is_near(warrior):
                    self.attack(towers)

        if isinstance(self.tower.command['command'], Tower):
            tower = self.tower.command['command']
            if self.is_near(tower):
                self.attack(tower, is_tower=True)
            else:
                self.go(tower.rect.x, tower.rect.y, self.speed)
        elif isinstance(self.tower.command['command'], Ore):
            ore = self.tower.command['command']
            if self.is_near(ore):
                self.attack(towers)
            else:
                self.go(ore.rect.x, ore.rect.y, self.speed)
        elif self.tower.command['command'] == 'def_tower':
            if self.is_near(self.tower):  # Если башня близко, то ищем ближайшего противника
                self.attack(towers)
            else:
                self.go(self.tower.rect.x, self.tower.rect.y, self.speed)

    def attack(self, towers, is_tower=False):  # Метод атаки противника (куда без него в симуляции людишек)
        if is_tower:  # Если мы атакуем башню, то атакуем её (капитан очевидность)
            towers.health -= self.damage
            if towers.health <= 0:
                for warrior in towers.warriors.copy():
                    warrior.kill()
                for miner in towers.miners.copy():
                    miner.kill()
                towers.kill()
                print(f'{self} уничтожил башню {towers}')
        else:  # Если мы не атакуем башню, то ищем ближайших противников от каждой башни
            near_warriors = set()
            for tower in towers:
                near_warrior = self.get_nearest(tower.warriors)
                if near_warrior is not None and near_warrior.tower != self.tower:
                    near_warriors.add(near_warrior)
            near_warrior = self.get_nearest(near_warriors)  # Получили ближайшего противника от всех башен
            if near_warrior is not None:  # Если он всё-таки существует, то бьём его
                if self.is_near(near_warrior):  # Если противник рядом
                    near_warrior.health -= self.damage  # Танком его!
                    if near_warrior.health <= 0:  # Если ненароком противника убили, то удаляем противника отовсюду
                        near_warrior.kill()
                        print(f'{self} убил {near_warrior}')  # И пишем об этом
                else:  # Если ближайший противник не рядом, то идём к нему
                    self.go(near_warrior.rect.x, near_warrior.rect.y, self.speed)
