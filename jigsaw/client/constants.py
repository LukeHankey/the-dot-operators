import pygame
import pygame_gui

pygame.init()

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")

font = pygame.font.SysFont(None, 36)  # Default font, size 36
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
