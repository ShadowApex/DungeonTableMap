# Dungeon Table Map
Dungeon Table Map is an open source map display program for table-top D&amp;D maps. Dungeon Table Map allows
you as a Dungeon Master to craft your own maps using the [Tiled](http://www.mapeditor.org/) map editor and
display them on a screen laid out flat. When running your campaign you can also use it to play music and sound
effects at the appropriate moment, and explore the map with fog of war.

![](http://makezine.com/wp-content/uploads/2015/12/gamingTable_5.jpg)

[source](http://makezine.com/2015/12/08/how-to-build-a-high-end-gaming-table-for-as-little-as-150/)

Features
--------

- Load scrollable maps
- Collidable walls
- Play music when map loads
- Fog of war

**Planned Features**

- Walls block vision of other rooms/locations
- Tie maps together
- Event system for playing sound effects at desired times

Version
-------

0.1

Requirements
------------

- pytmx
- pyscroll
- pygame

Installation
------------

**Ubuntu**

```sh
sudo apt-get install python python-pygame python-pip
sudo pip install pytmx
sudo pip install pyscroll
git clone https://github.com/ShadowApex/DungeonTableMap.git
cd DungeonTableMap/dungeon-table
./dungeon-table.py
```

Special Thanks
--------------

Thanks to [bitcraft](https://github.com/bitcraft) for the amazing pyscroll and pytmx libraries which is this
heavily based on!

License
----

GNU v3

Copyright (C) 2016 William Edwards <shadowapex@gmail.com> 

This software is distributed under the GNU General Public Licence as published
by the Free Software Foundation.  See the file LICENSE for the conditions
under which this software is made available.  Tuxemon also contains code from
other sources.
