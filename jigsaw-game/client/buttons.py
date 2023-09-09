import pygame
import pygame_gui
from constants import HEIGHT, WIDTH

button_width = 100
button_height = 50
right_edge = WIDTH - button_width


def create_buttons(manager):

    easy_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((right_edge - 50, 83), (button_width, button_height)),
        text="Easy",
        manager=manager
    )
    medium_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((right_edge - 50, 166), (button_width, button_height)),
        text="Medium",
        manager=manager
    )
    hard_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((right_edge - 50, 249), (button_width, button_height)),
        text="Hard",
        manager=manager
    )
    scoreboard_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((right_edge - 50, 332), (button_width, button_height)),
        text="Scoreboard",
        manager=manager
    )
    settings_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((right_edge - 50, 415), (button_width, button_height)),
        text="Settings",
        manager=manager
    )
    credits_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((right_edge - 50, 498), (button_width, button_height)),
        text="Credits",
        manager=manager
    )
    right_panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((WIDTH - 200, 0), (200, HEIGHT)),
        starting_height=0,
        manager=manager
    )
    return easy_button, medium_button, hard_button, scoreboard_button, settings_button, right_panel, credits_button
