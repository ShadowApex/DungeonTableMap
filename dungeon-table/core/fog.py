#!/usr/bin/python
# Based on xinmingzhang's fog of war implementation:
# https://github.com/xinmingzhang/fog_of_war/

import Image
import ImageDraw
import ImageFilter
import pygame
import pygame.gfxdraw

BLACK = (20, 20, 20, 255)

class FogOfWar(pygame.sprite.Sprite):
    def __init__(self, size, walls):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.visible_area = self.image.copy()
        self.image.fill((0,0,0,220))
        self.footprint = self.rect
        self.footprint.midbottom = self.rect.midbottom
        self.mask = pygame.mask.from_surface(self.visible_area)
        self.visible_position = [-1, -1]

        # Sprite details to conform to sprite group
        self.velocity = [0, 0]
        self._position = [0, 0]
        self._old_position = self.position
        self.feet = pygame.Rect(0, 0, self.rect.width * .5, 8)

    def update(self, dt):
        pos = self.visible_position
        if pos[0] == -1:
            return

        player_surface = pygame.Surface(self.rect.size).convert_alpha()
        for i in range(220,0,-10):
            pygame.draw.circle(player_surface,(0,0,0,i),(int(pos[0]),int(pos[1])),int(i/220.0*10+90))
        pygame.draw.circle(player_surface,(0,0,0,0),(int(pos[0]),int(pos[1])),90)
        self.image.blit(player_surface,(0,0),special_flags=pygame.BLEND_RGBA_MIN)
        pygame.draw.circle(self.visible_area, (255, 0, 0), (int(pos[0]), int(pos[1])), 80)
        self.mask = pygame.mask.from_surface(self.visible_area)

    def draw(self,surface):
        surface.blit(self.image, self.rect)

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    def set_visible_position(self, position):
        self.visible_position = position

    def move_back(self, dt):
        pass

