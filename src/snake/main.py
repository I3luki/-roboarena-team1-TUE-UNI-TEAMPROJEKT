import pygame


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
SNAKE_BLOCK_SIZE = 30
FPS = 10


def main():
    #Import
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")

    #Clocklogik
    clock = pygame.time.Clock()
    running = True
    direction = "RIGHT"

    # Startposition (Mitte des Bildschirms)
    # Die Schlange ist eine Liste aus Segmenten [x, y]
    snake = [[300, 300], [270, 300], [240, 300]]

    while running:
        # Events verarbeiten
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Bewegungseingabe erkennen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # Bewegungslogik
        head_x, head_y = snake[0]

        if direction == "UP":
            head_y -= SNAKE_BLOCK_SIZE
        elif direction == "DOWN":
            head_y += SNAKE_BLOCK_SIZE
        elif direction == "LEFT":
            head_x -= SNAKE_BLOCK_SIZE
        elif direction == "RIGHT":
            head_x += SNAKE_BLOCK_SIZE

        # Neuen Kopf hinzufügen
        new_head = [head_x, head_y]
        snake.insert(0, new_head)

        # Schwanz verschwindet (solange sie kein Essen frisst!!!)
        snake.pop()

        # Bildschirm zeichnen
        screen.fill((30, 30, 30))

        # Schlange zeichnen
        for segment in snake:
            pygame.draw.rect(screen, "green", [segment[0], segment[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

        pygame.display.flip()

        # Fenster aktualisieren
        pygame.display.flip()

        # FPS begrenzen
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()