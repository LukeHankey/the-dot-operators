import pygame
import pygame_gui
from constants import screen, WHITE, BLUE, WIDTH, manager, HEIGHT
from pygame.locals import QUIT

back_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((WIDTH // 2 - 50, HEIGHT - 70), (100, 50)),
    text="Back",
    manager=manager,
    visible=0
)


def credits_view():
    screen.fill(WHITE)

    title_font = pygame.font.Font(None, 48)
    credits_font = pygame.font.Font(None, 36)

    title = title_font.render("Jigsaw Game", True, BLUE)
    contributors = [
        "@LukeHankey LukeHankey Luke",
        "@busterbeam busterbeam Nathan Lloyd",
        "@EarthKiii EarthKiii Jonas Charrier",
        "@DavidStrootman DavidStrootman David Strootman",
        "@bartoszkobylinski Bartosz Kobylinski",
        "Version 0.1.0"
    ]

    back_button.show()
    clock = pygame.time.Clock()
    time_delta = 0

    while True:
        screen.fill(WHITE)

        # Center title in available space
        title_x = (WIDTH - 200) // 2 - title.get_width() // 2
        screen.blit(title, (title_x, 50))

        # Center contributors in available space
        y = 150
        for line in contributors:
            text = credits_font.render(line, True, BLUE)
            text_x = (WIDTH - 200) // 2 - text.get_width() // 2
            screen.blit(text, (text_x, y))
            y += 50

        for event in pygame.event.get():
            if event.type == QUIT:
                back_button.hide()
                return {"type": "quit"}
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        back_button.hide()
                        return {"type": "menu"}

            manager.process_events(event)

        manager.update(time_delta)

        manager.draw_ui(screen)

        pygame.display.update()
        time_delta = clock.tick(60) / 1000.0