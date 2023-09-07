#!/usr/bin/venv python3
"""This the main entry point"""

from os import listdir
from os.path import join, split
from random import choice

from client import GameClient

if __name__ == "__main__":
    path = join(split(__file__)[0], "images")
    filename = choice(
        [  # get a random image on each game run
            f"images/{filename}" for filename in listdir(path)
        ]
    )
    action = {"num_of_tiles": 16}
    action["overlap"] = 0.25  # 25% is the default value with a minimum of 15%
    action["filename"] = join(split(__file__)[0], filename)
    game = GameClient(action)
    game.mainloop()
