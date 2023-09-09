import os
import sys
import pygame
import pygame_gui
from pygame import QUIT
import tkinter as tk
from tkinter import filedialog
from constants import screen, WHITE, BLUE, font, WIDTH, HEIGHT, manager

fullscreen = False

def open_file_dialog():
    if sys.platform in ['linux', 'darwin']:
        return os.popen('zenity --file-selection').read().strip()
    elif sys.platform == 'win32':
        root = tk.Tk()
        root.withdraw()
        return filedialog.askopenfilename()

def settings_view():
    global fullscreen
    screen.fill(WHITE)
    title = font.render("Settings", True, BLUE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    settings_panel = pygame_gui.elements.UIPanel(
        relative_rect=pygame.Rect((50, 50), (WIDTH - 200 - 50, HEIGHT - 50)),
        starting_height=0,
        manager=manager
    )

    fullscreen_button = pygame_gui.elements.UIButton(pygame.Rect(50, 50, 200, 50),
                                                     'Fullscreen' if not fullscreen else "Windowed", manager=manager,
                                                     container=settings_panel)
    open_file_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 250), (200, 50)),
        text="Open File",
        manager=manager,
        container=settings_panel
    )
    api_image_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50, 310), (200, 50)),
        text="API Image",
        manager=manager,
        container=settings_panel
    )

    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((settings_panel.rect.width // 2 - 50, settings_panel.rect.height - 70), (100, 50)),
        text="Back",
        manager=manager,
        container=settings_panel
    )

    selected_shape = None
    selected_file = None

    clock = pygame.time.Clock()
    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == QUIT:
                return {"type": "quit"}
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == fullscreen_button:
                    fullscreen = not fullscreen
                    fullscreen_button.set_text("Fullscreen" if not fullscreen else "Windowed")
                if event.ui_element == open_file_button:
                    selected_file = open_file_dialog()
                    if selected_file:

                        print(f"File selected: {selected_file}")

                if event.ui_element == back_button:
                    settings_panel.hide()
                    return {'type': 'menu', 'selected_file': selected_file, 'fullscreen': fullscreen}

            manager.process_events(event)

        manager.update(time_delta)
        screen.fill(WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
        manager.draw_ui(screen)

        pygame.display.update()
