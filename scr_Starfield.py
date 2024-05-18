import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Star class
class Star:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(-WIDTH // 2, WIDTH // 2)
        self.y = random.randint(-HEIGHT // 2, HEIGHT // 2)
        self.z = random.randint(1, WIDTH)

    def update(self, speed):
        self.z -= speed
        if self.z <= 0:
            self.reset()

    def show(self, screen):
        # Map star position from 3D to 2D
        sx = int((self.x / self.z) * WIDTH // 2 + WIDTH // 2)
        sy = int((self.y / self.z) * HEIGHT // 2 + HEIGHT // 2)

        # Map star size and brightness based on z distance
        r = max(1, int(WIDTH / self.z))
        color = max(50, min(255, int(255 * (1 - self.z / WIDTH))))

        if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
            pygame.draw.circle(screen, (color, color, color), (sx, sy), r)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Starfield Screensaver")

# Create a list of stars
num_stars = 400
stars = [Star() for _ in range(num_stars)]

# Main loop
running = True
clock = pygame.time.Clock()
speed = 10

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for star in stars:
        star.update(speed)
        star.show(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
