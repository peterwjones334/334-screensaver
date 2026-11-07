import random
import pygame
from base import Screensaver, load_image


class AstronautScreensaver(Screensaver):
    def __init__(self):
        super().__init__(title="Astronaut Screensaver", fullscreen=True)
        self.astronaut_img = load_image("astronaut1.png")
        self.satellite_img = load_image("satellite1.png")
        try:
            bg = load_image("space1.png", convert_alpha=False)
            self.background = pygame.transform.scale(bg, (self.width, self.height))
        except FileNotFoundError:
            self.background = None

        self.satellite_center = (self.width // 2, self.height // 2)
        self.satellite_angle = 0
        self.satellite_rotation_speed = 0.05

        self.astronaut_x = random.randint(0, self.width)
        self.astronaut_y = random.randint(0, self.height)
        self.astronaut_speed_x = random.uniform(-1, 1)
        self.astronaut_speed_y = random.uniform(-1, 1)

        self.stars = []
        for _ in range(100):
            self.stars.append([
                random.randint(0, self.width),
                random.randint(0, self.height),
                random.randint(128, 255),
                random.uniform(0.05, 0.1),
                False,
                2,
            ])

        self.nova_timer = 0
        self.nova_interval = random.randint(5000, 10000)

    def update(self):
        self.satellite_angle = (self.satellite_angle + self.satellite_rotation_speed) % 360

        self.astronaut_x += self.astronaut_speed_x
        self.astronaut_y += self.astronaut_speed_y
        aw, ah = self.astronaut_img.get_size()
        if self.astronaut_x < -aw:
            self.astronaut_x = self.width
        elif self.astronaut_x > self.width:
            self.astronaut_x = -aw
        if self.astronaut_y < -ah:
            self.astronaut_y = self.height
        elif self.astronaut_y > self.height:
            self.astronaut_y = -ah

        self.nova_timer += self.clock.get_time()
        if self.nova_timer >= self.nova_interval:
            self.nova_timer = 0
            self.nova_interval = random.randint(5000, 10000)
            star = random.choice(self.stars)
            star[4] = True

    def draw(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((0, 0, 30))

        for star in self.stars:
            star_x, star_y, brightness, twinkle_speed, is_nova, radius = star
            if is_nova:
                brightness = 255
                radius += 2
                if radius > 10:
                    star[4] = False
                    brightness = random.randint(128, 255)
                    radius = 2
            else:
                brightness += twinkle_speed
                if brightness >= 255 or brightness <= 128:
                    twinkle_speed = -twinkle_speed
            brightness = max(0, min(255, brightness))
            star[2] = brightness
            star[3] = twinkle_speed
            star[5] = radius
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (star_x, star_y), radius)

        rotated = pygame.transform.rotate(self.satellite_img, self.satellite_angle)
        rect = rotated.get_rect(center=self.satellite_center)
        self.screen.blit(rotated, rect.topleft)
        self.screen.blit(self.astronaut_img, (self.astronaut_x, self.astronaut_y))


if __name__ == "__main__":
    AstronautScreensaver().run()
