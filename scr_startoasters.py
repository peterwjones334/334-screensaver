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
        sx = int((self.x / self.z) * WIDTH // 2 + WIDTH // 2)
        sy = int((self.y / self.z) * HEIGHT // 2 + HEIGHT // 2)
        r = max(1, int(WIDTH / self.z))
        color = max(50, min(255, int(255 * (1 - self.z / WIDTH))))

        if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
            pygame.draw.circle(screen, (color, color, color), (sx, sy), r)

# Toaster class
class Toaster:
    def __init__(self, image, speed):
        self.image = image
        self.speed = speed
        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH - self.image.get_width())
        self.y = random.randint(0, HEIGHT - self.image.get_height())
        self.direction = random.choice(["left", "right"])

    def update(self):
        if self.direction == "left":
            self.x -= self.speed
            if self.x < -self.image.get_width():
                self.reset()
        else:
            self.x += self.speed
            if self.x > WIDTH:
                self.reset()

    def show(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Starfield with Flying Toasters Screensaver")

# Load toaster image
toaster_image = pygame.image.load("toaster.png").convert_alpha()

# Create a list of stars
num_stars = 400
stars = [Star() for _ in range(num_stars)]

# Create a list of toasters
num_toasters = 10
toasters = [Toaster(toaster_image, random.randint(1, 5)) for _ in range(num_toasters)]

# Main loop
running = True
clock = pygame.time.Clock()
star_speed = 10

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Update and draw stars
    for star in stars:
        star.update(star_speed)
        star.show(screen)

    # Update and draw toasters
    for toaster in toasters:
        toaster.update()
        toaster.show(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
