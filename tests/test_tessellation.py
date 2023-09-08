from os import listdir
from os.path import join, split
from random import choice

from jigsaw.tessellation import polygon_tile_splitter, square_grid
from jigsaw.utils import get_image

path = join(split(__file__)[0], "../jigsaw/images")
filename = choice(
    [  # get a random image on each game run
        f"../jigsaw/images/{filename}" for filename in listdir(path)
    ]
)
filename = join(split(__file__)[0], filename)
image = get_image(join(split(__file__)[0], filename), (1000, 1000), 20)
for points, triangle, tile in polygon_tile_splitter(square_grid, image, 20):
    print(points)
    tile.show()
