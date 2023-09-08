from collections.abc import Callable, Generator
from math import atan2
from typing import Any

import numpy as np
from numpy.typing import NDArray
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


def square_grid(width: int, height: int, num_of_tiles: int) -> NDArray[np.int64]:
    """This function is an example to compare with isogrid.

    This doesn't actually create squares by itself as Delaunay breaks
    any grid into triangles.
    """
    x_spacing = width // num_of_tiles
    y_spacing = height // num_of_tiles

    xv, yv = np.meshgrid(
        np.arange(0, width, x_spacing), np.arange(0, height, y_spacing)
    )
    inside_isogrid = (xv >= 0) & (xv <= width + 1) & (yv >= 0) & (yv <= height + 1)

    return np.column_stack((xv[inside_isogrid], yv[inside_isogrid]))


def isogrid(width: int, height: int, num_of_tiles: int) -> NDArray[np.float64]:
    """A grid that produces regular triangles

    Read [here](https://en.wikipedia.org/wiki/Euclidean_tilings_by_convex_regular_polygons)
    for more about the different grid patterns
    """
    x_spacing = width // num_of_tiles
    y_spacing = height // num_of_tiles

    # Create a np.meshgrid of points
    xv, yv = np.meshgrid(
        np.arange(0, width, x_spacing), np.arange(0, height, y_spacing * np.sqrt(3) / 2)
    )

    # Offset rows of points
    offset = y_spacing / 2
    yv[:, 1::2] += offset

    # Filter points to keep only those inside the isogrid pattern
    inside_isogrid = (xv >= 0) & (xv <= width) & (yv >= 0) & (yv <= height)

    return np.column_stack((xv[inside_isogrid], yv[inside_isogrid]))


def polygon_tile_splitter(
    tiler: Callable[[int, int, int], NDArray[np.float64 | np.int64]],
    image: Image,
    num_of_tiles: int,
) -> Generator[tuple[list[tuple[Any, Any]], NDArray[np.intc], Image], None, None]:
    """This will take in the `tiler` and run it to get its grid points

    I think isogrid will become the default and we will build up shapes
    from their, maybe change to 'offset' to allow slightly different triangles.
    the `tiler` function will then become a "contructer" to stitch triangles
    together
    """
    num_of_tiles = int(np.sqrt(num_of_tiles))

    width, height = image.width, image.height
    points = tiler(width, height, num_of_tiles)

    # Draw lines along the triangulation edges
    for triangle in Delaunay(points).simplices:
        verticies = [points[triangle[i]] for i in range(3)]
        verticies = [(p[0], p[1]) for p in verticies]

        mask = new("L", image.size, 0)

        draw = Draw(mask)
        draw.polygon(verticies, fill=255)

        tile = composite(image, new("RGBA", image.size, (0, 0, 0, 0)), mask)

        yield mask.getbbox()[:2], (
            verticies,
            edge_parameters(verticies),
            tile.crop(mask.getbbox()),
        )


def tile_splitter(
    tile_generator: Callable[
        [Image, int, int], Generator[tuple[tuple[int, int], Image], None, None]
    ],
    image: Image,
    num_of_tiles: int,
) -> dict[tuple[int, int], Image]:
    """Opens image file and splits it into tiles and shuffles them"""
    sequence: dict[tuple[int, int], Image] = {}
    num_of_tiles = int(np.sqrt(num_of_tiles))

    width = image.width // num_of_tiles
    height = image.height // num_of_tiles

    for pos, tile in tile_generator(image, width, height):
        sequence[pos] = (pos, tile)

    return sequence


def square_tiler(
    image: Image, width: int, height: int
) -> Generator[tuple[tuple[int, int], Image], None, None]:
    """Tile generator with the inner most loop calling the specific

    shape for tiling applies the mask of the shape then continues
    """
    for x in range(0, image.width, width):
        for y in range(0, image.height, height):
            yield (x, y), image.crop((x, y, x + width, y + height))


def einstein_tiler(
    image: Image, width: int, height: int
) -> Generator[tuple[tuple[int, int], Image], None, None]:
    """
    Tile image into einstein tiles.

    This is an aperiodic monotile composed of 8 kites from a deltoidal trihexagonal tile.
    """
    raise NotImplementedError("einstein_tiler not yet implemented")
