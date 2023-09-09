from itertools import product

from jigsaw.fcolor import (
    analogue_palette,
    complementary_palette,
    monochrome_palette,
    random_color,
)
from jigsaw.modifier import CENTERED, UNCENTERED, backing

colors = list(product([0, 255], [0, 255], [0, 255]))
complementaries = [complementary_palette(*color) for color in colors]

colors = [random_color(64, 192), *complementaries, *colors]

output = "n" not in input("output images? [yes] ")

for palette in [analogue_palette, monochrome_palette]:
    for color in colors:
        for centered in [UNCENTERED, CENTERED]:
            print(palette.__name__, color, f"centered={centered}", sep="\t")
            if output:
                backing(500, 500, color, palette, centered).show()
