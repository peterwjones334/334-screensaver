import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)

# Bubble class
class Bubble:
    def __init__(self):
        self.radius = random.randint(5, 15)
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = HEIGHT + self.radius  # Start just below the bottom of the screen
        self.speed = random.uniform(1, 3)
        self.color = LIGHT_BLUE
        self.alpha = random.randint(50, 200)  # Set transparency level

    def update(self):
        self.y -= self.speed
        if self.y < -self.radius:
            self.reset()

    def reset(self):
        self.radius = random.randint(5, 15)
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = HEIGHT + self.radius
        self.speed = random.uniform(1, 3)
        self.alpha = random.randint(50, 200)  # Reset transparency level

    def show(self, screen):
        bubble_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(bubble_surface, self.color + (self.alpha,), (self.radius, self.radius), self.radius)
        screen.blit(bubble_surface, (self.x - self.radius, self.y - self.radius))

# Fish class
class Fish:
    def __init__(self, image, direction):
        self.image = image
        self.direction = direction
        self.reset()

    def reset(self):
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        if self.direction == 'right_to_left':
            self.rect.x = WIDTH
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)
            self.speed = random.uniform(2, 5)
        elif self.direction == 'left_to_right':
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)
            self.speed = random.uniform(2, 5)   

    def update(self):
        if self.direction == 'right_to_left':
            self.rect.x -= self.speed
            if self.rect.right < 0:
                self.reset()
        elif self.direction == 'left_to_right':
            self.rect.x += self.speed
            if self.rect.left > WIDTH:
                self.reset()
        #elif self.direction == 'up_down':
        #    self.rect.y -= self.speed
         #   if self.rect.bottom < 0:
        #        self.reset()

    def show(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Special Fish class
class SpecialFish(Fish):
    def __init__(self, image, direction):
        super().__init__(image, direction)
        self.vertical_speed = random.uniform(1, 2)  # Additional vertical speed

    def reset(self):
        super().reset()
        self.vertical_direction = random.choice([-1, 1])  # Random initial vertical direction

    def update(self):
        super().update()
        self.rect.y += self.vertical_speed * self.vertical_direction
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.vertical_direction *= -1  # Reverse vertical direction if hitting the screen edges

# Function to handle the screensaver behavior
def run_screensaver():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fish Tank Screensaver")

    # Load and scale the background image to fit the screen dimensions
    background = pygame.image.load("fishtank.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    num_bubbles = 36
    bubbles = [Bubble() for _ in range(num_bubbles)]

    # Load fish images and assign directions based on their names
    fish_images = [
        ('fish1.png', 'right_to_left'),
        ('fish2.png', 'left_to_right'),
        ('fish3.png', 'right_to_left'),
        ('fish4.png', 'left_to_right'),
        ('fish5.png', 'right_to_left'),
        ('fish6.png', 'left_to_right')
    ]

    Special_fish_images = [
        ('special_fish1.png', 'right_to_left'),
        ('special_fish2.png', 'left_to_right')
    ]

    # Create more fish and randomize their directions
    num_fish = 12
    fish = []
    for _ in range(num_fish):
        image_file, direction = random.choice(fish_images)
        image = pygame.image.load(image_file).convert_alpha()
        fish.append(Fish(image, direction))

    # Add special fish
    num_special_fish = 1
    special_fish_list = []
    for _ in range(num_special_fish):
        special_fish_image, direction = random.choice(Special_fish_images)
        image = pygame.image.load(special_fish_image).convert_alpha()
        special_fish_list.append(SpecialFish(image, direction))


    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        screen.blit(background, (0, 0))

        for bubble in bubbles:
            bubble.update()
            bubble.show(screen)

        for f in fish:
            f.update()
            f.show(screen)

        for f in special_fish_list:
            f.update()
            f.show(screen)         

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Check command line arguments to determine mode
if __name__ == '__main__':
    run_screensaver()
