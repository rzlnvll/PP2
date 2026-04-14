import datetime
import pygame


class MickeyClock:
    def __init__(self, screen, width, height):
        self.screen = screen

        self.clock_image = pygame.image.load("mickeys_clocks/images/clocks.png").convert_alpha()
        self.left_hand_image = pygame.image.load("mickeys_clocks/images/left_hand.png").convert_alpha()
        self.right_hand_image = pygame.image.load("mickeys_clocks/images/right_hand.png").convert_alpha()

        self.clock_image = pygame.transform.scale(self.clock_image, (600, 600))
        self.left_hand_image = pygame.transform.scale(self.left_hand_image, (140, 240))
        self.right_hand_image = pygame.transform.scale(self.right_hand_image, (140, 240))

        self.bg_color = (255, 255, 255)

        self.left_pivot = (300, 315)
        self.right_pivot = (300, 315)

        self.left_anchor = (60, 5)
        self.right_anchor = (50, 15)

    def blit_rotate(self, image, pivot, anchor, angle):
        rect = image.get_rect()
        offset = pygame.math.Vector2(anchor) - rect.center
        rotated_offset = offset.rotate(-angle)

        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rotated_image.get_rect(
            center=(pivot[0] - rotated_offset.x, pivot[1] - rotated_offset.y)
        )

        self.screen.blit(rotated_image, rotated_rect)

    def draw(self):
        self.screen.fill(self.bg_color)
        self.screen.blit(self.clock_image, (0, 0))

        now = datetime.datetime.now()
        minute = now.minute
        second = now.second

        second_angle = -(second * 6)
        minute_angle = -((minute + second / 60) * 6) + 180

        self.blit_rotate(
            self.right_hand_image,
            self.right_pivot,
            self.right_anchor,
            minute_angle
        )

        self.blit_rotate(
            self.left_hand_image,
            self.left_pivot,
            self.left_anchor,
            second_angle
        )