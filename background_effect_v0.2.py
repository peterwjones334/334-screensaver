import pygame
import random
import numpy as np
import math

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()
swidth, sheight = 800, 600
width, height = 1024, 768
screen = pygame.display.set_mode((swidth, sheight))
pygame.display.set_caption("Background Effects")
clock = pygame.time.Clock()

def draw_grid(surface, color, step_x, step_y):
    for x in range(0, width, step_x):
        pygame.draw.line(surface, color, (x, 0), (x, height))
    for y in range(0, height, step_y):
        pygame.draw.line(surface, color, (0, y), (width, y))

def draw_checkerboard(surface, color1, color2, step_x, step_y):
    for y in range(0, height, step_y):
        for x in range(0, width, step_x):
            rect = pygame.Rect(x, y, step_x, step_y)
            if (x // step_x + y // step_y) % 2 == 0:
                pygame.draw.rect(surface, color1, rect)
            else:
                pygame.draw.rect(surface, color2, rect)

def apply_glitch_effect(surface):
    arr = pygame.surfarray.pixels3d(surface)
    glitch_arr = arr.copy()
    for _ in range(10):
        x_start = random.randint(0, width - 100)
        y_start = random.randint(0, height - 100)
        x_offset = random.randint(-20, 20)
        y_offset = random.randint(-20, 20)
        x_end = min(x_start + 100, width)
        y_end = min(y_start + 100, height)
        x_offset_end = min(x_start + x_offset + 100, width)
        y_offset_end = min(y_start + y_offset + 100, height)
        x_offset = max(0, x_offset)
        y_offset = max(0, y_offset)

        try:
            glitch_arr[x_start + x_offset:x_offset_end, y_start + y_offset:y_offset_end] = arr[x_start:x_end, y_start:y_end]
        except ValueError:
            continue
    pygame.surfarray.blit_array(surface, glitch_arr)

def color_shift(color, shift_value):
    r = (color[0] + shift_value) % 256
    g = (color[1] + shift_value) % 256
    b = (color[2] + shift_value) % 256
    return (r, g, b)

def rotate_surface(surface, angle):
    return pygame.transform.rotate(surface, angle)

def main():
    running = True
    step_x, step_y = 50, 50
    color1 = WHITE
    color2 = BLACK
    shift_value = 5
    mode = 'grid'
    angle = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mode = 'checkerboard' if mode == 'grid' else 'grid'

        screen.fill((GREEN))

        # Create a surface to draw the pattern
        pattern_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        if mode == 'grid':
            draw_grid(pattern_surface, color1, step_x, step_y)
        else:
            draw_checkerboard(pattern_surface, color1, color2, step_x, step_y)

        # Rotate the pattern surface
        rotated_surface = rotate_surface(pattern_surface, angle)
        angle = (angle + 1) % 360

        # Blit the rotated surface onto the screen
        screen.blit(rotated_surface, (0, 0))

        apply_glitch_effect(screen)

        color1 = color_shift(color1, shift_value)
        color2 = color_shift(color2, -shift_value)
        
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
