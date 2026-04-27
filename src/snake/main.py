import pygame


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
FPS = 60


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")

    clock = pygame.time.Clock()
    running = True

    while running:
        # Events verarbeiten
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Bildschirm zeichnen
        screen.fill((30, 30, 30))

        # Fenster aktualisieren
        pygame.display.flip()

        # FPS begrenzen
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()