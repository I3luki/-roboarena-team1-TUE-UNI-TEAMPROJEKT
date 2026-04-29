import pygame
from random import randrange


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
SNAKE_BLOCK_SIZE = 30
APPLE_BLOCK_SIZE = 15
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

    # Startposition Schlange (Mitte des Bildschirms)
    # Die Schlange ist eine Liste aus Segmenten [x, y]
    snake = [[300, 300], [270, 300], [240, 300]]

    # Startposition Apfel (2.Zeile, 2.Reihe)
    # Der Apfel besteht aus einem Segment [x,y]
    apple = [SNAKE_BLOCK_SIZE,SNAKE_BLOCK_SIZE]


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

        # Testen ob Schlangenkopf Apfel berührt
        #   TRUE  --    setze Apfel auf zufaellige Position
        #   FALSE --    tue nichts
        def IsSnakeheadTouchingApple():
            snakehead_x = snake[0][0]
            snakehead_y = snake[0][1]
            apple_x = apple[0]
            apple_y = apple[1]
            if(apple_x == snakehead_x and apple_y == snakehead_y):
                return True
            return False
        
        if(IsSnakeheadTouchingApple()): 
            apple[0] = randrange(int(WINDOW_WIDTH/SNAKE_BLOCK_SIZE)) * SNAKE_BLOCK_SIZE
            apple[1] = randrange(int(WINDOW_HEIGHT/SNAKE_BLOCK_SIZE)) * SNAKE_BLOCK_SIZE
            
        # Bildschirmwechsel

        if head_x >= WINDOW_WIDTH:
            head_x = 0
        elif head_x < 0:
            head_x = WINDOW_WIDTH - SNAKE_BLOCK_SIZE
        if head_y >= WINDOW_HEIGHT:
            head_y = 0
        elif head_y < 0:
            head_y = WINDOW_HEIGHT - SNAKE_BLOCK_SIZE


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

        # Apfel zeichnen
        # offset fuer apfelgroesse kleiner als schlangengröße
        apple_draw_offset = int((SNAKE_BLOCK_SIZE - APPLE_BLOCK_SIZE) / 2)
        pygame.draw.rect(screen, "red", [ apple[0] + apple_draw_offset,
                                          apple[1] + apple_draw_offset, 
                                          APPLE_BLOCK_SIZE, APPLE_BLOCK_SIZE ])

        pygame.display.flip()

        # Fenster aktualisieren
        pygame.display.flip()

        # FPS begrenzen
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()