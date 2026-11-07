import random
from base import Screensaver, load_image


class Appliance:
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


class FlyingAppliancesScreensaver(Screensaver):
    def __init__(self):
        super().__init__(title="Flying Appliances")
        self.image = load_image("toaster.png")
        self.appliances = [
            Appliance(self.image, random.randint(1, 5), self.width, self.height)
            for _ in range(10)
        ]

    def update(self):
        for a in self.appliances:
            a.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        for a in self.appliances:
            a.show(self.screen)


if __name__ == "__main__":
    FlyingAppliancesScreensaver().run()
