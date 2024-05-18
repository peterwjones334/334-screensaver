import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
BLACK = (0, 0, 0)

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
pygame.display.set_caption("Flying Toasters Screensaver")

# Load toaster image
toaster_image = pygame.image.load("toaster.png").convert_alpha()
num_toasters = 10
toasters = [Toaster(toaster_image, random.randint(1, 5)) for _ in range(num_toasters)]

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for toaster in toasters:
        toaster.update()
        toaster.show(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
