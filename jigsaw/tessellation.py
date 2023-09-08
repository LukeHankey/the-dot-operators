from collections.abc import Callable, Generator
from math import atan2

import numpy as np

# from numpy.typing import NDArray
from PIL.Image import Image, new
from PIL.ImageChops import composite
from PIL.ImageDraw import Draw
from scipy.spatial import Delaunay


def edge_parameters(verticies):
    """To be used in polygon snapping"""
    edges = []
    for edge in np.array(list(zip(verticies, np.roll(verticies, -1, axis=0)))):
        edge_center = ((edge[0, 0] + edge[1, 0]) / 2, (edge[0, 1] + edge[1, 1]) / 2)
        edge_angle = atan2(edge[1, 0] - edge[0, 0], edge[1, 1] - edge[0, 1])
        edges.append((edge_center, edge_angle))
    return edges


def __iso(
    image: Image, width: int, height: int, y_axis: bool
) -> Generator[
    tuple[tuple[int, int], tuple[tuple[int, int], Image, tuple[float, float, float]]],
    None,
    None,
]:
    """A grid that produces regular triangles

    Read [here](https://en.wikipedia.org/wiki/Euclidean_tilings_by_convex_regular_polygons)
    for more about the different grid patterns
    """
    xv, yv = np.meshgrid(
        np.arange(0, image.width, width * (np.sqrt(3) / 2 if not y_axis else 1)),
        np.arange(0, image.height, height * (np.sqrt(3) / 2 if y_axis else 1)),
    )
    if y_axis:
        yv[:, 1::2] += height / 2  # offset on even
    else:
        xv[1::2, :] += width / 2  # offset on even
    inside_isogrid = (xv >= 0) & (xv <= image.width) & (yv >= 0) & (yv <= image.height)

    points = np.column_stack((xv[inside_isogrid], yv[inside_isogrid]))

    for triangle in Delaunay(points).simplices:
        verticies = [points[triangle[i]] for i in range(3)]
        verticies = [(p[0], p[1]) for p in verticies]
        mask = new("L", image.size, 0)
        draw = Draw(mask)
        draw.polygon(verticies, fill=255)
        tile = composite(image, new("RGBA", image.size, (0, 0, 0, 0)), mask)
        yield mask.getbbox()[:2], (
            mask.getbbox()[:2],
            tile.crop(mask.getbbox()),
            (verticies, edge_parameters(verticies)),
        )


def y_iso(image, width, height):
    """A generator Isogrid which shifts on the y axis"""
    yield from __iso(image, width, height, True)


def x_iso(image, width, height):
    """A generator Isogrid which shifts on the x axis"""
    yield from __iso(image, width, height, False)


def tile_splitter(
    tile_generator: Callable[
        [Image, int, int], Generator[tuple[tuple[int, int], Image], None, None]
    ],
    image: Image,
    num_of_tiles: int,
) -> Generator[tuple[tuple[int, int], Image], None, None]:
    """Opens image file and splits it into tiles and shuffles them"""
    num_of_tiles = int(np.sqrt(num_of_tiles))

    width = image.width // num_of_tiles
    height = image.height // num_of_tiles

    for pos, tile_params in tile_generator(image, width, height):
        yield (pos, tile_params)


def square(
    image: Image, width: int, height: int
) -> Generator[tuple[tuple[int, int], Image], None, None]:
    """Tile generator with the inner most loop calling the specific

    shape for tiling applies the mask of the shape then continues
    """
    for x in range(0, image.width, width):
        for y in range(0, image.height, height):
            bbox = (x, y, x + width, y + height)
            yield (x, y), ((x, y), image.crop(bbox), None)


def einstein_tiler(
    image: Image, width: int, height: int
) -> Generator[tuple[tuple[int, int], Image], None, None]:
    """
    Tile image into einstein tiles.

    This is an aperiodic monotile composed of 8 kites from a deltoidal trihexagonal tile.
    """
    raise NotImplementedError("einstein_tiler not yet implemented")
