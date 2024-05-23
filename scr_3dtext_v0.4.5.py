import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image, ImageFont, ImageDraw

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TEXT = "Hello, 3D World!"
FONT_NAME = "Arial"
FONT_SIZE = 32

# Colors
BLACK = (0, 0, 0)
TEXT_COLORS = [
    (58, 255, 4),   # Bright Green
    (0, 255, 255),  # Cyan
    (255, 20, 147), # Deep Pink
    (255, 140, 0),  # Dark Orange
    (173, 255, 47), # Green Yellow
    (255, 215, 0),  # Gold
    (192, 192, 192), # Silver
    (184, 115, 51), # Copper
    (229, 228, 226), # Platinum
    (70, 70, 70), # Iron
    (255, 0, 0), # Red
    (255, 255, 1), # Yellow
    (0, 255, 0), # Green
    (238, 130, 238), # Violet
    (0, 128, 128), #Teal 
    (0, 0, 128), # Navy
    (255, 165, 0), # Orange
    (128, 0, 128), # Purple
    (255, 192, 203) # Pink
]
WHITE = (255, 255, 255)

# Global variables
rotation_angle_x = 0
rotation_angle_y = 0
scale_factor = 1.0
current_color_index = 0

def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Text Rendering with PyOpenGL and Pygame")
    return screen

def init_opengl():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (WINDOW_WIDTH / WINDOW_HEIGHT), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)

def create_text_texture(text, font_path, font_size, color):
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Error: Unable to load font {font_path}.")
        sys.exit()

    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    image = Image.new("RGBA", (text_width + 10, text_height + 10))  # Expand the box slightly
    draw = ImageDraw.Draw(image)
    draw.text((5, 5), text, font=font, fill=color)  # Adjust text position within the box

    texture_data = image.tobytes()
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_width + 10, text_height + 10, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id, text_width + 10, text_height + 10

def render_text(texture_id, text_width, text_height, scale_factor, rotation_angle_x, rotation_angle_y):
    aspect_ratio = text_width / text_height

    glPushMatrix()
    glTranslatef(-text_width / text_height / 2, -0.5, 0)  # Centering the text
    glScalef(scale_factor * aspect_ratio, scale_factor, 1.0)
    glRotatef(rotation_angle_x, 1, 0, 0)
    glRotatef(rotation_angle_y, 0, 1, 0)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0); glVertex3f(0.0, 0.0, 0.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(1.0, 0.0, 0.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(1.0, 1.0, 0.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(0.0, 1.0, 0.0)
    glEnd()
    glPopMatrix()

def render_overlay_text(screen, text, position):
    font = pygame.font.SysFont("Arial", 18)
    surface = font.render(text, True, WHITE)
    screen.blit(surface, position)

def get_font_path(font_name):
    font_path = pygame.font.match_font(font_name)
    if font_path is None:
        font_path = pygame.font.get_default_font()
    return font_path

def check_opengl_errors():
    error = glGetError()
    if error != GL_NO_ERROR:
        print(f"OpenGL error: {gluErrorString(error)}")

def handle_events():
    global rotation_angle_x, rotation_angle_y, scale_factor, current_color_index

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_LEFT:
                rotation_angle_y -= 5
            elif event.key == K_RIGHT:
                rotation_angle_y += 5
            elif event.key == K_UP:
                rotation_angle_x -= 5
            elif event.key == K_DOWN:
                rotation_angle_x += 5
            elif event.key == K_w:
                scale_factor += 0.1
            elif event.key == K_s:
                scale_factor -= 0.1
            elif event.key == K_r:  # Reset the text position and size
                rotation_angle_x = 0
                rotation_angle_y = 0
                scale_factor = 1.0
                current_color_index = 1
            elif event.key == pygame.K_c:
                current_color_index = (current_color_index + 1) % len(TEXT_COLORS)

def main():
    print("Initializing Pygame...")
    screen = init_pygame()
    print("Pygame initialized.")

    print("Initializing OpenGL...")
    init_opengl()
    check_opengl_errors()
    print("OpenGL initialized.")

    font_path = get_font_path(FONT_NAME)
    texture_id, text_width, text_height = create_text_texture(TEXT, font_path, FONT_SIZE, TEXT_COLORS[current_color_index])

    clock = pygame.time.Clock()

    while True:
        handle_events()
        
        # Update the text texture color
        texture_id, text_width, text_height = create_text_texture(TEXT, font_path, FONT_SIZE, TEXT_COLORS[current_color_index])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        check_opengl_errors()
        glLoadIdentity()
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)  # Set the camera

        # Apply transformations for the text
        glTranslatef(0.0, 0.0, -5)
        glRotatef(rotation_angle_x, 1, 0, 0)
        glRotatef(rotation_angle_y, 0, 1, 0)
        glScalef(scale_factor, scale_factor, scale_factor)

        # Render the text
        render_text(texture_id, text_width, text_height, scale_factor, rotation_angle_x, rotation_angle_y)

        screen.fill(BLACK)
        render_overlay_text(screen, f"Rotation X: {rotation_angle_x}, Rotation Y: {rotation_angle_y}, Scale: {scale_factor}", (10, 10))

        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()