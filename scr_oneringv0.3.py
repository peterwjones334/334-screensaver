import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600

# Colors
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
COPPER = (184, 115, 51)
PLATINUM = (229, 228, 226)
IRON = (70, 70, 70)
WHITE = (255, 255, 255)

# List of metal colors
metal_colors = [GOLD, SILVER, COPPER, PLATINUM, IRON]
metal_color_names = ["Gold", "Silver", "Copper", "Platinum", "Iron"]
current_color_index = 0

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("One Ring")

# Clock to control frame rate
clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.SysFont('Arial', 18)

# Ring properties
ring_radius = 100
ring_thickness = 20
center_x, center_y, center_z = 0, 0, 0

# Camera properties
camera_distance = 300
camera_angle_x = 0
camera_angle_y = 0
rotation_speed = 1

# Light source properties
light_angle = 0
light_speed = 0.01
light_distance = 300

# Define the 3D coordinates of the ring
num_points = 100
ring_points = []
for i in range(num_points):
    angle = i * 2 * math.pi / num_points
    x = ring_radius * math.cos(angle)
    y = ring_radius * math.sin(angle)
    ring_points.append((x, y, 0))

def project_3d_to_2d(x, y, z):
    fov = 256
    z += camera_distance
    if z == 0: z = 1  # Prevent division by zero
    factor = fov / z
    x = x * factor + width // 2
    y = -y * factor + height // 2
    return int(x), int(y)

def rotate_point_around_axis(x, y, z, angle_x, angle_y):
    # Rotate around Y-axis
    cos_angle_y = math.cos(angle_y)
    sin_angle_y = math.sin(angle_y)
    x, z = cos_angle_y * x - sin_angle_y * z, sin_angle_y * x + cos_angle_y * z
    
    # Rotate around X-axis
    cos_angle_x = math.cos(angle_x)
    sin_angle_x = math.sin(angle_x)
    y, z = cos_angle_x * y - sin_angle_x * z, sin_angle_x * y + cos_angle_x * z
    
    return x, y, z

def calculate_light_intensity(point, normal, light_pos):
    # Calculate vector from point to light source
    light_vector = (light_pos[0] - point[0], light_pos[1] - point[1], light_pos[2] - point[2])
    light_dist = math.sqrt(sum([i ** 2 for i in light_vector]))
    light_vector = [i / light_dist for i in light_vector]

    # Calculate dot product between normal and light vector
    dot_product = sum([normal[i] * light_vector[i] for i in range(3)])
    
    return max(0, min(1, dot_product))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                camera_angle_x -= math.radians(rotation_speed)
            elif event.key == pygame.K_DOWN:
                camera_angle_x += math.radians(rotation_speed)
            elif event.key == pygame.K_LEFT:
                camera_angle_y -= math.radians(rotation_speed)
            elif event.key == pygame.K_RIGHT:
                camera_angle_y += math.radians(rotation_speed)
            elif event.key == pygame.K_a:
                light_speed += 0.01
            elif event.key == pygame.K_s:
                light_speed = max(0, light_speed - 0.01)
            elif event.key == pygame.K_c:
                current_color_index = (current_color_index + 1) % len(metal_colors)

    screen.fill(BLACK)

    # Update light position
    light_angle += light_speed
    light_pos_x = light_distance * math.cos(light_angle)
    light_pos_y = light_distance * math.sin(light_angle)
    light_pos_z = 0

    for point in ring_points:
        x, y, z = point
        x, y, z = rotate_point_around_axis(x, y, z, camera_angle_x, camera_angle_y)
        screen_x, screen_y = project_3d_to_2d(x, y, z)

        # Calculate normal vector (assuming simple ring)
        normal = (x, y, z)
        normal_dist = math.sqrt(sum([i ** 2 for i in normal]))
        if normal_dist == 0: normal_dist = 1  # Prevent division by zero
        normal = [i / normal_dist for i in normal]

        # Calculate light intensity
        intensity = calculate_light_intensity((x, y, z), normal, (light_pos_x, light_pos_y, light_pos_z))
        color = [min(255, max(0, int(metal_colors[current_color_index][i] * intensity))) for i in range(3)]

        pygame.draw.circle(screen, color, (screen_x, screen_y), ring_thickness // 2)

    # Render the camera and light coordinates as text
    camera_coords_text = f"Camera X: {math.degrees(camera_angle_x):.2f}°  Camera Y: {math.degrees(camera_angle_y):.2f}°"
    light_coords_text = f"Light Speed: {light_speed:.2f}"
    metal_color_text = f"Metal: {metal_color_names[current_color_index]}"
    text_surface_camera = font.render(camera_coords_text, True, WHITE)
    text_surface_light = font.render(light_coords_text, True, WHITE)
    text_surface_metal = font.render(metal_color_text, True, WHITE)
    screen.blit(text_surface_camera, (10, 10))
    screen.blit(text_surface_light, (10, 30))
    screen.blit(text_surface_metal, (10, 50))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()


# Arrow keys to rotate view of ring
#  'A' and 'S' keys to adjust the light_speed.
#  'S' key cycles thru colors
