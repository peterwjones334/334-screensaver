import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Max Headroom Background Effects")
clock = pygame.time.Clock()

def draw_grid(screen, color, step_x, step_y):
    for x in range(0, width, step_x):
        pygame.draw.line(screen, color, (x, 0), (x, height))
    for y in range(0, height, step_y):
        pygame.draw.line(screen, color, (0, y), (width, y))

def draw_checkerboard(screen, color1, color2, step_x, step_y):
    for y in range(0, height, step_y):
        for x in range(0, width, step_x):
            rect = pygame.Rect(x, y, step_x, step_y)
            if (x // step_x + y // step_y) % 2 == 0:
                pygame.draw.rect(screen, color1, rect)
            else:
                pygame.draw.rect(screen, color2, rect)

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

def main():
    running = True
    step_x, step_y = 50, 50
    color1 = (0, 255, 0)
    color2 = (255, 0, 255)
    shift_value = 5
    mode = 'grid'

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mode = 'checkerboard' if mode == 'grid' else 'grid'

        screen.fill((0, 0, 0))
        if mode == 'grid':
            draw_grid(screen, color1, step_x, step_y)
        else:
            draw_checkerboard(screen, color1, color2, step_x, step_y)
        
        apply_glitch_effect(screen)

        color1 = color_shift(color1, shift_value)
        color2 = color_shift(color2, -shift_value)
        
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
