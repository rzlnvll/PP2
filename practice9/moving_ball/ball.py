import pygame

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 25
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.r)
    def move(self, dx, dy):
        if 0 <= self.x + dx - self.r and self.x + dx + self.r <= 800:
            self.x += dx
        if 0 <= self.y + dy - self.r and self.y + dy + self.r <= 600:
            self.y += dy