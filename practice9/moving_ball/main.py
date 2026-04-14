import pygame
from ball import Ball

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

ball = Ball(400, 300)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ball.move(-20, 0)
            if event.key == pygame.K_RIGHT:
                ball.move(20, 0)
            if event.key == pygame.K_UP:
                ball.move(0, -20)
            if event.key == pygame.K_DOWN:
                ball.move(0, 20)

    screen.fill((255, 255, 255))
    ball.draw(screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()