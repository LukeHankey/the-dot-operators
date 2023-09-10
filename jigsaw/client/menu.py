import random

import pygame_gui
from pygame import init, draw, Rect, display, time, event, quit
from pygame.locals import QUIT, USEREVENT

from client.constants import WHITE, BLUE, WIDTH, HEIGHT, screen, font, manager
from client.credits_view import CreditsView
from client.settings_view import SettingsView

init()

'''
# Colors

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 36)  # Default font, size 36
overlap_sensitivity = 5

pygame.display.set_caption('Game Menu')

'''


class PlayGameView:
    pass

class Menu:
    def __init__(self):
        self.view_instances = {
            "settings": SettingsView(),
            "credits": CreditsView(),
            "play_game": PlayGameView(),
        }
        self.active_view = self
        self.clock = time.Clock()
        self.build()

    def build(self):
        button_size = (100, 50)
        right_edge = WIDTH - button_size[0]
        count = 83
        MODES = ["quick", "secret", "settings", "credits"]
        for mode in MODES:
            rectangle = Rect((right_edge - 50, count), button_size)
            button = pygame_gui.elements.UIButton(
                relative_rect=rectangle, text=mode.title(), manager=manager)
            count += 83
            setattr(self, f"{mode}_button", button)

        self.right_panel = pygame_gui.elements.UIPanel(
            relative_rect=Rect((WIDTH - 200, 0), (200, HEIGHT)),
            starting_height=0,
            manager=manager
        )

    def draw_completion_bar(self, completion_percent, position, size):
        """ Draws a completion bar on the screen.
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

    def event_handler(self, e):
        if e.type == QUIT:
            quit()
        if e.type == USEREVENT:
            if e.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if e.ui_element == self.quick_button:
                    self.active_view = self.view_instances["play_game"]
                if e.ui_element == self.secret_button:
                    self.active_view = self.view_instances["play_game"]
                if e.ui_element == self.settings_button:
                    self.active_view = self.view_instances["settings"]
                    self.active_view.show()
                if e.ui_element == self.credits_button:
                    self.active_view = self.view_instances["credits"]
                    self.active_view.show()
        return True

    def mainloop(self):
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


def hamming_distance(current_positions, correct_positions):
    """Calculate the Hamming distance between the current puzzle positions and the correct positions."""
    return sum(current != correct for current, correct in zip(current_positions, correct_positions))


def simulate_tile_positions(total_tiles):
    """
    Simulate random tile position to produce random Hamming distance
    """
    return random.sample(range(total_tiles), total_tiles)


# Views

def play_game(difficulty):
    screen.fill(WHITE)
    message = f"You choose {difficulty} mode!"
    txt = font.render(message, True, BLUE)

    screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - txt.get_height() // 2))
    display.flip()
    time.wait(2000)

    total_tiles = 9
    solution_tiles_positions = list(range(total_tiles))
    clock = time.Clock()
    counter = 0

    completion_bar = pygame_gui.elements.UIProgressBar(relative_rect=Rect((50, 500, 700, 20)),
                                                       manager=manager)

    while True:
        time_delta = clock.tick(60) / 1000.0
        for e in event.get():
            if e.type == QUIT:
                return {"type": "quit"}
            manager.process_events(e)

        # Every 3 seconds, simulate a new tile position to change the completion percentage
        if counter % 90 == 0:
            tiles_positions = simulate_tile_positions(total_tiles)
        counter += 1

        # Calculate completion based on Hamming distance
        distance = hamming_distance(tiles_positions, solution_tiles_positions)
        completion_percent = 1 - (distance / len(tiles_positions))

        completion_bar.set_current_progress(completion_percent * 100)

        manager.update(time_delta=time_delta)

        # Clear the screen for fresh drawing
        screen.fill(WHITE)
        manager.draw_ui(screen)

        display.flip()
        clock.tick(30)  # Run the loop at 30 FPS
