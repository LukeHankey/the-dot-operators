from os import listdir
from os.path import join, split
from random import choice

from jigsaw.tessellation import isogrid, polygon_tile_splitter
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
print(" topleft \t:\t vertex_0\tvertex_1\tvertex_2")
for topleft, tile in polygon_tile_splitter(isogrid, image, 20):
    verticies, edges, image = tile
    print(
        topleft,
        "\t:\t",
        *[(int(x), int(y)) for x, y in verticies],
        "\t:\t",
        *[(int(x), int(y), angle) for (x, y), angle in edges],
    )
    if output:
        tile.show()
