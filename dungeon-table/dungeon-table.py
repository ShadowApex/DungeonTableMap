#!/usr/bin/python

import os.path

import pygame
from pygame.locals import *
from pytmx.util_pygame import load_pygame

import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

from core import prepare
from core import fog

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def get_map(filename):
    return get_resource("/maps", filename)

def get_music(filename):
    return get_resource("/music", filename)

def load_sprite(filename):
    return pygame.image.load(get_resource("/sprites", filename))

def get_resource(data_dir, filename):
    if os.path.isfile(os.path.join(prepare.USER_DATA_PATH + data_dir, filename)):
        return os.path.join(prepare.USER_DATA_PATH + data_dir, filename)

    return os.path.join(prepare.RESOURCES_DIR + data_dir, filename)

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
    filename = get_map(prepare.CONFIG.starting_map)

    def __init__(self):
        self.running = False
        self.fog_enabled = False

        # load map data
        tmx_data = load_pygame(self.filename, pixelalpha=True)

        # load and play music if one is defined
        if "music" in tmx_data.properties:
            music = tmx_data.properties["music"]
            pygame.mixer.music.load(get_music(music))
            pygame.mixer.music.play(-1)

        # use fog of war if it is defined
        if "fog" in tmx_data.properties:
            if tmx_data.properties["fog"].lower() in ["yes", "true"]:
                self.fog_enabled = True

        # use starting position if defined in map
        if "start" in tmx_data.properties:
            starting_position = tmx_data.properties["start"].replace(" ", "").split(",")
            starting_position[0] = int(starting_position[0])
            starting_position[1] = int(starting_position[1])
        else:
            starting_position = prepare.CONFIG.starting_position

        # setup level geometry with simple pygame rects, loaded from pytmx
        self.walls = list()
        for object in tmx_data.objects:
            self.walls.append(pygame.Rect(
                object.x, object.y,
                object.width, object.height))

        # create fog layer
        if self.fog_enabled:
            fog_width = tmx_data.tilewidth * tmx_data.width
            fog_height = tmx_data.tileheight * tmx_data.height
            self.fog_of_war = fog.FogOfWar((fog_width, fog_height), self.walls)

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
                                                   starting_position)

        # add our hero to the group
        self.group.add(self.hero)
        if self.fog_enabled:
            self.group.add(self.fog_of_war)

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

                elif event.key ==K_f:
                    flags = screen.get_flags()
                    #toggle fullscreen by pressing F key.
                    if flags&FULLSCREEN==False:
                        flags|=FULLSCREEN
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
                    else:
                        flags^=FULLSCREEN
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)

        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            self.hero.velocity[1] = -prepare.CONFIG.move_speed
        elif pressed[K_DOWN]:
            self.hero.velocity[1] = prepare.CONFIG.move_speed
        else:
            self.hero.velocity[1] = 0

        if pressed[K_LEFT]:
            self.hero.velocity[0] = -prepare.CONFIG.move_speed
        elif pressed[K_RIGHT]:
            self.hero.velocity[0] = prepare.CONFIG.move_speed
        else:
            self.hero.velocity[0] = 0


    def update(self, dt):
        """ Tasks that occur over time should be handled here
        """
        self.group.update(dt)

        # Update the visibility of the fog of war
        if self.fog_enabled:
            self.fog_of_war.set_visible_position(self.hero.position)

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
    pygame.mixer.init()
    screen = init_screen(SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.display.set_caption('Dungeon Table Map')

    try:
        game = DungeonMap()
        game.run()
    except:
        pygame.quit()
        raise
