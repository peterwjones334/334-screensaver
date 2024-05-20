import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Logos Screensaver")

# Load logo or flag image
logo_image = pygame.image.load("logo.png").convert_alpha()
logo_rect = logo_image.get_rect()

# Colors
BLACK = (0, 0, 0)

# Movement parameters
num_logos = 6  # Number of logos
dx_range = (-3, 3)
dy_range = (-3, 3)

# Create a list of logos with positions and velocities
logos = []
for _ in range(num_logos):
    rect = logo_image.get_rect()
    rect.x = random.randint(0, WIDTH - rect.width)
    rect.y = random.randint(0, HEIGHT - rect.height)
    dx = random.choice([i for i in range(dx_range[0], dx_range[1]) if i != 0])
    dy = random.choice([i for i in range(dy_range[0], dy_range[1]) if i != 0])
    logos.append([rect, dx, dy])

# Option for trails
enable_trails = False

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            running = False

    if not enable_trails:
        screen.fill(BLACK)

    # Update logo positions
    for logo in logos:
        rect, dx, dy = logo
        rect.x += dx
        rect.y += dy

        # Bounce off the edges
        if rect.left <= 0 or rect.right >= WIDTH:
            dx = -dx
        if rect.top <= 0 or rect.bottom >= HEIGHT:
            dy = -dy

        # Update the logo's velocity
        logo[1] = dx
        logo[2] = dy

        # Draw the logo
        screen.blit(logo_image, rect.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
