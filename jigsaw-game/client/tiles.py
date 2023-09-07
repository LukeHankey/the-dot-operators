from pygame import image, sprite


class JigSawTiles(sprite.Group):
    """Inheritance for the addition of Group methods concerning active tiles"""

    def get_active(self):
        """Return the active tile"""
        for tile in self.sprites()[::-1]:
            if tile.active:
                return tile
        return False

    def get_inactives(self):
        """Return the inactive tiles"""
        return [tile for tile in self.sprites() if not tile.active]


class Tile(sprite.Sprite):
    """Tile which is a cropped image at a specifc point.

    dragging support is built in TODO; add support for alpha, better
    bounding box methods
    """

    def __init__(self, pos: tuple[int, int], cropped_image):
        """Basic init method that takes pillow image into pygame image"""
        super().__init__()
        self.image = image.fromstring(
            cropped_image.tobytes(), cropped_image.size, cropped_image.mode
        )
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.active = False
        self.drag_offset: tuple[int, int]
        self.snapping_rect = (self.rect.size[0] * 0.15, self.rect.size[1] * 0.15)

    def activate(self, pointer: tuple[int, int]):
        """Could add tile highlighting and other affects"""
        self.active = True
        self.drag_offset = (
            pointer[0] - self.rect.topleft[0],
            pointer[1] - self.rect.topleft[1],
        )

    def deactivate(self):
        """Remove anything `activate` added"""
        self.active = False
        self.drag_offset = (0, 0)  # so move can be used more directly

    def move(self, pointer: tuple[int, int]):
        """Move tile to pointer could be a mouse pointer or anything"""
        self.rect.topleft = (
            pointer[0] - self.drag_offset[0],
            pointer[1] - self.drag_offset[1],
        )

    def snap(self, side: str, coord: int, axis: int):
        """Snaps the tile to other tiles/image borders on the horizontal axis"""
        if side == "topleft":
            tmp_coord = list(self.rect.topleft)
            tmp_coord[axis] = coord
            self.rect.topleft = tuple(tmp_coord)
        else:
            tmp_coord = list(self.rect.bottomright)
            tmp_coord[axis] = coord
            self.rect.bottomright = tuple(tmp_coord)