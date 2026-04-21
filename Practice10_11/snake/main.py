# importing libraries
import pygame
import time
import random
import sys

snake_speed = 15

# Window size
window_x = 720
window_y = 480

# size of one snake/food block
block_size = 10

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)
purple = pygame.Color(180, 0, 255)
gray = pygame.Color(40, 40, 40)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('GeeksforGeeks Snakes')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position = [100, 50]

# defining first 4 blocks of snake body
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]

# -------------------- WALLS --------------------
# simple inner walls
walls = []

for x in range(200, 300, block_size):
    walls.append([x, 150])

for y in range(200, 300, block_size):
    walls.append([400, y])

# -------------------- FOOD TYPES --------------------
# each food has:
# color  -> how it looks
# weight -> how many points it gives
# timer  -> how long it stays on screen
food_types = [
    {"color": white, "weight": 1, "timer": 12},
    {"color": yellow, "weight": 2, "timer": 10},
    {"color": purple, "weight": 3, "timer": 8}
]

# fruit position
fruit_position = [0, 0]
fruit_spawn = True
current_food = random.choice(food_types)
food_start_time = time.time()

# setting default snake direction towards right
direction = 'RIGHT'
change_to = direction

# initial score and level
score = 0
level = 1


def is_on_snake(position):
    """
    Check if food is generated on snake body.
    """
    for block in snake_body:
        if position[0] == block[0] and position[1] == block[1]:
            return True
    return False


def is_on_wall(position):
    """
    Check if food is generated on wall.
    """
    for wall in walls:
        if position[0] == wall[0] and position[1] == wall[1]:
            return True
    return False


def generate_food():
    """
    Generate food in random position.
    Food must not appear on snake or wall.
    Also choose random food type.
    """
    global fruit_position, current_food, food_start_time

    while True:
        new_position = [random.randrange(1, (window_x // block_size)) * block_size,
                        random.randrange(1, (window_y // block_size)) * block_size]

        if not is_on_snake(new_position) and not is_on_wall(new_position):
            fruit_position = new_position
            current_food = random.choice(food_types)
            food_start_time = time.time()
            break


# create first food
generate_food()


# displaying Score and Level function
def show_score(choice, color, font, size):
  
    # creating font object
    score_font = pygame.font.SysFont(font, size)
    
    # text with score and level
    score_surface = score_font.render(
        'Score : ' + str(score) + '   Level : ' + str(level), True, color)
    
    # create rectangular object for the text
    score_rect = score_surface.get_rect()
    
    # displaying text
    game_window.blit(score_surface, score_rect)


def show_timer(color, font, size):
    """
    Show how much time is left before current food disappears.
    """
    timer_font = pygame.font.SysFont(font, size)
    time_left = current_food["timer"] - (time.time() - food_start_time)

    if time_left < 0:
        time_left = 0

    timer_surface = timer_font.render(
        'Food time : ' + str(int(time_left)), True, color)
    timer_rect = timer_surface.get_rect()
    timer_rect.topleft = (0, 25)
    game_window.blit(timer_surface, timer_rect)


# game over function
def game_over():
  
    # creating font object
    my_font = pygame.font.SysFont('times new roman', 50)
    
    # creating a text surface
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)
    
    # create a rectangular object for the text
    game_over_rect = game_over_surface.get_rect()
    
    # setting position of the text
    game_over_rect.midtop = (window_x/2, window_y/4)
    
    # draw text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    
    # after 2 seconds quit the program
    time.sleep(2)
    
    pygame.quit()
    quit()


# Main Function
while True:
    
    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # prevent opposite direction movement
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= block_size
    if direction == 'DOWN':
        snake_position[1] += block_size
    if direction == 'LEFT':
        snake_position[0] -= block_size
    if direction == 'RIGHT':
        snake_position[0] += block_size

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_position))

    # if snake eats fruit, increase score using food weight
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += current_food["weight"] * 10
        fruit_spawn = False
    else:
        snake_body.pop()

    # if food timer ends, remove old food and generate new one
    if time.time() - food_start_time >= current_food["timer"]:
        fruit_spawn = False
        
    # generate new food
    if not fruit_spawn:
        generate_food()
        
    fruit_spawn = True

    # level system
    # every 30 score points -> next level
    new_level = score // 30 + 1
    if new_level > level:
        level = new_level
        snake_speed += 2

    # background
    game_window.fill(black)

    # draw simple grid
    for x in range(0, window_x, block_size):
        pygame.draw.line(game_window, gray, (x, 0), (x, window_y))
    for y in range(0, window_y, block_size):
        pygame.draw.line(game_window, gray, (0, y), (window_x, y))
    
    # draw snake
    for i, pos in enumerate(snake_body):
        if i == 0:
            pygame.draw.rect(game_window, blue,
                             pygame.Rect(pos[0], pos[1], block_size, block_size))
        else:
            pygame.draw.rect(game_window, green,
                             pygame.Rect(pos[0], pos[1], block_size, block_size))

    # draw fruit with current random color
    pygame.draw.rect(game_window, current_food["color"], pygame.Rect(
        fruit_position[0], fruit_position[1], block_size, block_size))

    # draw walls
    for wall in walls:
        pygame.draw.rect(game_window, red,
                         pygame.Rect(wall[0], wall[1], block_size, block_size))

    # outer border
    pygame.draw.rect(game_window, white, pygame.Rect(0, 0, window_x, window_y), 10)

    # Game Over conditions for border collision / leaving area
    if snake_position[0] < 10 or snake_position[0] > window_x - 20:
        game_over()
    if snake_position[1] < 10 or snake_position[1] > window_y - 20:
        game_over()

    # collision with walls
    for wall in walls:
        if snake_position[0] == wall[0] and snake_position[1] == wall[1]:
            game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # displaying score and level continuously
    show_score(1, white, 'times new roman', 20)

    # displaying food timer
    show_timer(white, 'times new roman', 20)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second / Refresh Rate
    fps.tick(snake_speed)