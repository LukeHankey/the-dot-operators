#!/usr/bin/venv python3
"""This the main entry point"""

from os.path import join, split
from os import listdir
from random import choice
from common import regular_tiles, square_tiles
from client import (
    Tile, mainloop, SCREEN_WIDTH, SCREEN_HEIGHT)
from pygame import init, sprite, display


if __name__ == "__main__":
    init()
    screen = display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    path = join(split(__file__)[0], "images")
    filename = choice([  # get a random image on each game run
        f"images/{filename}" for filename in listdir(path)])
    filename = join(split(__file__)[0], filename)

    tiles = sprite.Group()
    for pos, image_tile in regular_tiles(filename, 16, square_tiles):
        tiles.add(Tile(pos, image_tile))

    mainloop(screen, tiles)
