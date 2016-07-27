#!/usr/bin/python

import os.path

import pygame
from pygame.locals import *
from pytmx.util_pygame import load_pygame

import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

from core import prepare

RESOURCES_DIR = 'resources'
HERO_MOVE_SPEED = 200 # pixels per second
MAP_FILENAME = 'dungeon-017.tmx'

def get_map(filename):
    return os.path.join(RESOURCES_DIR + "/maps", filename)

def load_image(filename):
    return pygame.image.load(os.path.join(RESOURCES_DIR + "/tilesets", filename))

def load_sprite(filename):
    return pygame.image.load(os.path.join(RESOURCES_DIR + "/sprites", filename))

def get_starting_position(tile_width, tile_position):
    position = (tile_position[0] * tile_width,
                tile_position[1] * tile_width)
    return position

class Hero(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_sprite('cross.png').convert_alpha()
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

    def update(self, dt):
        self._old_position = self._position[:]
        self._position[0] += self.velocity[0] * dt
        self._position[1] += self.velocity[1] * dt
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self, dt):
        """ If called after an update, the sprite can move back
        """
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

class DungeonMap(object):
    """Main game class.

    This class will load data, create a pyscroll group, a hero object.
    """
    filename = get_map(MAP_FILENAME)

    def __init__(self):
        self.running = False

        # load map data
        tmx_data = load_pygame(self.filename)

        # setup level geometry with simple pygame rects, loaded from pytmx
        self.walls = list()
        for object in tmx_data.objects:
            self.walls.append(pygame.Rect(
                object.x, object.y,
                object.width, object.height))

        # create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(tmx_data)

        # create new renderer (camera)
        # clamp_camera is used to prevent the map from scrolling past the edge
        self.map_layer = pyscroll.BufferedRenderer(map_data,
                                                   screen.get_size(),
                                                   clamp_camera=True)
        self.map_layer.zoom = 2


        # pyscroll supports layered rendering.  our map has 3 'under' layers
        # layers begin with 0, so the layers are 0, 1, and 2.
        # since we want the sprite to be on top of layer 1, we set the default
        # layer for sprites as 2
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)
        self.hero = Hero()

        # put the hero in the starting position of the map
        self.hero.position = get_starting_position(tmx_data.tilewidth,
                                                   prepare.CONFIG.starting_position)

        # add our hero to the group
        self.group.add(self.hero)

    def draw(self, surface):
        # center the map/screen on the party
        self.group.center(self.hero.rect.center)

        # draw the map and all sprites
        self.group.draw(surface)

    def handle_input(self):
        """ Handle pygame input events
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    break

                elif event.key == K_EQUALS:
                    self.map_layer.zoom += .25

                elif event.key == K_MINUS:
                    value = self.map_layer.zoom - .25
                    if value > 0:
                        self.map_layer.zoom = value

            elif event.type == pygame.VIDEORESIZE:
                init_screen(event.w, event.h)
                self.map_player.set_size((event.w / 2, event.h / 2))

        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            self.hero.velocity[1] = -HERO_MOVE_SPEED
        elif pressed[K_DOWN]:
            self.hero.velocity[1] = HERO_MOVE_SPEED
        else:
            self.hero.velocity[1] = 0

        if pressed[K_LEFT]:
            self.hero.velocity[0] = -HERO_MOVE_SPEED
        elif pressed[K_RIGHT]:
            self.hero.velocity[0] = HERO_MOVE_SPEED
        else:
            self.hero.velocity[0] = 0


    def update(self, dt):
        """ Tasks that occur over time should be handled here
        """
        self.group.update(dt)

        # check if the sprite's feet are colliding with wall
        # sprite must have a rect called feet, and move_back method,
        # otherwise this will fail
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back(dt)

    def run(self):
        """ Run the game loop
        """
        clock = pygame.time.Clock()
        fps = 60
        scale = pygame.transform.scale
        self.running = True

        try:
            while self.running:
                dt = clock.tick(fps) / 1000.
                self.handle_input()
                self.update(dt)
                self.draw(temp_surface)
                scale(temp_surface, screen.get_size(), screen)
                pygame.display.flip()
        except KeyboardInterrupt:
            self.running = False

def init_screen(width, height):
    global temp_surface
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    temp_surface = pygame.Surface((width / 2, height / 2)).convert()
    return screen

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    screen = init_screen(1280, 720)
    pygame.display.set_caption('Dungeon Table Map')

    try:
        game = DungeonMap()
        game.run()
    except:
        pygame.quit()
        raise
