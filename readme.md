# Pygame Screensaver Project

## Overview
This project demonstrates how to create a dynamic screensaver using Pygame, a set of Python modules designed for writing video games and multimedia applications. The screensaver features multiple moving sprites over a background image. Sprites can move in different patterns, including left to right, right to left, and random directions.

## What is a Screensaver?
A screensaver is a computer program that blanks the screen or fills it with moving images or patterns when the computer is not in use. Originally, screensavers were designed to prevent phosphor burn-in on CRT and plasma monitors. Today, they are primarily used for entertainment and security purposes.

## Features of This Screensaver
- **Dynamic Background**: The screensaver displays a background image that scales to fit the screen size.
- **Multiple Sprites**: Various sprites move across the screen in different patterns.
- **Resizable Window**: The screensaver window can be resized, and the background and sprites adjust accordingly.
- **User Input Handling**: The screensaver exits when the user presses a key or moves the mouse.
## Prerequisites
- Python 3.x
- Pygame library
## Installation
Install Python: Ensure Python 3.x is installed on your system. You can download it from python.org.

Install Pygame: Install the Pygame library using pip:

```sh
pip install pygame
```
Download the Project Files: Download the project files and place them in a directory.

## Files in the Project
- `dynamic_screensaver.py`: The main script that runs the screensaver.
- `background.png`: The background image for the screensaver.
- `sprite1.png`, `sprite2.png`, `sprite3.png`: Example sprite images used in the screensaver. 
You can add more images if needed.

## Running the Screensaver
Run the Script: Execute the Python script to run the screensaver:

```sh
python dynamic_screensaver.py
```

### Convert to a Screensaver (.scr) File:

Install PyInstaller if you haven't already:
```sh
pip install pyinstaller
```

Create an executable using PyInstaller:
```sh
pyinstaller --onefile --windowed dynamic_screensaver.py
```
Rename the resulting executable from dynamic_screensaver.exe to dynamic_screensaver.scr.
Move the `.scr` file to `C:\Windows\System32`.
Set the screensaver through the Screen Saver Settings in the Control Panel.

## Customization

### Adding More Sprites
To add more sprites, place the image files in the same directory as the script and update the images list in the script:

```python
images = [
    pygame.image.load("sprite1.png").convert_alpha(),
    pygame.image.load("sprite2.png").convert_alpha(),
    pygame.image.load("sprite3.png").convert_alpha(),
    pygame.image.load("new_sprite.png").convert_alpha()  # Add more images here
]
```

### Changing the Background
Replace `background.png` with a new background image, ensuring it matches the desired resolution and aspect ratio.

## Code Explanation

### Imports and Initialization

```python
import pygame
import random

# Initialize Pygame
pygame.init()
```

The script starts by importing necessary libraries and initializing Pygame.

## Detecting Screen Dimensions
```python
infoObject = pygame.display.Info()
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h
```

This code detects the current screen dimensions.

### Sprite Class

```python
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
```

The `Sprite` class handles the loading, movement, and display of sprites.

### Main Function

```python
def run_screensaver():
    global WIDTH, HEIGHT
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Pygame Screensaver")

    # Load and scale the background image to fit the screen dimensions
    background = pygame.image.load("background.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Load sprite images
    images = [
        pygame.image.load("sprite1.png").convert_alpha(),
        pygame.image.load("sprite2.png").convert_alpha(),
        pygame.image.load("sprite3.png").convert_alpha()
    ]

    # Create sprites
    num_sprites = 10
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
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEMOTION:
                running = False

        screen.blit(background, (0, 0))
        for sprite in sprites:
            sprite.update()
            sprite.show(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

run_screensaver()
```

The `run_screensaver` function sets up the screen, loads the background and sprite images, and handles the main animation loop.