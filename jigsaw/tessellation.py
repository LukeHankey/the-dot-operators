from math import sqrt

from PIL.Image import Image


def generate_tiles(
    image: Image,
    num_of_tiles: int,
) -> list[tuple[tuple[int, int], Image]]:
    """Opens image file and splits it into tiles and shuffles them"""
    num_of_tiles = int(sqrt(num_of_tiles))
    tiles = list()

    width = image.width // num_of_tiles
    height = image.height // num_of_tiles

    for x in range(0, image.width, width):
        for y in range(0, image.height, height):
            bbox = (x, y, x + width, y + height)
            tiles.append(((x, y), image.crop(bbox)))

    return tiles
