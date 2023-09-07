#!/usr/bin/env python3
"""This is to check what common/secret_codes.py does"""
from operator import itemgetter
from os import listdir
from os.path import join, split

from PIL import Image

from jigsaw.secret_codes import NUM_OF_TILES, filter_tiles, fitted_text_mask
from jigsaw.tessellation import square_tiler, tile_splitter
from jigsaw.utils import get_image, tile_scrambler

# For ever image test the secret_codes
for filename in listdir(join(split(__file__)[0], "../jigsaw/images")):
    # get image and get image with text on it
    filename = join(split(__file__)[0], f"../jigsaw/images/{filename}")
    image = get_image(filename, (800, 800), NUM_OF_TILES)
    text = fitted_text_mask(image, "Hello, World!")

    # get generator from tiled images
    filtered_tiles = list(
        filter_tiles(
            [
                (key, value)
                for key, value in tile_splitter(
                    square_tiler, text, NUM_OF_TILES
                ).items()
            ],
            [
                (key, value)
                for key, value in tile_splitter(
                    square_tiler, image, NUM_OF_TILES
                ).items()
            ],
        )
    )

    # now lets paste it all together and show the user
    final = Image.new("RGB", image.size, "white")
    for pos, tile in filter(itemgetter(1), filtered_tiles):
        bbox = (pos[0], pos[1], pos[0] + tile.width, pos[1] + tile.height)
        final.paste(tile, bbox)
    final.show()

    # show scrambled
    for pos, tile in filter(
        itemgetter(1), tile_scrambler({key: value for (key, value) in filtered_tiles})
    ):
        bbox = (pos[0], pos[1], pos[0] + tile.width, pos[1] + tile.height)
        final.paste(tile, bbox)
    final.show()
