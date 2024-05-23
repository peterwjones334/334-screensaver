import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random

# Initialize Pygame
pg.init()
display = (800, 600)
pg.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -20)

# Function to draw a cylinder
def draw_cylinder(radius, height, slices):
    quad = gluNewQuadric()
    gluCylinder(quad, radius, radius, height, slices, 1)

# Function to draw a torus quarter
def draw_torus_quarter(inner_radius, outer_radius, sides, rings):
    glBegin(GL_QUAD_STRIP)
    for i in range(rings+1):
        theta = i * np.pi / 2 / rings
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        for j in range(sides+1):
            phi = j * 2 * np.pi / sides
            cos_phi = np.cos(phi)
            sin_phi = np.sin(phi)
            x = (outer_radius + inner_radius * cos_phi) * cos_theta
            y = (outer_radius + inner_radius * cos_phi) * sin_theta
            z = inner_radius * sin_phi
            glVertex3f(x, y, z)
    glEnd()

# Function to draw a sphere patch
def draw_sphere_patch(radius, slices, stacks):
    for i in range(stacks//2):
        lat0 = np.pi * (-0.5 + float(i) / stacks)
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)

        lat1 = np.pi * (-0.5 + float(i + 1) / stacks)
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)

        glBegin(GL_QUAD_STRIP)
        for j in range(slices + 1):
            lng = 2 * np.pi * float(j) / slices
            x = np.cos(lng)
            y = np.sin(lng)

            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

# Define the grid size and cell size
grid_size = (12, 10, 4)
cell_size = 3.0

# Generate a random pipe configuration for each cell in the grid
def generate_pipe_configuration():
    return random.randint(0, 63)

grid = np.zeros(grid_size, dtype=int)
for x in range(grid_size[0]):
    for y in range(grid_size[1]):
        for z in range(grid_size[2]):
            grid[x, y, z] = generate_pipe_configuration()

# Function to draw the pipes based on the configuration
def draw_pipes(grid):
    for x in range(grid_size[0]):
        for y in range(grid_size[1]):
            for z in range(grid_size[2]):
                config = grid[x, y, z]
                glPushMatrix()
                glTranslatef(x * cell_size, y * cell_size, z * cell_size)
                draw_pipe(config)
                glPopMatrix()

# Function to draw a pipe segment based on its configuration
def draw_pipe(config):
    if config == 0:
        return  # Empty cell
    radius = 0.1
    length = cell_size
    if config & 1:
        glPushMatrix()
        glTranslatef(0, 0, -length/2)
        draw_cylinder(radius, length, 16)
        glPopMatrix()
    if config & 2:
        glPushMatrix()
        glRotatef(90, 1, 0, 0)
        glTranslatef(0, 0, -length/2)
        draw_cylinder(radius, length, 16)
        glPopMatrix()
    if config & 4:
        glPushMatrix()
        glRotatef(90, 0, 1, 0)
        glTranslatef(0, 0, -length/2)
        draw_cylinder(radius, length, 16)
        glPopMatrix()
    if config & 8:
        glPushMatrix()
        glRotatef(-90, 0, 1, 0)
        glTranslatef(0, 0, -length/2)
        draw_cylinder(radius, length, 16)
        glPopMatrix()
    if config & 16:
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        glTranslatef(0, 0, -length/2)
        draw_cylinder(radius, length, 16)
        glPopMatrix()
    if config & 32:
        glPushMatrix()
        glRotatef(180, 1, 0, 0)
        glTranslatef(0, 0, -length/2)
        draw_cylinder(radius, length, 16)
        glPopMatrix()

# Main loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_pipes(grid)
    pg.display.flip()
    pg.time.wait(100)

pg.quit()
