import random
import pygame
from base import Screensaver


class Star:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.x = random.randint(-self.width // 2, self.width // 2)
        self.y = random.randint(-self.height // 2, self.height // 2)
        self.z = random.randint(1, self.width)

    def update(self, speed):
        self.z -= speed
        if self.z <= 0:
            self.reset()

    def show(self, screen):
        sx = int((self.x / self.z) * self.width // 2 + self.width // 2)
        sy = int((self.y / self.z) * self.height // 2 + self.height // 2)
        r = max(1, int(self.width / self.z))
        color = max(50, min(255, int(255 * (1 - self.z / self.width))))
        if 0 <= sx < self.width and 0 <= sy < self.height:
            pygame.draw.circle(screen, (color, color, color), (sx, sy), r)


class StarfieldScreensaver(Screensaver):
    def __init__(self):
        super().__init__(title="Starfield Screensaver")
        self.speed = 10
        self.stars = [Star(self.width, self.height) for _ in range(400)]

    def update(self):
        for star in self.stars:
            star.update(self.speed)

    def draw(self):
        self.screen.fill((0, 0, 0))
        for star in self.stars:
            star.show(self.screen)


if __name__ == "__main__":
    StarfieldScreensaver().run()
