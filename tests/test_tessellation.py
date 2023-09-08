from os import listdir
from os.path import join, split
from random import choice

from jigsaw.tessellation import square, tile_splitter, x_iso, y_iso
from jigsaw.utils import get_image

path = join(split(__file__)[0], "../jigsaw/images")
filename = choice(
    [  # get a random image on each game run
        f"../jigsaw/images/{filename}" for filename in listdir(path)
    ]
)
filename = join(split(__file__)[0], filename)
image = get_image(join(split(__file__)[0], filename), (1000, 1000), 20)

output = "n" not in input("do you want to output the images? [yes] ")

for grid in [square, x_iso, y_iso]:
    for topleft, tile_paramters in tile_splitter(grid, image, 20):
        xy, tile, extra = tile_paramters
        if extra:
            (verticies, edges) = extra
            print(
                topleft,
                xy,
                *[(int(x), int(y)) for (x, y) in verticies],
                *[(int(x), int(y), angle) for (x, y), angle in edges],
            )
        else:
            print(topleft, xy)
        if output:
            tile.show()
