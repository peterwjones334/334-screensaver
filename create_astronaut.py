import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Astronaut Bitmap Creation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create a simple astronaut bitmap (50x50 pixels)
astronaut_bitmap = pygame.Surface((50, 50))
astronaut_bitmap.fill(BLACK)

# Draw a simple representation of an astronaut
pygame.draw.circle(astronaut_bitmap, WHITE, (25, 15), 10)  # Head
pygame.draw.rect(astronaut_bitmap, WHITE, pygame.Rect(15, 25, 20, 20))  # Body
pygame.draw.line(astronaut_bitmap, WHITE, (15, 25), (5, 45), 2)  # Left leg
pygame.draw.line(astronaut_bitmap, WHITE, (35, 25), (45, 45), 2)  # Right leg
pygame.draw.line(astronaut_bitmap, WHITE, (15, 25), (5, 15), 2)  # Left arm
pygame.draw.line(astronaut_bitmap, WHITE, (35, 25), (45, 15), 2)  # Right arm

# Save the bitmap to a file
pygame.image.save(astronaut_bitmap, "satellite.png")

# Display the bitmap to verify
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    screen.blit(astronaut_bitmap, (width // 2 - 25, height // 2 - 25))
    pygame.display.flip()

    # Cap the frame rate
    clock = pygame.time.Clock()
    clock.tick(60)

pygame.quit()
sys.exit()
