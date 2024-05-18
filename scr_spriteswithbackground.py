""""
Title: Screen Saver 
Description: This script creates a screensaver with a background and flying sprites.
Author: 334 Digital 
Date: 2024-05-18
Version: 1.0

Dependencies:
    - sys
    - pygame
    - random

Usage:
    scr_spriteswithbackground.py

License:
    MIT License

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import sys
import pygame
import random

# Initialize Pygame
pygame.init()

# Detect screen dimensions
infoObject = pygame.display.Info()
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h

# Colors
BLACK = (0, 0, 0)

# Sprite class
class Sprite:
    def __init__(self, images, speed):
        self.images = images
        self.image = random.choice(self.images)
        self.speed = speed
        self.reset()

    def reset(self):
        self.image = random.choice(self.images)
        self.direction = random.choice(["left_to_right", "right_to_left", "random"])
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

# Function to handle the screensaver behavior
def run_screensaver():
    global WIDTH, HEIGHT
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Dynamic Screensaver with Multiple Sprites")

    background = pygame.image.load("fractal_background.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    images = [
        pygame.image.load("toaster.png").convert_alpha(),
        pygame.image.load("camel.png").convert_alpha(),
        pygame.image.load("starship.png").convert_alpha(),  # Add more images as needed
    ]

    num_sprites = 12
    sprites = [Sprite(images, random.randint(1, 5)) for _ in range(num_sprites)]

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                background = pygame.transform.scale(background, (WIDTH, HEIGHT))
                for sprite in sprites:
                    sprite.reset()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False                    

        screen.blit(background, (0, 0))

        for sprite in sprites:
            sprite.update()
            sprite.show(screen)
        pygame.display.flip()
        clock.tick(60)

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
