import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

# Create the planet arc image
arc_width, arc_height = 200, 200
planet_arc = pygame.Surface((arc_width, arc_height), pygame.SRCALPHA)
planet_arc.fill((0, 0, 0, 0))  # Fill with transparency

# Draw the filled arc (planet horizon)
pygame.draw.arc(planet_arc, BLUE, [0, 0, arc_width, arc_height], math.radians(0), math.radians(180), 10)
pygame.draw.arc(planet_arc, BROWN, [0, 10, arc_width, arc_height], math.radians(0), math.radians(180), 10)

# Save the arc image
pygame.image.save(planet_arc, "planet_arc.png")

# Display the arc image to verify
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Planet Arc")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    screen.blit(planet_arc, (0, height - arc_height))
    pygame.display.flip()

pygame.quit()
sys.exit()
