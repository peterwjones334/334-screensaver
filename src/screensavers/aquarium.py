import random
import pygame
from base import Screensaver, load_image

LIGHT_BLUE = (173, 216, 230)


class Bubble:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.radius = random.randint(5, 15)
        self.x = random.randint(self.radius, self.width - self.radius)
        self.y = self.height + self.radius
        self.speed = random.uniform(1, 3)
        self.alpha = random.randint(50, 200)

    def update(self):
        self.y -= self.speed
        if self.y < -self.radius:
            self.reset()

    def show(self, screen):
        bubble_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(bubble_surface, LIGHT_BLUE + (self.alpha,), (self.radius, self.radius), self.radius)
        screen.blit(bubble_surface, (self.x - self.radius, self.y - self.radius))


class Fish:
    def __init__(self, image, direction, width, height):
        self.image = image
        self.direction = direction
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.rect = self.image.get_rect()
        if self.direction == 'right_to_left':
            self.rect.x = self.width
            self.rect.y = random.randint(0, self.height - self.rect.height)
            self.speed = random.uniform(2, 5)
        else:
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, self.height - self.rect.height)
            self.speed = random.uniform(2, 5)

    def update(self):
        if self.direction == 'right_to_left':
            self.rect.x -= self.speed
            if self.rect.right < 0:
                self.reset()
        else:
            self.rect.x += self.speed
            if self.rect.left > self.width:
                self.reset()

    def show(self, screen):
        screen.blit(self.image, self.rect.topleft)


class SpecialFish(Fish):
    def __init__(self, image, direction, width, height):
        super().__init__(image, direction, width, height)
        self.vertical_speed = random.uniform(1, 2)

    def reset(self):
        super().reset()
        self.vertical_direction = random.choice([-1, 1])

    def update(self):
        super().update()
        self.rect.y += self.vertical_speed * self.vertical_direction
        if self.rect.top <= 0 or self.rect.bottom >= self.height:
            self.vertical_direction *= -1


class AquariumScreensaver(Screensaver):
    def __init__(self):
        super().__init__(title="Fish Tank Screensaver")
        bg = load_image("fishtank.png", convert_alpha=False)
        self.background = pygame.transform.scale(bg, (self.width, self.height))

        self.bubbles = [Bubble(self.width, self.height) for _ in range(36)]

        fish_files = [
            ('fish1.png', 'right_to_left'),
            ('fish2.png', 'left_to_right'),
            ('fish3.png', 'right_to_left'),
            ('fish4.png', 'left_to_right'),
            ('fish5.png', 'right_to_left'),
            ('fish6.png', 'left_to_right'),
        ]
        special_files = [
            ('special_fish1.png', 'right_to_left'),
            ('special_fish2.png', 'left_to_right'),
        ]

        self.fish = []
        for _ in range(12):
            fname, direction = random.choice(fish_files)
            img = load_image(fname)
            self.fish.append(Fish(img, direction, self.width, self.height))

        self.special_fish = []
        fname, direction = random.choice(special_files)
        img = load_image(fname)
        self.special_fish.append(SpecialFish(img, direction, self.width, self.height))

    def update(self):
        for b in self.bubbles:
            b.update()
        for f in self.fish:
            f.update()
        for f in self.special_fish:
            f.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for b in self.bubbles:
            b.show(self.screen)
        for f in self.fish:
            f.show(self.screen)
        for f in self.special_fish:
            f.show(self.screen)


if __name__ == "__main__":
    AquariumScreensaver().run()
