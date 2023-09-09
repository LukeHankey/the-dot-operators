import pygame
import pygame_gui
from pygame.locals import QUIT

from constants import screen, WHITE, BLUE, WIDTH, HEIGHT, manager, font


def custom_game_view():
    global fullscreen
    screen.fill(WHITE)
    title = font.render("Custom Game", True, BLUE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    custom_game_panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((50, 50), (WIDTH - 200 - 50, HEIGHT - 50)),
        manager=manager
    )

    shape_option = pygame_gui.elements.UISelectionList(pygame.Rect(50, 50, 200, 46),
                                                       ['Triangle', 'Square'],
                                                       manager=manager,
                                                       container=custom_game_panel)
    start_game_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 150), (200, 50)),
        text="Start Game",
        manager=manager,
        container=custom_game_panel
    )
    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 210), (200, 50)),
        text="Back",
        manager=manager,
        container=custom_game_panel
    )

    selected_shape = None

    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == QUIT:
                return {"type": "quit"}
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_game_button:
                    custom_game_panel.hide()
                    return {"type": "play_game", "selected_shape": selected_shape}
                if event.ui_element == back_button:
                    custom_game_panel.hide()
                    return {"type": "menu"}
            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == shape_option:
                    selected_shape = shape_option.get_single_selection()

            manager.process_events(event)

        manager.update(time_delta)
        screen.fill(WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        manager.draw_ui(screen)

        pygame.display.update()

