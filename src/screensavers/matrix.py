import random
import pygame
from base import Screensaver, load_image

FONT_SIZE = 20
CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


class Character:
    def __init__(self, x, y, speed, height):
        self.x = x
        self.y = y
        self.speed = speed
        self.height = height
        self.value = random.choice(CHARS)
        self.trail = []
        self.blink = random.choice([True, False])
        self.blink_timer = random.randint(5, 20)
        self.color = (0, random.randint(100, 255), 0)
        self.font = pygame.font.SysFont("monospace", FONT_SIZE, bold=True)

    def update(self):
        self.trail.append((self.x, self.y, self.value))
        if len(self.trail) > 15:
            self.trail.pop(0)

        self.y += self.speed
        if self.y > self.height:
            self.y = random.randint(-20, -1)
            self.value = random.choice(CHARS)
            self.trail = []
            self.color = (0, random.randint(100, 255), 0)

        if self.blink:
            self.blink_timer -= 1
            if self.blink_timer <= 0:
                self.blink = not self.blink
                self.blink_timer = random.randint(5, 20)

    def draw(self, surface):
        for i, (tx, ty, tvalue) in enumerate(self.trail):
            shade = 255 - (i * 15)
            char_color = (0, min(self.color[1], shade), 0)
            char = self.font.render(tvalue, True, char_color)
            surface.blit(char, (tx, ty))
        if not self.blink:
            char = self.font.render(self.value, True, self.color)
            surface.blit(char, (self.x, self.y))


class MatrixScreensaver(Screensaver):
    def __init__(self):
        super().__init__(title="Matrix Falling Characters")
        try:
            bg = load_image("matrix_background.png", convert_alpha=False)
            self.background = pygame.transform.scale(bg, (self.width, self.height))
        except FileNotFoundError:
            self.background = None

        columns = self.width // (FONT_SIZE // 2)
        self.falling_chars = []
        for col in range(columns):
            for _ in range(random.randint(8, 15)):
                x = col * (FONT_SIZE // 2)
                y = random.randint(-self.height, 0)
                speed = random.uniform(2, 5)
                self.falling_chars.append(Character(x, y, speed, self.height))

    def update(self):
        for char in self.falling_chars:
            char.update()

    def draw(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((0, 0, 0))
        for char in self.falling_chars:
            char.draw(self.screen)


if __name__ == "__main__":
    MatrixScreensaver().run()
