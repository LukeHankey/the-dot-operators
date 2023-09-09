import pygame.event
import pygame_gui.elements
from pygame import QUIT

from constants import screen, WHITE, RED, BLUE, font, WIDTH, HEIGHT, manager

#  Create a GUI components
'''
game_settings_panel = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect((50, 50), (350, 500)),
    starting_height=1,
    manager=manager
)
image_settings_panel = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect((400, 50), (350, 500)),
    starting_height=1,
    manager=manager,
)

# UI elements for the game_settings_panel

overlap_sensitivity_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((100, 100), (200, 20)),
    start_value=0.15,
    value_range=(0.15, 0.25),
    manager=manager,
    container=game_settings_panel
)
checkbox = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((100, 150), (200, 50)),
    text="Fullscreen",
    manager=manager,
    container=game_settings_panel
)
# UI elements for the image_settings_panel

image_api_options_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 50), (250, 50)),
    text="Image API Options",
    manager=manager,
    container=image_settings_panel
)
directory_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 110), (250, 50)),
    text="Upload from directory",
    manager=manager,
    container=image_settings_panel
)

back_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((100, 350), (100, 50)),
    text="Back",
    manager=manager
)

'''


def settings_view():
    screen.fill(WHITE)
    title = font.render("Settings", True, BLUE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    '''
    game_settings_panel.show()
    image_settings_panel.show()
    '''
    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == QUIT:
                return {"type": "quit"}
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    # if event.ui_element == back_button:
                    # 0    game_settings_panel.hide()
                    #   image_settings_panel.hide()
                    return {"type": "menu"}

            manager.process_events(event)

        manager.update(time_delta)

        screen.fill(WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        manager.draw_ui(screen)

        pygame.display.update()