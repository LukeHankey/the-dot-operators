#!/usr/bin/venv python3
"""This the main entry point"""

from os import listdir
from os.path import join, split
from random import choice

from client import GameClient
from tessellation import square, tile_splitter
from utils import get_image, tile_scrambler

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

MAX_OVERLAP = 0.25
MIN_OVERLAP = 0.15
DEFAULT_OVERLAP = 0.25

MIN_TILE_NUMBER = 16
DEFAULT_TILE_NUMBER = 36

path = join(split(__file__)[0], "images")
filename = choice(
    [  # get a random image on each game run
        f"images/{filename}" for filename in listdir(path)
    ]
)
filename = join(split(__file__)[0], filename)

image = get_image(filename, SCREEN_DIMENSIONS, DEFAULT_TILE_NUMBER)
correct_tiles = tile_splitter(square, image, DEFAULT_TILE_NUMBER)
action = {
    "num_of_tiles": DEFAULT_TILE_NUMBER,
    "image": image,
    "overlap": DEFAULT_OVERLAP,
    "solved_tiles": correct_tiles,
    "scrambled_tiles": tile_scrambler(correct_tiles),
}

game = GameClient(action)
game.mainloop()
