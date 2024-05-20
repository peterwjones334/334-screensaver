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

# Option for trails
enable_trails = False

# Define the Logo sprite class
class Logo(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.dx = random.choice([i for i in range(dx_range[0], dx_range[1]) if i != 0])
        self.dy = random.choice([i for i in range(dy_range[0], dy_range[1]) if i != 0])

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Bounce off the edges
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.dx = -self.dx
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy = -self.dy

# Function to handle collisions between logos
def handle_collisions(logos):
    for logo in logos:
        for other_logo in logos:
            if logo != other_logo and pygame.sprite.collide_rect(logo, other_logo):
                # More natural collision response: calculate new velocities based on mass (simplified to equal mass)
                dx1, dy1 = logo.dx, logo.dy
                dx2, dy2 = other_logo.dx, other_logo.dy

                logo.dx = dx2
                logo.dy = dy2
                other_logo.dx = dx1
                other_logo.dy = dy1

                # Move them apart based on their velocity
                while pygame.sprite.collide_rect(logo, other_logo):
                    logo.rect.x += logo.dx
                    logo.rect.y += logo.dy
                    other_logo.rect.x += other_logo.dx
                    other_logo.rect.y += other_logo.dy

# Create a group of logos
logos = pygame.sprite.Group()
for _ in range(num_logos):
    logo = Logo(logo_image)
    logos.add(logo)

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

    # Update and draw all logos
    logos.update()
    handle_collisions(logos)
    logos.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
