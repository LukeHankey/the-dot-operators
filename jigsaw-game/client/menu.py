import random
import pygame
import pygame_gui
from pygame.locals import QUIT, MOUSEBUTTONDOWN
from settings_view import settings_view
from constants import WHITE, RED, BLUE, WIDTH, HEIGHT, screen, font, manager
from credits_view import credits_view
from buttons import create_buttons

pygame.init()

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

easy_button, medium_button, hard_button, scoreboard_button, settings_button, right_panel, credits_button = create_buttons(
    manager)


def draw_button(surface, rect, text, button_color, text_color):
    pygame.draw.rect(surface, button_color, rect)
    txt = font.render(text, True, text_color)
    txt_pos = (rect.x + rect.width // 2 - txt.get_width() // 2, rect.y + rect.height // 2 - txt.get_height() // 2)
    surface.blit(txt, txt_pos)


def is_button_clicked(event, rect):
    if event.type == MOUSEBUTTONDOWN:
        return rect.collidepoint(event.pos)
    return False


def hamming_distance(current_positions, correct_positions):
    """Calculate the Hamming distance between the current puzzle positions and the correct positions."""
    return sum(current != correct for current, correct in zip(current_positions, correct_positions))


def draw_completion_bar(screen, completion_percent, position, size):
    """ Draws a completion bar on the screen.
    Args:
        screen (pygame.Surface): The surface to draw on.
        completion_percent (float): The completion percentage (0.0.to 1.0)
        position (tuple): (x,y) position ef the top-left corner of the bar.
        size (tuple): (width, height) of the bar.
    """
    border_color = (0, 0, 0)
    fill_color = (0, 255, 0)

    pygame.draw.rect(screen, border_color, position + size, 2)

    fill_width = int(size[0] * completion_percent)
    pygame.draw.rect(screen, fill_color, (position[0], position[1], fill_width, size[1]))


def draw_slider(screen, rect, value, min_value, max_value):
    """Draws a slider on the screen"""
    border_color = (0, 0, 0)
    fill_color = (0, 255, 0)
    handle_color = (255, 0, 0)
    pygame.draw.rect(screen, border_color, rect, 2)
    fill_width = int(rect.width * ((value - min_value) / (max_value - min_value)))
    pygame.draw.rect(screen, fill_color, (rect.x, rect.y, fill_width, rect.height))
    handle_x = rect.x + fill_width - 5
    pygame.draw.rect(screen, handle_color, (handle_x, rect.y, 10, rect.height))


def tile_overlap_settings_view():
    global overlap_sensitivity
    screen.fill(WHITE)

    slider_rect = pygame.Rect(100, 100, 200, 20)
    back_button = pygame.Rect(100, 200, 200, 50)

    draw_slider(screen, slider_rect, overlap_sensitivity, 0.15, 0.25)
    draw_button(screen, back_button, "Back", RED, BLUE)


def simulate_tile_positions(total_tiles):
    """
    Simulate random tile position to produce random Hamming distance
    """
    return random.sample(range(total_tiles), total_tiles)


# Views
def game_selection_view():
    screen.fill(WHITE)

    easy_button = pygame.Rect(100, 100, 200, 50)
    moderate_button = pygame.Rect(100, 200, 200, 50)
    hard_button = pygame.Rect(100, 300, 200, 50)

    draw_button(screen, easy_button, "Easy", RED, BLUE)
    draw_button(screen, moderate_button, "Moderate", RED, BLUE)
    draw_button(screen, hard_button, "Hard", RED, BLUE)

    for event in pygame.event.get():
        if event.type == QUIT:
            return {"type": "quit"}
        elif is_button_clicked(event, easy_button):
            return {"type": "play_game", "difficulty": "easy"}
        elif is_button_clicked(event, moderate_button):
            return {"type": "play_game", "difficulty": "moderate"}
        elif is_button_clicked(event, hard_button):
            return {"type": "play_game", "difficulty": "hard"}

    return {"type": "game_selection"}


def play_game(difficulty):
    screen.fill(WHITE)
    message = f"You choose {difficulty} mode!"
    txt = font.render(message, True, BLUE)

    screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, HEIGHT // 2 - txt.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

    total_tiles = 9
    solution_tiles_positions = list(range(total_tiles))
    clock = pygame.time.Clock()
    counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return {"type": "quit"}

        # Every 3 seconds, simulate a new tile position to change the completion percentage
        if counter % 90 == 0:
            tiles_positions = simulate_tile_positions(total_tiles)
        counter += 1

        # Calculate completion based on Hamming distance
        distance = hamming_distance(tiles_positions, solution_tiles_positions)
        completion_percent = 1 - (distance / len(tiles_positions))

        # Clear the screen for fresh drawing
        screen.fill(WHITE)

        # Draw the completion bar
        bar_position = (50, 500)
        bar_size = (700, 20)
        draw_completion_bar(screen, completion_percent, bar_position, bar_size)

        pygame.display.flip()
        clock.tick(30)  # Run the loop at 30 FPS


def menu_view():
    screen.fill(WHITE)

    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == QUIT:
                return {"type": "quit"}
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == easy_button:
                        return {"type": "play_game", "difficulty": "easy"}
                    if event.ui_element == medium_button:
                        return {"type": "play_game", "difficulty": "medium"}
                    if event.ui_element == hard_button:
                        return {"type": "play_game", "difficulty": "hard"}
                    if event.ui_element == settings_button:
                        return {"type": "settings"}
                    if event.ui_element == credits_button:
                        return {"type": "credits"}

            manager.process_events(event)

        manager.update(time_delta)

        screen.fill(WHITE)
        manager.draw_ui(screen)

        pygame.display.update()


# Main loop
def menu():
    current_view = "menu"
    current_difficulty = None
    view_functions = {
        "menu": menu_view,
        "game_selection": game_selection_view,
        "settings": settings_view,
        "credits": credits_view,
    }

    while True:
        if current_view == "play_game":
            action = play_game(current_difficulty)
        else:
            action = view_functions[current_view]()

        if action["type"] == "quit":
            break
        elif action["type"] == "play_game":
            current_difficulty = action['difficulty']
            current_view = action['type']
        elif action["type"] in view_functions:
            current_view = action["type"]

        pygame.display.flip()

    pygame.quit()


