from pygame import Rect, Surface


class JigSaw(Surface):
    """This is the Surface that the user interacts with the puzzle"""

    def __init__(self, screen: Surface, size: tuple[int, int]) -> None:
        """Set Jigsaw position"""
        super().__init__(size)
        self.screen = screen
        self.size = size
        self.set_bounds()

    def set_bounds(self) -> None:
        """Called to set the real surface coords"""
        screen_bounds = self.screen.get_rect()
        surface_bounds = self.get_rect()

        x_offset = (screen_bounds.width - surface_bounds.width) // 2
        y_offset = (screen_bounds.height - surface_bounds.height) // 2

        self.rect = Rect(
            x_offset, y_offset, self.size[0] + x_offset, self.size[1] + y_offset
        )
        self.center = (x_offset, y_offset)

    def translate(self, position: tuple[int, int]) -> tuple[int, int]:
        """Adjust screen coordinates to jigsaw surface coordinates"""
        return position[0] - self.rect.topleft[0], position[1] - self.rect.topleft[1]
