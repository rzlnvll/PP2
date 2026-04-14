import pygame
from clock import MickeyClock


def main():
    pygame.init()

    WIDTH, HEIGHT = 600, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey Clock")

    app = MickeyClock(screen, WIDTH, HEIGHT)
    fps_clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        app.draw()
        pygame.display.flip()
        fps_clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()