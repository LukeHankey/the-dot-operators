#!/usr/bin/venv python3
"""Core Image Manipulation functionality"""

from math import sqrt
from operator import itemgetter
from random import shuffle

from PIL.Image import Image, open


def get_image(
    filename: str, max_dimensions: tuple[int, int], num_of_tiles: int
) -> Image:
    """This could be extended to by addeding filters, and from other sources"""
    with open(filename) as image:
        image.thumbnail(max_dimensions)
        num_of_tiles = int(sqrt(num_of_tiles))

        width = image.width // num_of_tiles
        height = image.height // num_of_tiles
        image = image.crop((0, 0, num_of_tiles * width, num_of_tiles * height))

    return image


def hamming_distance(sequence_0, sequence_1):
    """Find the distance between the solution and the scrambled"""
    return sum(x != y for x, y in zip(sequence_0, sequence_1))


def tile_scrambler(
    tiles: list[tuple[int, int], Image]
) -> list[tuple[tuple[int, int], Image]]:
    """Extract out the positions to shuffle then add back in"""
    positions = list(map(itemgetter(0), tiles))
    length = len(positions)
    new_positions = positions[:]
    shuffle(new_positions)
    while hamming_distance(new_positions, positions) != length:
        shuffle(new_positions)
    return zip(positions, map(itemgetter(1), tiles))
