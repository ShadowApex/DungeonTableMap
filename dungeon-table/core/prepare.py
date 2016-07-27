#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Dungeon Table Map
# Copyright (C) 2016, William Edwards <shadowapex@gmail.com>
#
# This file is part of Dungeon Table Map.
#
# Dungeon Table Map is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Dungeon Table Map is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Dungeon Table Map.  If not, see <http://www.gnu.org/licenses/>.
#
# Contributor(s):
#
# William Edwards <shadowapex@gmail.com>
#

import config
import os
import shutil
from platform import *

# Get the Dungeon Map base directory
BASEDIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")) + os.sep

# Set up our config directory
CONFIG_FILE_NAME = "dungeon.cfg"
CONFIG_PATH = get_config_path() + "/.local/share/dungeontable/"
try:
    os.makedirs(CONFIG_PATH)
except OSError:
    if not os.path.isdir(CONFIG_PATH):
        raise

# Create a copy of our default config if one does not exist in the home dir.
CONFIG_FILE_PATH = CONFIG_PATH + CONFIG_FILE_NAME
if not os.path.isfile(CONFIG_FILE_PATH):
    try:
        shutil.copyfile(BASEDIR + CONFIG_FILE_NAME, CONFIG_FILE_PATH)
    except OSError:
        raise

# Set up our custom campaign data directory.
USER_DATA_PATH = CONFIG_PATH + "data/resources"
if not os.path.isdir(USER_DATA_PATH):
    try:
        os.makedirs(USER_DATA_PATH)
    except OSError:
        if not os.path.isdir(USER_DATA_PATH):
            raise

for data_dir in ["/maps", "/sprites", "/tilesets"]:
    if not os.path.isdir(USER_DATA_PATH + data_dir):
        try:
            os.makedirs(USER_DATA_PATH + data_dir)
        except OSError:
            if not os.path.isdir(USER_DATA_PATH + data_dir):
                raise

# Read the "dungeon.cfg" configuration file
CONFIG = config.Config(CONFIG_FILE_PATH)

RESOURCES_DIR = 'resources'
HERO_MOVE_SPEED = 200 # pixels per second
MAP_FILENAME = CONFIG.starting_map
