"""This the main entry point"""

from json import dump, load
from os import listdir
from os.path import exists, join, split
from random import choice

from client.menu import Menu

LOG_FILENAME = ".log.json"

game_log = load(open(LOG_FILENAME)) if exists(LOG_FILENAME) else {}
path = join(split(__file__)[0], "images")
filename = choice(
    [  # get a random image on each game run
        f"jigsaw/images/{filename}" for filename in listdir(path)
    ]
)
filename = join(split(__file__)[0], filename)
menu = Menu(filename)
menu.mainloop()

with open(LOG_FILENAME, "w") as log_file:
    dump(game_log, log_file, indent=1)

