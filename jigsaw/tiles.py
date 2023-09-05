from collections.abc import Generator

from PIL.Image import Image, new
from PIL.ImageDraw import Draw
from pygame import image, sprite


class Tile(sprite.Sprite):
    """Tile which is a cropped image at a specifc point.

    dragging support is built in TODO; add support for alpha, better
    bounding box methods
    """

    def __init__(self, pos: tuple[int, int], cropped_image: Image) -> None:
        """Basic init method that takes pillow image into pygame image"""
        super().__init__()
        self.image = image.fromstring(
            cropped_image.tobytes(), cropped_image.size, cropped_image.mode
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.active = False
        self.drag_offset: tuple[int, int]

    def activate(self, pointer: tuple[int, int]) -> None:
        """Could add tile highlighting and other affects"""
        self.active = True
        self.drag_offset = (
            pointer[0] - self.rect.topleft[0],
            pointer[1] - self.rect.topleft[1],
        )

    def deactivate(self) -> None:
        """Remove anything `activate` added"""
        self.active = False
        self.drag_offset = (0, 0)  # so move can be used more directly

    def move(self, pointer: tuple[int, int]) -> None:
        """Move tile to pointer could be a mouse pointer or anything"""
        self.rect.topleft = (
            pointer[0] - self.drag_offset[0],
            pointer[1] - self.drag_offset[1],
        )

    def snap_h(self, side: int, h_coord: int) -> None:
        """Snaps the tile to other tiles/image borders on the horizontal axis"""
        match side:
            case 0:
                self.rect.midleft = (h_coord, self.rect.midleft[1])
            case 1:
                self.rect.midright = (h_coord, self.rect.midright[1])

    def snap_v(self, side: int, v_coord: int) -> None:
        """Snaps the tile to other tiles/image borders on the vertical axis"""
        match side:
            case 1:
                self.rect.midbottom = (self.rect.midbottom[0], v_coord)
            case 0:
                self.rect.midtop = (self.rect.midtop[0], v_coord)


def trianglular_tiles(
    image: Image, width: int, height: int
) -> Generator[tuple[tuple[int, int], Image], None, None]:
    """Tile generator with the inner most loop calling the specific

    shape for tiling applies the mask of the shape then continues
    """
    for x in range(0, image.width, width):
        for y in range(0, image.height, height):
            mask = new("L", (width, height), 0)
            draw = Draw(mask)
            draw.polygon([(0, 0), (0, height), (width, height)], fill=255)
            tile = image.crop((x, y, x + width, y + height))
            tile.putalpha(mask)
            yield (x, y), tile  # first yield for half the triangle

            mask = new("L", (width, height), 0)
            draw = Draw(mask)
            draw.polygon([(0, 0), (width, 0), (width, height)], fill=255)
            tile = image.crop((x, y, x + width, y + height))
            tile.putalpha(mask)
            yield (x, y), tile  # second yield for the other half


def square_tiles(
    image: Image, width: int, height: int
) -> Generator[tuple[tuple[int, int], Image], None, None]:
    """Tile generator with the inner most loop calling the specific

    shape for tiling applies the mask of the shape then continues
    """
    for x in range(0, image.width, width):
        for y in range(0, image.height, height):
            yield (x, y), image.crop((x, y, x + width, y + height))
