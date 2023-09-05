#!/usr/bin/venv python3
"""This the main entry point"""

from os import listdir
from os.path import join, split
from random import choice

from .client import GameClient

path = join(split(__file__)[0], "images")
filename = choice(
    [  # get a random image on each game run
        f"images/{filename}" for filename in listdir(path)
    ]
)
filename = join(split(__file__)[0], filename)
game = GameClient(filename, 16)
game.mainloop()
