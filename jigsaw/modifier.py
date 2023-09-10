from collections.abc import Callable

import numpy as np
from fcolor import palette_builder
from numpy import int64, random
from numpy.typing import NDArray
from PIL import Image, ImageDraw
from scipy.spatial import Voronoi

from .fcolor import palette_builder

CENTERED = True
UNCENTERED = False


def backing(
    width: int,
    height: int,
    seed_color: tuple[int, int, int],
    palette_function: Callable[
        [float, float, float, float], tuple[float, float, float]
    ],
    from_center: bool = CENTERED,
) -> Image.Image:
    """Returns Voronoi image from dimensions, seed_color and palette_function"""
    x_offset = width // 5
    y_offset = height // 5
    x_limit = width + x_offset * 2
    y_limit = height + y_offset * 2

    points = np.array(
        list(
            zip(
                random.randint(0, x_limit, size=(100)),
                random.randint(0, y_limit, size=(100)),
            )
        )
    )
    image = Image.new("RGBA", (x_limit, y_limit), "white")

    return voronoi_generator(
        points,
        image,
        (x_offset, y_offset, width, height),
        seed_color,
        palette_function,
        from_center,
    )


def voronoi_generator(
    points: NDArray[int64],
    image: Image.Image,
    bbox: tuple[int, int, int, int],
    seed_color: tuple[int, int, int],
    palette_function: Callable[
        [float, float, float, float], tuple[float, float, float]
    ],
    from_center: bool,
):
    """Voronoi is organic looking cells coloured in a specific manner"""
    voronoi = Voronoi(points)
    draw = ImageDraw.Draw(image)

    cells = voronoi.regions
    colors = palette_builder(len(cells), palette_function, from_center)
    palette = colors(*seed_color)

    for num, cell in enumerate(cells):
        if len(cell) > 0 and -1 not in cell:
            polygon = [tuple(voronoi.vertices[index]) for index in cell]
            if from_center:
                centroid = np.mean(polygon, axis=0)
                min_distance = min(
                    centroid[0],
                    centroid[1],
                    image.width - centroid[0],
                    image.height - centroid[1],
                )

                try:
                    num = int(min_distance % num)
                except ValueError:
                    num = 0

            draw.polygon(polygon, fill=palette[num])

    return image.crop(bbox)
