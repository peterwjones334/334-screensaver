import random
import pygame
from base import Screensaver, load_image


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


class Toaster:
    def __init__(self, image, speed, width, height):
        self.image = image
        self.speed = speed
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.x = random.randint(0, self.width - self.image.get_width())
        self.y = random.randint(0, self.height - self.image.get_height())
        self.direction = random.choice(["left", "right"])

    def update(self):
        if self.direction == "left":
            self.x -= self.speed
            if self.x < -self.image.get_width():
                self.reset()
        else:
            self.x += self.speed
            if self.x > self.width:
                self.reset()

    def show(self, screen):
        screen.blit(self.image, (self.x, self.y))


class FlyingToastersScreensaver(Screensaver):
    def __init__(self):
        super().__init__(title="Flying Toasters")
        self.toaster_image = load_image("toaster.png")
        self.stars = [Star(self.width, self.height) for _ in range(400)]
        self.toasters = [
            Toaster(self.toaster_image, random.randint(1, 5), self.width, self.height)
            for _ in range(10)
        ]
        self.star_speed = 10

    def update(self):
        for star in self.stars:
            star.update(self.star_speed)
        for toaster in self.toasters:
            toaster.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for star in self.stars:
            star.show(self.screen)
        for toaster in self.toasters:
            toaster.show(self.screen)


if __name__ == "__main__":
    FlyingToastersScreensaver().run()
