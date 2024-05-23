import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()

# Get screen dimensions
info = pygame.display.Info()
width, height = info.current_w, info.current_h

# Set up the display in full screen
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Astronaut Screensaver")

# Load images
astronaut_img = pygame.image.load("astronaut1.png").convert_alpha()
satellite_img = pygame.image.load("satellite1.png").convert_alpha()

# Load and scale the optional background image
background_img = pygame.image.load("space1.png").convert() if pygame.image.get_extended() else None
if background_img:
    background_img = pygame.transform.scale(background_img, (width, height))

# Background color
bg_color = (0, 0, 30)

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

# Star properties
num_stars = 100
stars = []
for _ in range(num_stars):
    star_x = random.randint(0, width)
    star_y = random.randint(0, height)
    brightness = random.randint(128, 255)
    twinkle_speed = random.uniform(0.05, 0.1)
    stars.append([star_x, star_y, brightness, twinkle_speed, False, 2])  # Added nova state and radius

# Function to draw stars
def draw_stars(screen, stars):
    for star in stars:
        star_x, star_y, brightness, twinkle_speed, is_nova, radius = star
        
        if is_nova:
            # Expand and fade out nova star
            brightness = 255  # Flash bright white
            radius += 2
            if radius > 10:  # End nova state after expanding
                star[4] = False  # End nova state
                brightness = random.randint(128, 255)
                radius = 2
        else:
            # Normal twinkling
            brightness += twinkle_speed
            if brightness >= 255 or brightness <= 128:
                twinkle_speed = -twinkle_speed
        
        brightness = max(0, min(255, brightness))
        star[2] = brightness
        star[3] = twinkle_speed
        star[5] = radius
        color = (brightness, brightness, brightness)
        pygame.draw.circle(screen, color, (star_x, star_y), radius)

# Clock to control frame rate
clock = pygame.time.Clock()

# Timer for nova events
nova_timer = 0
nova_interval = random.randint(5000, 10000)  # Random interval between 5 and 10 seconds

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
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
    if background_img:
        screen.blit(background_img, (0, 0))
    else:
        screen.fill(bg_color)

    draw_stars(screen, stars)

    screen.blit(rotated_satellite, satellite_rect.topleft)
    screen.blit(astronaut_img, (astronaut_x, astronaut_y))

    # Display update
    pygame.display.flip()

    # Check for nova event
    nova_timer += clock.get_time()
    if nova_timer >= nova_interval:
        nova_timer = 0
        nova_interval = random.randint(5000, 10000)
        # Trigger a nova event for a random star
        star = random.choice(stars)
        star[4] = True

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()
