import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 1024, 768

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Astronaut Screensaver")

# Load images
astronaut_img = pygame.image.load("astronaut1.png").convert_alpha()
satellite_img = pygame.image.load("satellite1.png").convert_alpha()

# Background color
bg_color = (0, 0, 0)

# Satellite properties
satellite_center = (width // 2, height // 2)
satellite_radius = 50
satellite_angle = 0
satellite_rotation_speed = 0.05

# Astronaut properties
astronaut_x = random.randint(0, width)
astronaut_y = random.randint(0, height)
astronaut_speed_x = random.uniform(-1, 1)
astronaut_speed_y = random.uniform(-1, 1)

# Clock to control frame rate
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update satellite rotation
    satellite_angle += satellite_rotation_speed
    if satellite_angle >= 360:
        satellite_angle -= 360
    rotated_satellite = pygame.transform.rotate(satellite_img, satellite_angle)
    satellite_rect = rotated_satellite.get_rect(center=satellite_center)

    # Update astronaut position
    astronaut_x += astronaut_speed_x
    astronaut_y += astronaut_speed_y

    # Wrap astronaut position around screen
    if astronaut_x < -astronaut_img.get_width():
        astronaut_x = width
    elif astronaut_x > width:
        astronaut_x = -astronaut_img.get_width()
    if astronaut_y < -astronaut_img.get_height():
        astronaut_y = height
    elif astronaut_y > height:
        astronaut_y = -astronaut_img.get_height()

    # Draw everything
    screen.fill(bg_color)
    screen.blit(rotated_satellite, satellite_rect.topleft)
    screen.blit(astronaut_img, (astronaut_x, astronaut_y))

    # Display update
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
