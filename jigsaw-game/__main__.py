#!/usr/bin/venv python3
"""This the main entry point"""

from os import listdir
from os.path import join, split
from random import choice

from client import GameClient
from client.menu import menu

if __name__ == "__main__":
    action = menu()
    while action:
        path = join(split(__file__)[0], "images")
        filename = choice([  # get a random image on each game run
            f"images/{filename}" for filename in listdir(path)])
        action["filename"] = join(split(__file__)[0], filename)
        action["num_of_tiles"] = 16

        game = GameClient(action)
        game.mainloop()

        action = menu()
