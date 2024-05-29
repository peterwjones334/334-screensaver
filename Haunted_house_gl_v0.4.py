import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import random

# Load the bitmap image with transparency
def load_texture(image_path):
    texture_surface = pygame.image.load(image_path).convert_alpha()
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
    width = texture_surface.get_width()
    height = texture_surface.get_height()

    glEnable(GL_TEXTURE_2D)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    return texture_id

# Draw the house with the texture
def draw_house(texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-1.5, -1.5, 0)
    glTexCoord2f(1, 0)
    glVertex3f(1.5, -1.5, 0)
    glTexCoord2f(1, 1)
    glVertex3f(1.5, 1.5, 0)
    glTexCoord2f(0, 1)
    glVertex3f(-1.5, 1.5, 0)
    glEnd()

# Draw a simple sphere
def draw_sphere(radius, slices, stacks):
    for i in range(slices):
        lat0 = math.pi * (-0.5 + float(i) / slices)
        z0 = radius * math.sin(lat0)
        zr0 = radius * math.cos(lat0)

        lat1 = math.pi * (-0.5 + float(i + 1) / slices)
        z1 = radius * math.sin(lat1)
        zr1 = radius * math.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(stacks + 1):
            lng = 2 * math.pi * float(j) / stacks
            x = math.cos(lng)
            y = math.sin(lng)

            glNormal3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr0, y * zr0, z0)
            glNormal3f(x * zr1, y * zr1, z1)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

# Simple animation behind the windows
def draw_animation(time):
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(0.5 * math.sin(time), 0.5 * math.cos(time), -1)
    draw_sphere(0.1, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0, 1, 0)
    glTranslatef(-0.5 * math.sin(time), -0.5 * math.cos(time), -1)
    draw_sphere(0.1, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(0.5 * math.cos(time), 0.5 * math.sin(time), -1)
    draw_sphere(0.1, 20, 20)
    glPopMatrix()

# Set up lighting
def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    light_pos = [0, 0, 5, 1]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])

# Apply lightning effect
def apply_lightning_effect(lightning, time):
    if lightning:
        intensity = 2.0 if (time % 1.0 < 0.1) else 1.0
    else:
        intensity = 1.0
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [intensity, intensity, intensity, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [intensity, intensity, intensity, 1])

# Initialize and render the scene
def render_scene(image_path):
    pygame.init()
    display = (1024, 768)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    
    texture_id = load_texture(image_path)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    
    setup_lighting()
    
    clock = pygame.time.Clock()
    time = 0
    lightning = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        time += clock.get_time() / 1000.0

        # Randomly trigger lightning
        if random.random() < 0.01:
            lightning = not lightning

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Apply lightning effect
        apply_lightning_effect(lightning, time)
        
        # Draw animation behind the house
        glPushMatrix()
        glTranslatef(0, 0, -1)
        draw_animation(time)
        glPopMatrix()
        
        # Draw the house
        glPushMatrix()
        draw_house(texture_id)
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

# Use the uploaded image file
image_path = 'haunted_house6.png'
render_scene(image_path)



