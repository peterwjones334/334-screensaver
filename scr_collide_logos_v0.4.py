import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Logos Screensaver")

# Load background image
background_image_path = "background.png"
if os.path.exists(background_image_path):
    background_image = pygame.image.load(background_image_path).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
else:
    background_image = None

# Load all logo images from the 'logos' directory
logo_dir = 'logos'
if os.path.exists(logo_dir) and os.listdir(logo_dir):
    logo_images = [pygame.image.load(os.path.join(logo_dir, file)).convert_alpha() for file in os.listdir(logo_dir) if file.endswith('.png')]
else:
    logo_images = []

# Function to generate a random 64x64 colored square
def generate_random_logo():
    logo = pygame.Surface((64, 64), pygame.SRCALPHA)
    color = [random.randint(0, 255) for _ in range(3)]
    logo.fill(color)
    return logo

# If no logo images were loaded, generate random logos
if not logo_images:
    logo_images = [generate_random_logo() for _ in range(10)]

# Colors
BLACK = (0, 0, 0)

# Movement parameters
num_logos = 10  # Number of logos
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

        # Ensure logo stays within bounds after bouncing
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

# Function to handle collisions between logos
def handle_collisions(logos):
    for logo in logos:
        for other_logo in logos:
            if logo != other_logo and pygame.sprite.collide_rect(logo, other_logo):
                # More natural collision response: calculate new velocities based on mass (simplified to equal mass)
                dx1, dy1 = logo.dx, logo.dy
                dx2, dy2 = other_logo.dx, other_logo.dy

                logo.dx, other_logo.dx = dx2, dx1
                logo.dy, other_logo.dy = dy2, dy1

                # Move them apart based on their velocity
                while pygame.sprite.collide_rect(logo, other_logo):
                    logo.rect.x += logo.dx
                    logo.rect.y += logo.dy
                    other_logo.rect.x += other_logo.dx
                    other_logo.rect.y += other_logo.dy

                # Ensure logos stay within bounds after collision
                logo.rect.x = max(0, min(logo.rect.x, WIDTH - logo.rect.width))
                logo.rect.y = max(0, min(logo.rect.y, HEIGHT - logo.rect.height))
                other_logo.rect.x = max(0, min(other_logo.rect.x, WIDTH - other_logo.rect.width))
                other_logo.rect.y = max(0, min(other_logo.rect.y, HEIGHT - other_logo.rect.height))

# Create a group of logos
logos = pygame.sprite.Group()
for _ in range(num_logos):
    image = random.choice(logo_images)
    logo = Logo(image)
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
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BLACK)

    # Update and draw all logos
    logos.update()
    handle_collisions(logos)
    logos.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

