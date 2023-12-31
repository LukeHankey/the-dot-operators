import pygame_gui
from pygame import Rect, font
from pygame.event import Event
from pygame.locals import QUIT, USEREVENT

from .constants import BLUE, HEIGHT, WHITE, WIDTH, manager, screen


class CreditsView:
    """Credits view"""

    def __init__(self) -> None:
        self.title_font = font.Font(None, 48)

        self.title = self.title_font.render("Jigsaw Game", True, BLUE)
        self.contributors = [
            "@LukeHankey LukeHankey Luke",
            "@busterbeam busterbeam Nathan Lloyd",
            "@EarthKiii EarthKiii Jonas Charrier",
            "@DavidStrootman DavidStrootman David Strootman",
            "@bartoszkobylinski Bartosz Kobylinski",
            "@chuchumuru Pilogic",
            "Version 0.1.0",
        ]
        self.build()

    def build(self):
        """Builds the view's layout"""
        screen.fill(WHITE)

        # Center title in available space
        title_x = (WIDTH - 200) // 2 - self.title.get_width() // 2
        screen.blit(self.title, (title_x, 50))

        self.credit_text_box = pygame_gui.elements.UITextBox(
            relative_rect=Rect((WIDTH // 2 - 160, 70), (320, 200)),
            manager=manager,
            html_text=f"<font color='#FFFFFF'>{'<br>'.join(self.contributors)}</body>",
        )

        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=Rect((WIDTH // 2 - 50, HEIGHT // 2 + 60), (100, 50)),
            text="Back",
            manager=manager,
        )

        self.hide()

    def event_handler(self, e: Event) -> bool:
        """Event handler for the view"""
        if e.type == QUIT:
            quit()
        if e.type == USEREVENT:
            if e.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if e.ui_element == self.back_button:
                    return False
        return True

    def show(self) -> None:
        """Shows the view"""
        self.credit_text_box.show()
        self.back_button.show()

    def hide(self) -> None:
        """Hides the view"""
        self.credit_text_box.hide()
        self.back_button.hide()
