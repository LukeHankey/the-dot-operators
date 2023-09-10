from itertools import product
from os import chdir

from jigsaw.fcolor import (
    analogue_palette,
    complementary_color,
    monochrome_palette,
    random_color,
)
from jigsaw.modifier import CENTERED, UNCENTERED, backing
from jigsaw.utils import get_generated_image

chdir(__import__("jigsaw").utils.__file__.rstrip("utils.py"))


colors = list(product([0, 255], [0, 255], [0, 255]))
complementaries = [complementary_color(*color) for color in colors]

colors = [random_color(64, 192), *complementaries, *colors]

output = "n" not in input("output images? [yes] ")

while not input("continue"):
    get_generated_image((1000, 1000), 16).show()

for palette in [analogue_palette, monochrome_palette]:
    for color in colors:
        for centered in [UNCENTERED, CENTERED]:
            print(palette.__name__, color, f"centered={centered}", sep="\t")
            if output:
                backing(500, 500, color, palette, centered).show()
