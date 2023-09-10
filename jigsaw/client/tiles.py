from typing import Literal

from PIL.Image import Image
from pygame import image, sprite


class Tile(sprite.Sprite):
    """Tile which is a cropped image at a specifc point.

    dragging support is built in TODO; add support for alpha, better
    bounding box methods
    """

    def __init__(
        self: sprite.Sprite,
        pos: tuple[int, int],
        overlap: float,
        tile: tuple[tuple[int, int], Image],
    ) -> None:
        """Basic init method that takes pillow image into pygame image"""
        super().__init__()
        self.image = image.fromstring(tile[1].tobytes(), tile[1].size, tile[1].mode)
        self.correct_position = tile[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.active = False
        self.drag_offset: tuple[int, int]
        self.snapping_rect = (self.rect.size[0] * overlap, self.rect.size[1] * overlap)

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

    def snap(self, side: str, coord: int, axis: int) -> Literal[True]:
        """Snaps the tile to other tiles/image borders on the horizontal axis"""
        tmp_coord = list(getattr(self.rect, side))
        tmp_coord[axis] = coord
        setattr(self.rect, side, tuple(tmp_coord))
        return True


class JigSawTiles(sprite.Group):
    """Inheritance for the addition of Group methods concerning active tiles"""

    def get_active(self) -> Tile | None:
        """Return the active tile"""
        for tile in self.sprites()[::-1]:
            if tile.active:
                return tile
        return None

    def get_inactives(self) -> list[Tile]:
        """Return the inactive tiles"""
        return [tile for tile in self.sprites() if not tile.active]
