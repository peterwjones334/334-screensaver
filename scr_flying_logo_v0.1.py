import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Logo Screensaver")

# Load logo or flag image
logo_image = pygame.image.load("logo.png").convert_alpha()
logo_rect = logo_image.get_rect()
logo_rect.topleft = (WIDTH // 2 - logo_rect.width // 2, HEIGHT // 2 - logo_rect.height // 2)

# Colors
BLACK = (0, 0, 0)

# Movement parameters
dx = 3
dy = 3

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            running = False

    # Update logo position
    logo_rect.x += dx
    logo_rect.y += dy

    # Bounce off the edges
    if logo_rect.left <= 0 or logo_rect.right >= WIDTH:
        dx = -dx
    if logo_rect.top <= 0 or logo_rect.bottom >= HEIGHT:
        dy = -dy

    # Draw everything
    screen.fill(BLACK)
    screen.blit(logo_image, logo_rect.topleft)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

