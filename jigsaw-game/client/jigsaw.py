from .tiles import Tile, JigSawTiles
from pygame import Rect, Surface

TOP = BOTTOM = 1
LEFT = RIGHT = 0


class JigSaw(Surface):
    """This is the Surface that the user interacts with the puzzle"""

    def __init__(self, screen: Surface, size: tuple[int, int]) -> None:
        """Set Jigsaw position"""
        super(JigSaw, self).__init__(size)
        self.screen = screen
        self.size = size
        self.set_bounds()

    def set_bounds(self):
        """Called to set the real surface coords"""
        screen_bounds = self.screen.get_rect()
        surface_bounds = self.get_rect()
        x_offset = (screen_bounds.width - surface_bounds.width) // 2
        y_offset = (screen_bounds.height - surface_bounds.height) // 2
        self.rect = Rect(
            x_offset, y_offset, self.size[0] + x_offset, self.size[1] + y_offset
        )
        self.center = (x_offset, y_offset)

    def translate(self, position: tuple[int, int]):
        """Adjust screen coordinates to jigsaw surface coordinates"""
        offset = (
            position[0] - self.rect.topleft[0],
            position[1] - self.rect.topleft[1],
        )
        return offset

    def border_check_snap(self, side: int, tile: "client.Tile"):
        """Checks if the tile can be snapped to the game border and snaps it if it can"""
        if tile.rect.topleft[side] < tile.snapping_rect[side]:
            return tile.snap("topleft", 0, side)
        elif tile.rect.bottomright[side] > (self.size[side] - tile.snapping_rect[side]):
            return tile.snap("bottomright", self.size[side], side)
        return False

    @staticmethod
    def tile_check_snap(side: int, tile: "client.Tile", check_tile: "client.Tile"):
        """Checks if the tile can be snapped to the check_tile and snaps it if it can"""
        topleft_snap = abs(check_tile.rect.bottomright[side] - tile.rect.topleft[side])
        bottomright_snap = abs(
            check_tile.rect.topleft[side] - tile.rect.bottomright[side]
        )
        if topleft_snap < bottomright_snap and topleft_snap <= tile.snapping_rect[side]:
            return tile.snap("topleft", check_tile.rect.bottomright[side], side)
        elif bottomright_snap <= tile.snapping_rect[side]:
            return tile.snap("bottomright", check_tile.rect.topleft[side], side)
        return False

    def mouse_down(self, tiles: "client.JigSawTiles", mouse_position: tuple[int, int]):
        """Handler for if mouse press down in jigsaw surface"""
        # [::-1] reverse list check is downwards in z depth
        for tile in tiles.sprites()[::-1]:
            if tile.rect.collidepoint(self.translate(mouse_position)):
                # reorder to the top before drag
                tiles.remove(tile)
                tiles.add(tile)  # reorder to top
                tile.activate(mouse_position)
                break
        return tiles

    def mouse_up(self, tiles: "client.JigSawTiles", mouse_position: tuple[int, int]):
        """Handler for if mouse press release in jigsaw surface"""
        active_tile = tiles.get_active()

        h_snapped = self.border_check_snap(LEFT, active_tile)
        if not h_snapped:
            h_snapped = self.border_check_snap(RIGHT, active_tile)

        v_snapped = self.border_check_snap(TOP, active_tile)
        if not v_snapped:
            v_snapped = self.border_check_snap(BOTTOM, active_tile)

        for check_tile in tiles.get_inactives():
            # if the tile has been snapped on the 2 axis, no need to check the other tiles
            if v_snapped and h_snapped:
                return active_tile.deactivate()
            if not h_snapped:
                h_snapped = self.tile_check_snap(LEFT, active_tile, check_tile)
                if not h_snapped:
                    h_snapped = self.tile_check_snap(RIGHT, active_tile, check_tile)
            if not v_snapped:
                v_snapped = self.tile_check_snap(TOP, active_tile, check_tile)
                if not v_snapped:
                    v_snapped = self.tile_check_snap(BOTTOM, active_tile, check_tile)
        active_tile.deactivate()

    @staticmethod
    def mouse_motion(tiles: "client.JigSawTiles", mouse_position: tuple[int, int]):
        """Handler for if mouse moving on jigsaw surface"""
        for tile in tiles.sprites()[::-1]:
            if tile.active:
                tile.move(mouse_position)
        return tiles
