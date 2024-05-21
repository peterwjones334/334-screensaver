import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Matrix Falling Characters Screensaver")

# Load background image
background_image_path = "matrix_background.png"
if os.path.exists(background_image_path):
    background_image = pygame.image.load(background_image_path).convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
else:
    background_image = None

# Colors
BLACK = (0, 0, 0)

# Font settings
FONT_SIZE = 20
font = pygame.font.SysFont("monospace", FONT_SIZE, bold=True)

# Define the Character class
class Character:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.value = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        self.trail = []
        self.blink = random.choice([True, False])
        self.blink_timer = random.randint(5, 20)
        self.color = (0, random.randint(100, 255), 0)

    def update(self):
        self.trail.append((self.x, self.y, self.value))
        if len(self.trail) > 15:  # Increase the length of the trail
            self.trail.pop(0)

        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-20, -1)
            self.value = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            self.trail = []
            self.color = (0, random.randint(100, 255), 0)

        # Update blinking
        if self.blink:
            self.blink_timer -= 1
            if self.blink_timer <= 0:
                self.blink = not self.blink
                self.blink_timer = random.randint(5, 20)

    def draw(self, surface):
        for i, (tx, ty, tvalue) in enumerate(self.trail):
            shade = 255 - (i * 15)  # Adjust the fading effect
            char_color = (0, min(self.color[1], shade), 0)
            char = font.render(tvalue, True, char_color)
            surface.blit(char, (tx, ty))
        if not self.blink:
            char = font.render(self.value, True, self.color)
            surface.blit(char, (self.x, self.y))

# Create a list of falling characters
def create_falling_chars(columns):
    falling_chars = []
    for col in range(columns):
        for _ in range(random.randint(8, 15)):  # Increase density and overlap
            x = col * (FONT_SIZE // 2)  # Reduce spacing between columns
            y = random.randint(-HEIGHT, 0)
            speed = random.uniform(2, 5)
            falling_chars.append(Character(x, y, speed))
    return falling_chars

# Main loop
def main():
    running = True
    clock = pygame.time.Clock()
    columns = WIDTH // (FONT_SIZE // 2)
    falling_chars = create_falling_chars(columns)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BLACK)

        for char in falling_chars:
            char.update()
            char.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
