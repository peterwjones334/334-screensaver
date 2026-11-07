import math
import pygame
from base import Screensaver

GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
COPPER = (184, 115, 51)
PLATINUM = (229, 228, 226)
IRON = (70, 70, 70)
WHITE = (255, 255, 255)
METAL_COLORS = [GOLD, SILVER, COPPER, PLATINUM, IRON]
METAL_NAMES = ["Gold", "Silver", "Copper", "Platinum", "Iron"]


class OneRingScreensaver(Screensaver):
    def __init__(self):
        super().__init__(title="One Ring")
        self.font = pygame.font.SysFont("Arial", 18)
        self.ring_radius = 100
        self.ring_thickness = 20
        self.camera_distance = 300
        self.camera_angle_x = 0
        self.camera_angle_y = 0
        self.rotation_speed = 1
        self.light_angle = 0
        self.light_speed = 0.01
        self.light_distance = 300
        self.current_color_index = 0

        num_points = 100
        self.ring_points = []
        for i in range(num_points):
            angle = i * 2 * math.pi / num_points
            x = self.ring_radius * math.cos(angle)
            y = self.ring_radius * math.sin(angle)
            self.ring_points.append((x, y, 0))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.camera_angle_x -= math.radians(self.rotation_speed)
                elif event.key == pygame.K_DOWN:
                    self.camera_angle_x += math.radians(self.rotation_speed)
                elif event.key == pygame.K_LEFT:
                    self.camera_angle_y -= math.radians(self.rotation_speed)
                elif event.key == pygame.K_RIGHT:
                    self.camera_angle_y += math.radians(self.rotation_speed)
                elif event.key == pygame.K_a:
                    self.light_speed += 0.01
                elif event.key == pygame.K_s:
                    self.light_speed = max(0, self.light_speed - 0.01)
                elif event.key == pygame.K_c:
                    self.current_color_index = (self.current_color_index + 1) % len(METAL_COLORS)
                else:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.running = False

    def project_3d_to_2d(self, x, y, z):
        fov = 256
        z += self.camera_distance
        if z == 0:
            z = 1
        factor = fov / z
        x = x * factor + self.width // 2
        y = -y * factor + self.height // 2
        return int(x), int(y)

    def rotate_point_around_axis(self, x, y, z, angle_x, angle_y):
        cos_y = math.cos(angle_y)
        sin_y = math.sin(angle_y)
        x, z = cos_y * x - sin_y * z, sin_y * x + cos_y * z
        cos_x = math.cos(angle_x)
        sin_x = math.sin(angle_x)
        y, z = cos_x * y - sin_x * z, sin_x * y + cos_x * z
        return x, y, z

    def calculate_light_intensity(self, point, normal, light_pos):
        light_vector = (light_pos[0] - point[0], light_pos[1] - point[1], light_pos[2] - point[2])
        light_dist = math.sqrt(sum(i ** 2 for i in light_vector))
        if light_dist == 0:
            light_dist = 1
        light_vector = [i / light_dist for i in light_vector]
        dot = sum(normal[i] * light_vector[i] for i in range(3))
        return max(0, min(1, dot))

    def update(self):
        self.light_angle += self.light_speed

    def draw(self):
        self.screen.fill((0, 0, 0))
        light_pos_x = self.light_distance * math.cos(self.light_angle)
        light_pos_y = self.light_distance * math.sin(self.light_angle)
        light_pos = (light_pos_x, light_pos_y, 0)
        metal = METAL_COLORS[self.current_color_index]

        for point in self.ring_points:
            x, y, z = self.rotate_point_around_axis(*point, self.camera_angle_x, self.camera_angle_y)
            sx, sy = self.project_3d_to_2d(x, y, z)
            normal = (x, y, z)
            ndist = math.sqrt(sum(i ** 2 for i in normal))
            if ndist == 0:
                ndist = 1
            normal = [i / ndist for i in normal]
            intensity = self.calculate_light_intensity((x, y, z), normal, light_pos)
            color = [min(255, max(0, int(metal[i] * intensity))) for i in range(3)]
            pygame.draw.circle(self.screen, color, (sx, sy), self.ring_thickness // 2)

        cam_text = f"Camera X: {math.degrees(self.camera_angle_x):.2f}°  Camera Y: {math.degrees(self.camera_angle_y):.2f}°"
        light_text = f"Light Speed: {self.light_speed:.2f}"
        metal_text = f"Metal: {METAL_NAMES[self.current_color_index]}"
        self.screen.blit(self.font.render(cam_text, True, WHITE), (10, 10))
        self.screen.blit(self.font.render(light_text, True, WHITE), (10, 30))
        self.screen.blit(self.font.render(metal_text, True, WHITE), (10, 50))


if __name__ == "__main__":
    OneRingScreensaver().run()
