import random
import time
import pygame
from base import Screensaver, load_image


class GhostSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.width = width
        self.height = height

    def update(self):
        self.rect.x += random.randint(-5, 5)
        self.rect.y += random.randint(-5, 5)
        self.rect.x = max(0, min(self.rect.x, self.width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.height - self.rect.height))


class EyesSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.original_image = image
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.width = width
        self.height = height
        self.blinking = False

    def blink(self):
        if not self.blinking:
            self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            self.blinking = True
        else:
            self.image = self.original_image
            self.blinking = False

    def move(self, dx, dy):
        self.rect.x = max(0, min(self.rect.x + dx, self.width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y + dy, self.height - self.rect.height))


class BatSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, direction, width, height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = direction
        self.width = width
        self.height = height
        self.vertical_movement = 0

    def update(self):
        if self.direction == "right":
            self.rect.x += 5
            if self.rect.x > self.width:
                self.rect.x = -self.rect.width
        else:
            self.rect.x -= 5
            if self.rect.x < -self.rect.width:
                self.rect.x = self.width

        self.vertical_movement += random.choice([-1, 1])
        self.rect.y += self.vertical_movement
        self.vertical_movement = -self.vertical_movement
        self.rect.y = max(0, min(self.rect.y, self.height // 2 - self.rect.height))


class HauntedHouseScreensaver(Screensaver):
    def __init__(self):
        super().__init__(title="Haunted House", width=1025, height=768)
        self.house_image = load_image("haunted_house7.png")
        self.logo_image = load_image("logo.png")
        self.skull_image = pygame.transform.scale(load_image("skull1.png"), (200, 200))

        self.ghosts = pygame.sprite.Group()
        ghost_files = ["ghost1.png", "ghost2.png", "ghost3.png"]
        ghost_positions = [(256, 384), (512, 384), (600, 384)]
        for path, pos in zip(ghost_files, ghost_positions):
            img = load_image(path)
            self.ghosts.add(GhostSprite(img, pos[0], pos[1], self.width, self.height))

        eyes_img = load_image("eyes1.png")
        self.eyes = EyesSprite(eyes_img, 512, 268, self.width, self.height)

        self.bats = pygame.sprite.Group()
        bat_img = load_image("bat1.png")
        bat_positions = [(60, 50), (750, 100), (70, 150)]
        for i, pos in enumerate(bat_positions):
            direction = "right" if i % 2 == 0 else "left"
            self.bats.add(BatSprite(bat_img, pos[0], pos[1], direction, self.width, self.height))

        self.flash_skull = False
        self.flash_time = 0
        self.skull_flash_interval = random.randint(10, 30)
        self.showed_logo = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_b:
                    self.eyes.blink()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.eyes.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            self.eyes.move(5, 0)
        if keys[pygame.K_UP]:
            self.eyes.move(0, -5)
        if keys[pygame.K_DOWN]:
            self.eyes.move(0, 5)

    def update(self):
        if not self.showed_logo:
            return
        self.ghosts.update()
        self.bats.update()
        if time.time() - self.flash_time > self.skull_flash_interval:
            self.flash_skull = True
            self.flash_time = time.time()
            self.skull_flash_interval = random.randint(10, 30)

    def draw(self):
        if not self.showed_logo:
            self.screen.fill((0, 0, 0))
            logo_rect = self.logo_image.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(self.logo_image, logo_rect)
            pygame.display.flip()
            time.sleep(5)
            self.showed_logo = True
            return

        self.screen.fill((0, 0, 0))
        self.ghosts.draw(self.screen)
        self.screen.blit(self.house_image, (0, 0))
        self.screen.blit(self.eyes.image, self.eyes.rect)
        self.bats.draw(self.screen)

        if self.flash_skull:
            self.screen.blit(self.skull_image, ((self.width - self.skull_image.get_width()) // 2,
                                               (self.height - self.skull_image.get_height()) // 2))
            pygame.display.flip()
            time.sleep(0.5)
            self.flash_skull = False


if __name__ == "__main__":
    HauntedHouseScreensaver().run()
