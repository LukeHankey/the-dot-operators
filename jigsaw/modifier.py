import numpy as np
from numpy import random
from PIL import Image, ImageDraw
from scipy.spatial import Voronoi


def voronoi_generator(width: int height: int):
    random.seed(0)
    points = array(list(zip(
        random.randint(0, width),
        random.randint(0, height))))
    boundary_points = np.array([
        [1, 1], [1, height - 1], [width - 1, 1], [width - 1, height - 1]])
    points = np.concatenate((points, boundary_points), axis=0)
    voronoi = Voronoi(points)
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    # Step 4: Iterate through Voronoi regions and fill them with colors
    color = lambda: (
        random.randint(0, 256),
        random.randint(0, 256),
        random.randint(0, 256))
    for region in voronoi.regions:
        if len(region) > 0:  # and -1 not in region:
            polygon = [tuple(voronoi.vertices[i]) for i in region]
            draw.polygon(polygon, fill=color())
    img.show()
