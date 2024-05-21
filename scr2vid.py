import pygame
import random
import sys
import cv2
import os
from datetime import datetime

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 1024
HEIGHT = 768

# Colors
BLACK = (0, 0, 0)

# Sprite class to handle different images and movement patterns
class Sprite:
    def __init__(self, images, speed):
        self.images = images  # List of images for the sprite
        self.image = random.choice(self.images)  # Select a random image
        self.speed = speed  # Speed of the sprite
        self.reset()

    def reset(self):
        self.image = random.choice(self.images)  # Select a random image
        self.direction = random.choice(["left_to_right", "right_to_left", "random"])  # Choose a random direction
        if self.direction == "left_to_right":
            self.x = 0
            self.y = random.randint(0, HEIGHT - self.image.get_height())
        elif self.direction == "right_to_left":
            self.x = WIDTH - self.image.get_width()
            self.y = random.randint(0, HEIGHT - self.image.get_height())
        elif self.direction == "random":
            self.x = random.randint(0, WIDTH - self.image.get_width())
            self.y = random.randint(0, HEIGHT - self.image.get_height())
            self.vx = random.choice([-self.speed, self.speed])
            self.vy = random.choice([-self.speed, self.speed])

    def update(self):
        if self.direction == "left_to_right":
            self.x += self.speed
            if self.x > WIDTH:
                self.reset()
        elif self.direction == "right_to_left":
            self.x -= self.speed
            if self.x < -self.image.get_width():
                self.reset()
        elif self.direction == "random":
            self.x += self.vx
            self.y += self.vy
            if self.x < 0 or self.x > WIDTH - self.image.get_width():
                self.vx = -self.vx
            if self.y < 0 or self.y > HEIGHT - self.image.get_height():
                self.vy = -self.vy

    def show(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Function to handle the screensaver behavior and capture frames
def run_screensaver_capture(video_filename, duration, frame_rate):
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Set up the screen with resizable option
    pygame.display.set_caption("Dynamic Screensaver with Multiple Sprites")

    # Load and scale the background image to fit the screen dimensions
    background = pygame.image.load("nebula_background_9_16.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Load the sprite images
    images = [
        pygame.image.load("toaster.png").convert_alpha(),
        pygame.image.load("camel.png").convert_alpha(),
        pygame.image.load("starship.png").convert_alpha(),  # Add more images as needed
    ]

    # Create a list of sprites
    num_sprites = 25
    sprites = [Sprite(images, random.randint(1, 5)) for _ in range(num_sprites)]

    running = True
    clock = pygame.time.Clock()
    frame_count = 0
    total_frames = duration * frame_rate

    # Video writer setup
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(video_filename, fourcc, frame_rate, (WIDTH, HEIGHT))

    while running and frame_count < total_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the background and update sprites
        screen.blit(background, (0, 0))
        for sprite in sprites:
            sprite.update()
            sprite.show(screen)

        pygame.display.flip()

        # Capture the screen
        frame = pygame.surfarray.array3d(pygame.display.get_surface())
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = cv2.transpose(frame)
        # frame = cv2.flip(frame, 0)
        video_writer.write(frame)

        frame_count += 1
        clock.tick(frame_rate)

    video_writer.release()
    pygame.quit()
    print(f"Video saved as {video_filename}")

# Check command line arguments to determine mode
if len(sys.argv) == 1 or sys.argv[1] == '/s':
    vidname = f"vid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    output_video_file = os.path.join(os.getcwd(), vidname)
    run_screensaver_capture(output_video_file, duration=30, frame_rate=30)
elif sys.argv[1] == '/c':
    print("No configuration needed.")
elif sys.argv[1] == '/p':
    hwnd = int(sys.argv[2])
    print("Preview window not implemented.")
else:
    vidname = f"vid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    output_video_file = os.path.join(os.getcwd(), vidname)
    run_screensaver_capture(output_video_file, duration=10, frame_rate=30)
