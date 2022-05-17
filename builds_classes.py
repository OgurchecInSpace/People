# Файл с классами для основной программы
# Здесь лежат классы каких-либо структур
import pygame
from random import randrange
from classes_of_people import *
from constants import *


class Ore(pygame.sprite.Sprite):
    # Класс руды, в котором можно задавать кол-во энергии.
    # Энергия эта будет отдаваться во время добычи шахтёру
    # Этим самым можно как бы выбирать тип руды
    def __init__(self, x, y, output_energy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((40, 40))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.output_energy = output_energy

    def give_energy(self):
        # Метод выдачи энергии шахтёру
        energy = self.output_energy
        return energy / 10


class Tower(pygame.sprite.Sprite):  # Класс башни
    def __init__(self, color, x, y, health=1000):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 90))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.status = 'Good'
        self.last_health = health
        self.health = health
        self.color = color
        self.energy = 351  # Базовое значение энергии
        self.miners = pygame.sprite.Group()
        self.warriors = pygame.sprite.Group()
        self.tick = 0

    def __repr__(self):
        return f'Башня на X:{self.rect.x} Y:{self.rect.y}'

    def spawn_miner(self):
        new_miner = Miner(len(self.miners), self, self.rect.x, self.rect.y)
        self.miners.add(new_miner)
        self.energy -= cost_miner
        print('spawn miner')

    def spawn_warrior(self):
        new_warrior = Warrior(len(self.warriors), self, self.rect.x, self.rect.y)
        self.warriors.add(new_warrior)
        self.energy -= cost_warrior
        print('spawn warrior')

    def update(self):
        self.tick += 1
        if self.tick % 10 == 0:  # Создаём с некоторой периодичностью воинов и шахтёров
            if self.energy >= cost_warrior:
                self.spawn_warrior()
        if self.tick % 20 == 0:
            if self.energy >= cost_miner:
                self.spawn_miner()

        if self.health < self.last_health:
            self.status = 'Bad'
            self.last_health = self.health
        else:
            self.status = 'Good'
