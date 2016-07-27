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

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

class Config(object):
    """Handles loading of the configuration file for the primary game.

    """
    def __init__(self, file="dungeon.cfg"):
        self.config = configparser.ConfigParser()
        self.config.read(file)

        self.resolution_x = self.config.get("display", "resolution_x")
        self.resolution_y = self.config.get("display", "resolution_y")
        self.resolution = (int(self.resolution_x), int(self.resolution_y))

        self.fullscreen = self.config.getboolean("display", "fullscreen")
        self.fps = int(self.config.get("display", "fps"))

        self.starting_map = self.config.get("game", "starting_map")
        self.starting_position = [int(self.config.get("game", "starting_position_x")),
                                  int(self.config.get("game", "starting_position_y"))]

        self.debug_logging = self.config.get("logging", "debug_logging")
        self.debug_level = str(self.config.get("logging", "debug_level")).lower()
        self.loggers = self.config.get("logging", "loggers")
        self.loggers = self.loggers.replace(" ", "").split(",")

