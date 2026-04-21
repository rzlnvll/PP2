# Imports
import pygame, sys
from pygame.locals import *
import random

# Initializing pygame
pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Screen size
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Game variables
SPEED = 5                 # enemy speed
SCORE = 0                 # how many enemies passed
COINS = 0                 # total collected coin value
COINS_FOR_SPEEDUP = 5     # every 5 collected coin points -> increase speed

# Setting up fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Loading background image
background = pygame.image.load("Practice10_11/racer/AnimatedStreet.png")

# Creating the game window
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Loading crash sound once
crash_sound = pygame.mixer.Sound("Practice10_11/racer/crash.wav")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load enemy image
        self.image = pygame.image.load("Practice10_11/racer/Enemy.png")
        self.rect = self.image.get_rect()

        # Put enemy at random x position at the top
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE

        # Move enemy downward
        self.rect.move_ip(0, SPEED)

        # If enemy goes below screen, reset it to top and increase score
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load player image
        self.image = pygame.image.load("Practice10_11/racer/Player.png")
        self.rect = self.image.get_rect()

        # Starting position of player
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        # Move left
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        # Move right
        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Randomly choose coin weight
        # weight = how many points player gets after collecting it
        self.weight = random.choice([1, 2, 3])

        # Create different size/color coin depending on weight
        # You can replace this with image files if you want
        if self.weight == 1:
            self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(self.image, YELLOW, (10, 10), 10)
        elif self.weight == 2:
            self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.circle(self.image, GREEN, (12, 12), 12)
        else:
            self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
            pygame.draw.circle(self.image, BLUE, (14, 14), 14)

        self.rect = self.image.get_rect()

        # Place coin at random position above the screen
        self.reset_position()

        # Coin falls a bit slower than enemy
        self.speed = 4

    def reset_position(self):
        # Random x position on road, random y above screen
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-300, -50)
        )

    def move(self):
        # Move coin downward
        self.rect.move_ip(0, self.speed)

        # If coin leaves screen, respawn it again randomly
        if self.rect.top > SCREEN_HEIGHT:
            self.weight = random.choice([1, 2, 3])

            # Recreate coin appearance depending on new weight
            if self.weight == 1:
                self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
                pygame.draw.circle(self.image, YELLOW, (10, 10), 10)
            elif self.weight == 2:
                self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
                pygame.draw.circle(self.image, GREEN, (12, 12), 12)
            else:
                self.image = pygame.Surface((28, 28), pygame.SRCALPHA)
                pygame.draw.circle(self.image, BLUE, (14, 14), 14)

            self.rect = self.image.get_rect()
            self.reset_position()


# Creating player and enemy objects
P1 = Player()
E1 = Enemy()

# Create some coins that appear randomly on the road
coin1 = Coin()
coin2 = Coin()

# Groups for sprites
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(coin1, coin2)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, coin1, coin2)

# Event for increasing speed with time
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# This variable helps us avoid increasing speed every frame
last_speedup_step = 0

# Game loop
while True:
    # Process events
    for event in pygame.event.get():
        # Increase speed slightly every second
        if event.type == INC_SPEED:
            SPEED += 0.2

        # Quit the game
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))

    # Show enemy pass score in top left
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))

    # Show collected coins in top right
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    coin_rect = coin_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    DISPLAYSURF.blit(coin_text, coin_rect)

    # Move and draw all sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Check collision between player and coins
    collected_coins = pygame.sprite.spritecollide(P1, coins, False)
    for coin in collected_coins:
        # Add the value of the collected coin
        COINS += coin.weight

        # Respawn the coin
        coin.weight = random.choice([1, 2, 3])

        if coin.weight == 1:
            coin.image = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(coin.image, YELLOW, (10, 10), 10)
        elif coin.weight == 2:
            coin.image = pygame.Surface((24, 24), pygame.SRCALPHA)
            pygame.draw.circle(coin.image, GREEN, (12, 12), 12)
        else:
            coin.image = pygame.Surface((28, 28), pygame.SRCALPHA)
            pygame.draw.circle(coin.image, BLUE, (14, 14), 14)

        coin.rect = coin.image.get_rect()
        coin.reset_position()

    # Increase enemy speed when enough coins are collected
    # Example:
    # 0-4 coins -> no bonus
    # 5-9 coins -> +1 speed
    # 10-14 coins -> +2 speed
    current_step = COINS // COINS_FOR_SPEEDUP
    if current_step > last_speedup_step:
        SPEED += 1
        last_speedup_step = current_step

    # Check collision between player and enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        crash_sound.play()

        # Show game over screen
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()

        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    # Update display and keep FPS stable
    pygame.display.update()
    FramePerSec.tick(FPS)