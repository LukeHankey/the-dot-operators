import os
import sys
from pygame import Rect, quit
import pygame_gui
from pygame import QUIT
import tkinter as tk
from tkinter import filedialog
from client.constants import screen, WHITE, BLUE, font, WIDTH, HEIGHT, manager


class SettingsView:
    def __init__(self):
        self.settings = {}
        self.selected_file = None
        self.title = font.render("Settings", True, BLUE)

    def build(self):
        screen.fill(WHITE)
        screen.blit(self.title, (WIDTH // 2 - self.title.get_width() // 2, 50))

        self.settings_panel = pygame_gui.elements.UIPanel(
            relative_rect=Rect((50, 50), (WIDTH - 200 - 50, HEIGHT - 50)),
            starting_height=0,
            manager=manager
        )

        self.fullscreen_button = pygame_gui.elements.UIButton(Rect(50, 50, 200, 50),
                                                              "Fullscreen" if not self.settings[
                                                                  "fullscreen"] else "Windowed",
                                                              manager=manager,
                                                              container=self.settings_panel)
        self.open_file_button = pygame_gui.elements.UIButton(
            relative_rect=Rect((50, 250), (200, 50)),
            text="Open File",
            manager=manager,
            container=self.settings_panel
        )
        self.api_image_button = pygame_gui.elements.UIButton(
            relative_rect=Rect((50, 310), (200, 50)),
            text="API Image",
            manager=manager,
            container=self.settings_panel
        )

        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=Rect((self.settings_panel.rect.width // 2 - 50, self.settings_panel.rect.height - 70),
                               (100, 50)),
            text="Back",
            manager=manager,
            container=self.settings_panel
        )

        self.overlap_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=Rect((50, 370), (200, 50)),
            value_range=(0.15, 0.25),
            start_value=0.25,
            manager=manager,
            container=self.settings_panel
        )

    def open_file_dialog(self):
        if sys.platform in ['linux', 'darwin']:
            self.selected_file = os.popen('zenity --file-selection').read().strip()
        elif sys.platform == 'win32':
            root = tk.Tk()
            root.withdraw()
            self.selected_file = filedialog.askopenfilename()

    def event_handler(self, e):
        if e.type == QUIT:
            quit()
        if e.type == pygame_gui.UI_BUTTON_PRESSED:
            if e.ui_element == self.fullscreen_button:
                self.settings["fullscreen"] = not self.settings["fullscreen"]
                self.fullscreen_button.set_text("Fullscreen" if not self.settings['fullscreen'] else "Windowed")
            if e.ui_element == self.open_file_button:
                self.open_file_dialog()
                if self.selected_file:
                    print(f"File selected: {self.selected_file}")

            if e.ui_element == self.back_button:
                self.settings_panel.hide()
                return False
            return True

