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


def draw_button(surface, rect, text, button_color, text_color):
    pygame.draw.rect(surface, button_color, rect)
    txt = font.render(text, True, text_color)
    txt_pos = (rect.x + rect.width // 2 - txt.get_width() // 2, rect.y + rect.height // 2 - txt.get_height() // 2)
    surface.blit(txt, txt_pos)


def is_button_clicked(event, rect):
    if event.type == MOUSEBUTTONDOWN:
        return rect.collidepoint(event.pos)
    return False


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
    return {"type": "menu"}


def menu_view():
    screen.fill(WHITE)
    game_selection_button = pygame.Rect(100, 100, 200, 50)
    draw_button(screen, game_selection_button, "Game Selection", RED, BLUE)

    for event in pygame.event.get():
        if event.type == QUIT:
            return {"type": "quit"}
        if is_button_clicked(event, game_selection_button):
            return {"type": "game_selection"}

    return {"type": "menu"}


# Main loop
def menu():
    current_view = "menu"
    current_difficulty = None
    view_functions = {
        "menu": menu_view,
        "game_selection": game_selection_view,
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
    return action

if __name__ == "__main__":
    print(menu())
