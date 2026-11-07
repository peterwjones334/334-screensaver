import math
import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from base import asset_path, load_image


def load_texture(path):
    surface = load_image(path)
    texture_data = pygame.image.tostring(surface, "RGBA", 1)
    width, height = surface.get_size()
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    return texture_id


def draw_house(texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-1.5, -1.5, 0)
    glTexCoord2f(1, 0); glVertex3f(1.5, -1.5, 0)
    glTexCoord2f(1, 1); glVertex3f(1.5, 1.5, 0)
    glTexCoord2f(0, 1); glVertex3f(-1.5, 1.5, 0)
    glEnd()


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


def draw_animation(t):
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(0.5 * math.sin(t), 0.5 * math.cos(t), -1)
    draw_sphere(0.1, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0, 1, 0)
    glTranslatef(-0.5 * math.sin(t), -0.5 * math.cos(t), -1)
    draw_sphere(0.1, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(0.5 * math.cos(t), 0.5 * math.sin(t), -1)
    draw_sphere(0.1, 20, 20)
    glPopMatrix()


def run():
    pygame.init()
    display = (1024, 768)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Haunted House GL")
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    texture_id = load_texture("haunted_house6.png")
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 5, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])

    clock = pygame.time.Clock()
    t = 0
    lightning = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                running = False

        t += clock.get_time() / 1000.0
        if random.random() < 0.01:
            lightning = not lightning

        intensity = 2.0 if (lightning and t % 1.0 < 0.1) else 1.0
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [intensity, intensity, intensity, 1])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [intensity, intensity, intensity, 1])

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslatef(0, 0, -1)
        draw_animation(t)
        glPopMatrix()
        glPushMatrix()
        draw_house(texture_id)
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run()
