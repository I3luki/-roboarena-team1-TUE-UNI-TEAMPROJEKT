import pygame


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
FPS = 10


def main():
    #Import
    from input_handler import handle_keydown
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")

    #Clocklogik
    clock = pygame.time.Clock()
    running = True
    #Bewgenugns Initlaiserungs Richtung
    direction = "right"
    while running:
        # Events verarbeiten
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Bewegung in Main implemtieren
            elif event.type == pygame.KEYDOWN:
                direction = handle_keydown(event, direction)
                # Überprüfung der bewungslogik auf der Konsole
                print(direction)

        # Bildschirm zeichnen
        screen.fill((30, 30, 30))

        # Fenster aktualisieren
        pygame.display.flip()

        # FPS begrenzen
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()