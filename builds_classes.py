# Файл с классами для основной программы
# Здесь лежат классы каких-либо структур
import pygame
from random import randrange
from classes_of_peoples import Unit  # , Miner

limit = 5


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
        energy = self.output_energy + randrange(limit, -limit, -1)
        return energy


class Tower(pygame.sprite.Sprite):  # Класс башни
    def __init__(self, color, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 30))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.color = color
        self.energy = 100  # Базовое значение энергии
        self.miners = pygame.sprite.Group()

    def spawn_miner(self):
        if self.energy >= 50:
            new_unit = Unit(len(self.miners), self, self.rect.x, self.rect.y)
            self.miners.add(new_unit)
            self.energy -= 50
