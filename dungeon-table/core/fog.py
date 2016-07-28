#!/usr/bin/python

import Image
import ImageDraw
import ImageFilter
import pygame
import pygame.gfxdraw

#FOG_SIZE = (200, 200)
#CIRCLE_POSITION = [FOG_SIZE[0] / 2, FOG_SIZE[1] / 2]
BLACK = (20, 20, 20, 255)

class FogOfWar(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill(BLACK)
        self.size = size
        self.visible_position = [0, 0]

        # Sprite details
        self.velocity = [0, 0]
        self._position = [0, 0]
        self._old_position = self.position
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * .5, 8)

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    def set_visible_position(self, position):
        self.visible_position = position

    def update(self, dt):
        self.render_fog()
        pass

    def move_back(self, dt):
        pass

    def render_fog(self):
        self.image.fill((0, 0, 0, 255))
        m = 255/float(200)
        for i in range(200, 1, -1):
            alpha = i * m
            position = [int(self.visible_position[0]), int(self.visible_position[1])]
            pygame.draw.circle(self.image, (0, 0, 0, alpha), position, i)



