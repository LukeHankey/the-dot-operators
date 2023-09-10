import random
from typing import Literal, NoReturn

import pygame_gui
from client.constants import HEIGHT, WHITE, WIDTH, manager, screen
from client.credits_view import CreditsView
from client.settings_view import SettingsView
from pygame import Rect, display, draw, event, init, quit, time
from pygame.event import Event
from pygame.locals import QUIT, USEREVENT
from tessellation import generate_tiles
from utils import get_image, tile_scrambler

from .game import GameClient

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

MAX_OVERLAP = 0.25
MIN_OVERLAP = 0.15
DEFAULT_OVERLAP = 0.25

MIN_TILE_NUMBER = 16
DEFAULT_TILE_NUMBER = 36

init()


class Menu:
    """Menu view and controller"""

    def __init__(self, filename):
        self.view_instances = {
            "settings": SettingsView(),
            "credits": CreditsView(),
            "play_game": PlayGameView(filename),
        }
        self.active_view = self
        self.clock = time.Clock()
        self.build()

    def build(self) -> None:
        """Builds the menu's layout"""
        button_size = (100, 50)
        right_edge = WIDTH - button_size[0]

        count = 83
        MODES = ["quick", "secret", "settings", "credits"]

        for mode in MODES:
            rectangle = Rect((right_edge - 50, count), button_size)
            button = pygame_gui.elements.UIButton(
                relative_rect=rectangle, text=mode.title(), manager=manager
            )
            count += 83
            setattr(self, f"{mode}_button", button)

        self.right_panel = pygame_gui.elements.UIPanel(
            relative_rect=Rect((WIDTH - 200, 0), (200, HEIGHT)),
            starting_height=0,
            manager=manager,
        )

    def draw_completion_bar(
        self,
        completion_percent: float,
        position: tuple[int, int],
        size: tuple[int, int],
    ) -> None:
        """Draws a completion bar on the screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
            completion_percent (float): The completion percentage (0.0.to 1.0)
            position (tuple): (x,y) position ef the top-left corner of the bar.
            size (tuple): (width, height) of the bar.
        """
        border_color = (0, 0, 0)
        fill_color = (0, 255, 0)

        draw.rect(screen, border_color, position + size, 2)

        fill_width = int(size[0] * completion_percent)
        draw.rect(screen, fill_color, (position[0], position[1], fill_width, size[1]))

    def event_handler(self, e: Event) -> Literal[True]:
        """Event handler for the menu"""
        if e.type == QUIT:
            quit()
        if e.type == USEREVENT:
            if e.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if e.ui_element == self.quick_button:
                    self.view_instances["play_game"].num_of_tiles = MIN_TILE_NUMBER
                    self.active_view = self.view_instances["play_game"]
                if e.ui_element == self.secret_button:
                    self.view_instances["play_game"].num_of_tiles = DEFAULT_TILE_NUMBER
                    self.active_view = self.view_instances["play_game"]
                if e.ui_element == self.settings_button:
                    self.active_view = self.view_instances["settings"]
                if e.ui_element == self.credits_button:
                    self.active_view = self.view_instances["credits"]
                self.active_view.show()
        return True

    def mainloop(self) -> NoReturn:
        """Main loop for the menu"""
        while True:
            screen.fill(WHITE)
            time_delta = self.clock.tick(60) / 1000.0
            for e in event.get():
                if not self.active_view.event_handler(e):
                    self.active_view.hide()
                    self.active_view = self
                manager.process_events(e)
            manager.draw_ui(screen)
            manager.update(time_delta)
            display.update()
            display.flip()


def hamming_distance(current_positions: list[int], correct_positions: list[int]) -> int:
    """Calculate the Hamming distance between the current puzzle positions and the correct positions."""
    return sum(
        current != correct
        for current, correct in zip(current_positions, correct_positions)
    )


def simulate_tile_positions(total_tiles: int) -> list[int]:
    """Simulate random tile position to produce random Hamming distance"""
    return random.sample(range(total_tiles), total_tiles)


class PlayGameView:
    """Intermediary "view" before launching game"""

    def __init__(self, filename):
        self.filename = filename
        self.num_of_tiles = None

    def event_handler(self, _):
        """For compatibility purposes"""
        return True

    def show(self):
        """Bad name (for compatibility purposes), starts the game"""
        image = get_image(self.filename, SCREEN_DIMENSIONS, self.num_of_tiles)
        correct_tiles = generate_tiles(image, self.num_of_tiles)

        action = {
            "num_of_tiles": self.num_of_tiles,
            "image": image,
            "overlap": DEFAULT_OVERLAP,
            "solved_tiles": correct_tiles,
            "scrambled_tiles": tile_scrambler(correct_tiles),
        }
        game = GameClient(action)
        game.mainloop()
