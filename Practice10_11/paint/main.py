import pygame
import math

pygame.init()

# Window
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)

# Background
screen.fill(WHITE)

# Font
font = pygame.font.SysFont("Arial", 18)

# Current settings
current_color = BLACK
current_tool = "rectangle"

# Mouse positions
start_pos = None
drawing = False

# Canvas for saving drawings
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# Tool buttons
tool_buttons = {
    "rectangle": pygame.Rect(10, 10, 100, 30),
    "circle": pygame.Rect(120, 10, 100, 30),
    "eraser": pygame.Rect(230, 10, 100, 30),
    "square": pygame.Rect(340, 10, 100, 30),
    "right triangle": pygame.Rect(450, 10, 120, 30),
    "equilateral triangle": pygame.Rect(580, 10, 170, 30),
    "rhombus": pygame.Rect(760, 10, 100, 30)
}

# Color buttons
color_buttons = [
    (BLACK, pygame.Rect(10, 50, 40, 40)),
    (RED, pygame.Rect(60, 50, 40, 40)),
    (GREEN, pygame.Rect(110, 50, 40, 40)),
    (BLUE, pygame.Rect(160, 50, 40, 40)),
    (YELLOW, pygame.Rect(210, 50, 40, 40))
]


def draw_toolbar():
    # Top gray panel
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 100))

    # Draw tool buttons
    for tool, rect in tool_buttons.items():
        if tool == current_tool:
            pygame.draw.rect(screen, BLUE, rect)
        else:
            pygame.draw.rect(screen, WHITE, rect)

        pygame.draw.rect(screen, BLACK, rect, 2)
        text = font.render(tool, True, BLACK)
        screen.blit(text, (rect.x + 5, rect.y + 7))

    # Draw color section
    text = font.render("Colors:", True, BLACK)
    screen.blit(text, (10, 95))

    for color, rect in color_buttons:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    # Show selected color
    pygame.draw.rect(screen, current_color, (280, 50, 40, 40))
    pygame.draw.rect(screen, BLACK, (280, 50, 40, 40), 2)
    label = font.render("Selected", True, BLACK)
    screen.blit(label, (330, 60))


def draw_rectangle(surface, color, start, end):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    width = abs(start[0] - end[0])
    height = abs(start[1] - end[1])
    pygame.draw.rect(surface, color, (x, y, width, height), 2)


def draw_square(surface, color, start, end):
    side = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
    x = start[0]
    y = start[1]

    if end[0] < start[0]:
        x = start[0] - side
    if end[1] < start[1]:
        y = start[1] - side

    pygame.draw.rect(surface, color, (x, y, side, side), 2)


def draw_circle(surface, color, start, end):
    radius = int(math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2))
    pygame.draw.circle(surface, color, start, radius, 2)


def draw_right_triangle(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points, 2)


def draw_equilateral_triangle(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end

    side = abs(x2 - x1)
    height = int((math.sqrt(3) / 2) * side)

    p1 = (x1, y1)
    p2 = (x1 + side, y1)

    if y2 >= y1:
        p3 = (x1 + side // 2, y1 + height)
    else:
        p3 = (x1 + side // 2, y1 - height)

    pygame.draw.polygon(surface, color, [p1, p2, p3], 2)


def draw_rhombus(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end

    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    points = [
        (center_x, y1),
        (x2, center_y),
        (center_x, y2),
        (x1, center_y)
    ]
    pygame.draw.polygon(surface, color, points, 2)


running = True
clock = pygame.time.Clock()

while running:
    screen.blit(canvas, (0, 0))
    draw_toolbar()

    # Preview shape while dragging
    if drawing and start_pos and current_tool != "eraser":
        temp_surface = canvas.copy()
        mouse_pos = pygame.mouse.get_pos()

        if current_tool == "rectangle":
            draw_rectangle(temp_surface, current_color, start_pos, mouse_pos)
        elif current_tool == "circle":
            draw_circle(temp_surface, current_color, start_pos, mouse_pos)
        elif current_tool == "square":
            draw_square(temp_surface, current_color, start_pos, mouse_pos)
        elif current_tool == "right triangle":
            draw_right_triangle(temp_surface, current_color, start_pos, mouse_pos)
        elif current_tool == "equilateral triangle":
            draw_equilateral_triangle(temp_surface, current_color, start_pos, mouse_pos)
        elif current_tool == "rhombus":
            draw_rhombus(temp_surface, current_color, start_pos, mouse_pos)

        screen.blit(temp_surface, (0, 0))
        draw_toolbar()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Check tool buttons
            for tool, rect in tool_buttons.items():
                if rect.collidepoint(mouse_pos):
                    current_tool = tool

            # Check color buttons
            for color, rect in color_buttons:
                if rect.collidepoint(mouse_pos):
                    current_color = color

            # Start drawing only below toolbar
            if mouse_pos[1] > 100:
                drawing = True
                start_pos = mouse_pos

                if current_tool == "eraser":
                    pygame.draw.circle(canvas, WHITE, mouse_pos, 20)

        elif event.type == pygame.MOUSEMOTION:
            if drawing and current_tool == "eraser":
                pygame.draw.circle(canvas, WHITE, event.pos, 20)

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = event.pos

                if current_tool == "rectangle":
                    draw_rectangle(canvas, current_color, start_pos, end_pos)
                elif current_tool == "circle":
                    draw_circle(canvas, current_color, start_pos, end_pos)
                elif current_tool == "square":
                    draw_square(canvas, current_color, start_pos, end_pos)
                elif current_tool == "right triangle":
                    draw_right_triangle(canvas, current_color, start_pos, end_pos)
                elif current_tool == "equilateral triangle":
                    draw_equilateral_triangle(canvas, current_color, start_pos, end_pos)
                elif current_tool == "rhombus":
                    draw_rhombus(canvas, current_color, start_pos, end_pos)

            drawing = False
            start_pos = None

    pygame.display.update()
    clock.tick(60)

pygame.quit()