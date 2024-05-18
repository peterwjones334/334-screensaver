import sys
import random
import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 255, 255)]

# Pipe class
class Pipe:
    def __init__(self, x, y, direction, color):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color
        self.size = 10
        self.history = [(x, y)]

    def update(self):
        if self.direction == 0:  # Move right
            self.x += self.size
        elif self.direction == 1:  # Move down
            self.y += self.size
        elif self.direction == 2:  # Move left
            self.x -= self.size
        elif self.direction == 3:  # Move up
            self.y -= self.size

        # Append the new position to the history
        self.history.append((self.x, self.y))

        # Randomly change direction
        if random.randint(0, 9) == 0:
            self.direction = random.randint(0, 3)

        # Keep the pipe within screen bounds
        if self.x < 0 or self.x >= WIDTH or self.y < 0 or self.y >= HEIGHT:
            self.x, self.y = WIDTH // 2, HEIGHT // 2
            self.history = [(self.x, self.y)]

    def draw(self, screen):
        for i in range(len(self.history) - 1):
            start_pos = self.history[i]
            end_pos = self.history[i + 1]
            pygame.draw.line(screen, self.color, start_pos, end_pos, self.size)

# Function to handle the screensaver behavior
def run_screensaver():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pipes Screensaver")

    pipes = [Pipe(WIDTH // 2, HEIGHT // 2, random.randint(0, 3), random.choice(COLORS)) for _ in range(5)]

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BLACK)

        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Check command line arguments to determine mode
if len(sys.argv) == 1:
    run_screensaver()
elif sys.argv[1] == '/s':
    run_screensaver()
elif sys.argv[1] == '/c':
    print("No configuration needed.")
elif sys.argv[1] == '/p':
    hwnd = int(sys.argv[2])
    print("Preview window not implemented.")
else:
    run_screensaver()
