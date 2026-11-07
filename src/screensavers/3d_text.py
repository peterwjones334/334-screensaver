import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image, ImageFont, ImageDraw
from base import asset_path

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TEXT = "Hello, 3D World!"
FONT_NAME = "Arial"
FONT_SIZE = 32
TEXT_COLORS = [
    (58, 255, 4), (0, 255, 255), (255, 20, 147), (255, 140, 0),
    (173, 255, 47), (255, 215, 0), (192, 192, 192), (184, 115, 51),
    (229, 228, 226), (70, 70, 70), (255, 0, 0), (255, 255, 1),
    (0, 255, 0), (238, 130, 238), (0, 128, 128), (0, 0, 128),
    (255, 165, 0), (128, 0, 128), (255, 192, 203),
]
WHITE = (255, 255, 255)


def get_font_path(font_name):
    font_path = pygame.font.match_font(font_name)
    if font_path is None:
        font_path = pygame.font.get_default_font()
    return font_path


def create_text_texture(text, font_path, font_size, color):
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        print(f"Error: Unable to load font {font_path}.")
        sys.exit(1)

    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    image = Image.new("RGBA", (text_width + 10, text_height + 10))
    draw = ImageDraw.Draw(image)
    draw.text((5, 5), text, font=font, fill=color)

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
    glTranslatef(-text_width / text_height / 2, -0.5, 0)
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


def run():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Text")

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (WINDOW_WIDTH / WINDOW_HEIGHT), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    font_path = get_font_path(FONT_NAME)
    rotation_angle_x = 0
    rotation_angle_y = 0
    scale_factor = 1.0
    current_color_index = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
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
                    scale_factor = max(0.1, scale_factor - 0.1)
                elif event.key == K_r:
                    rotation_angle_x = 0
                    rotation_angle_y = 0
                    scale_factor = 1.0
                    current_color_index = 1
                elif event.key == K_c:
                    current_color_index = (current_color_index + 1) % len(TEXT_COLORS)
                else:
                    running = False
            elif event.type == MOUSEBUTTONDOWN:
                running = False

        texture_id, text_width, text_height = create_text_texture(
            TEXT, font_path, FONT_SIZE, TEXT_COLORS[current_color_index]
        )

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
        glTranslatef(0.0, 0.0, -5)
        glRotatef(rotation_angle_x, 1, 0, 0)
        glRotatef(rotation_angle_y, 0, 1, 0)
        glScalef(scale_factor, scale_factor, scale_factor)
        render_text(texture_id, text_width, text_height, scale_factor, rotation_angle_x, rotation_angle_y)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run()
