import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flying Plane")

# Load images
plane_image_path = "plane.png"
terrain_image_path = "terrain.png"
cloud_image_path = "cloud.png"

if os.path.exists(plane_image_path):
    plane_image = pygame.image.load(plane_image_path).convert_alpha()
else:
    print("Plane image not found.")
    exit()

if os.path.exists(terrain_image_path):
    terrain_image = pygame.image.load(terrain_image_path).convert_alpha()
else:
    print("Terrain image not found.")
    exit()

if os.path.exists(cloud_image_path):
    cloud_image = pygame.image.load(cloud_image_path).convert_alpha()
else:
    print("Cloud image not found.")
    exit()

# Colors
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)

# Plane settings
plane_rect = plane_image.get_rect(center=(100, HEIGHT // 2))
plane_speed = 5

# Terrain settings
terrain_height = terrain_image.get_height()
terrain_rect = terrain_image.get_rect(topleft=(0, HEIGHT - terrain_height))
terrain_scroll_speed = 2

# Cloud settings
class Cloud:
    def __init__(self):
        self.image = cloud_image
        self.rect = self.image.get_rect(topleft=(WIDTH, random.randint(0, HEIGHT // 2)))
        self.speed = random.uniform(1, 3)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = WIDTH
            self.rect.top = random.randint(0, HEIGHT // 2)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

clouds = [Cloud() for _ in range(5)]

# Main loop
def main():
    running = True
    clock = pygame.time.Clock()
    
    terrain_x = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    plane_rect.y -= plane_speed
                elif event.key == pygame.K_DOWN:
                    plane_rect.y += plane_speed
                elif event.key == pygame.K_LEFT:
                    plane_rect.x -= plane_speed
                elif event.key == pygame.K_RIGHT:
                    plane_rect.x += plane_speed
        
        # Scroll terrain
        terrain_x -= terrain_scroll_speed
        if terrain_x <= -terrain_image.get_width():
            terrain_x = 0
        
        # Update clouds
        for cloud in clouds:
            cloud.update()
        
        # Check for collision with terrain
        if plane_rect.bottom > HEIGHT - terrain_height:
            plane_rect.bottom = HEIGHT - terrain_height
        
        # Ensure the plane stays within the screen boundaries
        plane_rect.clamp_ip(screen.get_rect())

        # Draw everything
        screen.fill(SKY_BLUE)
        screen.blit(terrain_image, (terrain_x, HEIGHT - terrain_height))
        screen.blit(terrain_image, (terrain_x + terrain_image.get_width(), HEIGHT - terrain_height))
        for cloud in clouds:
            cloud.draw(screen)
        screen.blit(plane_image, plane_rect.topleft)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
