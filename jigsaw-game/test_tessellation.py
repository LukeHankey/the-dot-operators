from os import listdir
from os.path import join, split
from random import choice

from common import get_image
from common.tessellation import polygon_tile_splitter, square_grid

path = join(split(__file__)[0], "images")
filename = choice(
    [  # get a random image on each game run
        f"images/{filename}" for filename in listdir(path)
    ]
)
filename = join(split(__file__)[0], filename)
image = get_image(join(split(__file__)[0], filename), (1000, 1000), 20)
for points, triangle, tile in polygon_tile_splitter(square_grid, image, 20):
    print(points)
    tile.show()
