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


class FlyingObject:
    def __init__(self, image, speed, width, height, always_left=False):
        self.image = image
        self.speed = speed
        self.width = width
        self.height = height
        self.always_left = always_left
        self.reset()

    def reset(self):
        if self.always_left:
            self.x = 0
            self.y = random.randint(0, self.height - self.image.get_height())
            self.direction = "right"
        else:
            self.x = random.randint(0, self.width - self.image.get_width())
            self.y = random.randint(0, self.height - self.image.get_height())
            self.direction = random.choice(["left", "right"])

    def update(self):
        if self.always_left or self.direction == "right":
            self.x += self.speed
            if self.x > self.width:
                self.reset()
        else:
            self.x -= self.speed
            if self.x < -self.image.get_width():
                self.reset()

    def show(self, screen):
        screen.blit(self.image, (self.x, self.y))


class StarsToasterCamelScreensaver(Screensaver):
    def __init__(self):
        super().__init__(title="Starfield with Flying Toasters & Camels")
        toaster_img = load_image("toaster.png")
        camel_img = load_image("camel.png")

        self.stars = [Star(self.width, self.height) for _ in range(400)]
        self.toasters = [
            FlyingObject(toaster_img, random.randint(1, 5), self.width, self.height)
            for _ in range(10)
        ]
        self.camels = [
            FlyingObject(camel_img, random.randint(1, 5), self.width, self.height, always_left=True)
            for _ in range(1)
        ]
        self.star_speed = 10

    def update(self):
        for star in self.stars:
            star.update(self.star_speed)
        for t in self.toasters:
            t.update()
        for c in self.camels:
            c.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for star in self.stars:
            star.show(self.screen)
        for t in self.toasters:
            t.show(self.screen)
        for c in self.camels:
            c.show(self.screen)


if __name__ == "__main__":
    StarsToasterCamelScreensaver().run()
