from os import listdir
from os.path import join, split

from jigsaw.tessellation import generate_tiles
from jigsaw.utils import get_image, tile_scrambler

path = join(split(__file__)[0], "../jigsaw/images")
filenames = [f"../jigsaw/images/{filename}" for filename in listdir(path)]

output = "n" not in input("do you want to output the images? [yes] ")
num_of_tiles = 25

for filename in filenames:
    image = get_image(join(split(__file__)[0], filename), (1000, 1000), num_of_tiles)
    if output:
        image.show()
    tiles = generate_tiles(image, num_of_tiles)
    for pos_0, (pos_1, tile) in tile_scrambler(tiles):
        print(pos_0, pos_1)
        if output:
            tile.show()
