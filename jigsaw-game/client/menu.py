import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

pygame.init()

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game Menu')

font = pygame.font.SysFont(None, 36)  # Default font, size 36


class BaseView(pygame.Surface):
    """Base view that acts as a template for all game views."""

    def __init__(self, width, height):
        """Initialize the base view with given dimensions."""
        super().__init__((width, height))

    def draw(self):
        """Draw the view elements on the screen"""
        pass

    def handle_event(self, event):
        """Handle the given element"""
        pass


class GameSelectionView(BaseView):
    """View for the selection screen."""

    pass


class MenuView(BaseView):
    """Main menu view"""

    def draw(self):
        """Draw the menu elements on the screen."""
        self.fill(WHITE)
        pygame.draw.rect(self, RED, (100, 100, 200, 50))
        game_selection_text = font.render("Game Selection", True, BLUE)
        self.blit(game_selection_text, (
            150 - game_selection_text.get_width() // 2 + 50, 125 - game_selection_text.get_height() // 2))

    def handle_event(self, event):
        """Handle menu interactions."""
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            if 100 < x < 300 and 100 < y < 150:
                return GameSelectionView(WIDTH, HEIGHT)
        return self


current_view = MenuView(WIDTH, HEIGHT)

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        current_view = current_view.handle_event(event)

    current_view.draw()
    screen.blit(current_view, (0, 0))
    pygame.display.flip()

pygame.quit()
