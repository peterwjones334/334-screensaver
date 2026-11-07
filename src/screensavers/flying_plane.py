import random
import pygame
from base import Screensaver, load_image


class Cloud:
    def __init__(self, image, width, height):
        self.image = image
        self.width = width
        self.height = height
        self.rect = self.image.get_rect(topleft=(width, random.randint(0, height // 2)))
        self.speed = random.uniform(1, 3)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = self.width
            self.rect.top = random.randint(0, self.height // 2)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


class FlyingPlaneScreensaver(Screensaver):
    def __init__(self):
        super().__init__(title="Flying Plane", width=1024, height=768)
        self.plane_image = load_image("plane.png")
        self.terrain_image = load_image("terrain.png")
        self.cloud_image = load_image("cloud.png")

        self.plane_rect = self.plane_image.get_rect(center=(100, self.height // 2))
        self.plane_speed = 5
        self.terrain_height = self.terrain_image.get_height()
        self.terrain_scroll_speed = 2
        self.terrain_x = 0
        self.clouds = [Cloud(self.cloud_image, self.width, self.height) for _ in range(5)]

    def handle_events(self):
        # Keep default quit behaviour, plus optional arrow-key control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.plane_rect.y -= self.plane_speed
                    elif event.key == pygame.K_DOWN:
                        self.plane_rect.y += self.plane_speed
                    elif event.key == pygame.K_LEFT:
                        self.plane_rect.x -= self.plane_speed
                    elif event.key == pygame.K_RIGHT:
                        self.plane_rect.x += self.plane_speed
                    else:
                        self.running = False
                else:
                    self.running = False
            elif event.type == pygame.VIDEORESIZE and not self.fullscreen:
                self.width, self.height = event.w, event.h
                self.screen = pygame.display.set_mode((self.width, self.height))

    def update(self):
        self.terrain_x -= self.terrain_scroll_speed
        if self.terrain_x <= -self.terrain_image.get_width():
            self.terrain_x = 0

        for cloud in self.clouds:
            cloud.update()

        if self.plane_rect.bottom > self.height - self.terrain_height:
            self.plane_rect.bottom = self.height - self.terrain_height
        self.plane_rect.clamp_ip(self.screen.get_rect())

    def draw(self):
        self.screen.fill((135, 206, 235))
        self.screen.blit(self.terrain_image, (self.terrain_x, self.height - self.terrain_height))
        self.screen.blit(self.terrain_image, (self.terrain_x + self.terrain_image.get_width(), self.height - self.terrain_height))
        for cloud in self.clouds:
            cloud.draw(self.screen)
        self.screen.blit(self.plane_image, self.plane_rect.topleft)


if __name__ == "__main__":
    FlyingPlaneScreensaver().run()
