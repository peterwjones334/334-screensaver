import random
import pygame
from base import Screensaver

COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 255, 255)]


class Pipe:
    def __init__(self, x, y, direction, color, width, height):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color
        self.size = 10
        self.history = [(x, y)]
        self.width = width
        self.height = height

    def update(self):
        if self.direction == 0:
            self.x += self.size
        elif self.direction == 1:
            self.y += self.size
        elif self.direction == 2:
            self.x -= self.size
        elif self.direction == 3:
            self.y -= self.size

        self.history.append((self.x, self.y))

        if random.randint(0, 9) == 0:
            self.direction = random.randint(0, 3)

        if self.x < 0 or self.x >= self.width or self.y < 0 or self.y >= self.height:
            self.x, self.y = self.width // 2, self.height // 2
            self.history = [(self.x, self.y)]

    def draw(self, screen):
        for i in range(len(self.history) - 1):
            pygame.draw.line(screen, self.color, self.history[i], self.history[i + 1], self.size)


class PipesScreensaver(Screensaver):
    def __init__(self):
        super().__init__(title="Pipes Screensaver", fps=30)
        self.pipes = [
            Pipe(self.width // 2, self.height // 2, random.randint(0, 3), random.choice(COLORS), self.width, self.height)
            for _ in range(5)
        ]

    def update(self):
        for pipe in self.pipes:
            pipe.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for pipe in self.pipes:
            pipe.draw(self.screen)


if __name__ == "__main__":
    PipesScreensaver().run()
