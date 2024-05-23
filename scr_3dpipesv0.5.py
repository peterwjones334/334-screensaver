import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random
import time

# Parameters
SPEED = 1  # Speed of drawing
COMPLEXITY = 1000  # Number of pipes
THICKNESS = 0.1  # Thickness of the pipes
COLORS = [
    (1.0, 0.0, 0.0),  # Red
    (0.0, 1.0, 0.0),  # Green
    (0.0, 0.0, 1.0),  # Blue
    (1.0, 1.0, 0.0),  # Yellow
    (1.0, 0.0, 1.0),  # Magenta
    (0.0, 1.0, 1.0),   # Cyan
    (1.0, 1.0, 1.0),  # White
    # (0.0, 0.0, 0.0)   # Black
]

# Initialize Pygame
pg.init()
display = (800, 600)
pg.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -20)

# Enable lighting
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_POSITION,  (0, 0, 10, 1))  # Light position
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

# Enable depth test
glEnable(GL_DEPTH_TEST)

# Function to draw a cylinder
def draw_cylinder(radius, height, slices):
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluCylinder(quad, radius, radius, height, slices, 1)

# Function to set material color
def set_material_color(color):
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (*color, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50.0)

# Define the pipe directions
directions = [
    (1, 0, 0), (-1, 0, 0),
    (0, 1, 0), (0, -1, 0),
    (0, 0, 1), (0, 0, -1)
]

# Class to represent a pipe
class Pipe:
    def __init__(self, x, y, z, direction, color, thickness):
        self.x, self.y, self.z = x, y, z
        self.direction = direction
        self.segments = []
        self.color = color
        self.thickness = thickness

    def add_segment(self, length):
        self.segments.append((self.x, self.y, self.z, self.direction, length))
        self.x += self.direction[0] * length
        self.y += self.direction[1] * length
        self.z += self.direction[2] * length

    def change_direction(self, new_direction):
        self.direction = new_direction

    def draw(self):
        set_material_color(self.color)
        for x, y, z, direction, length in self.segments:
            glPushMatrix()
            glTranslatef(x, y, z)
            if direction == (1, 0, 0):
                glRotatef(90, 0, 1, 0)
            elif direction == (-1, 0, 0):
                glRotatef(-90, 0, 1, 0)
            elif direction == (0, 1, 0):
                glRotatef(-90, 1, 0, 0)
            elif direction == (0, -1, 0):
                glRotatef(90, 1, 0, 0)
            elif direction == (0, 0, -1):
                glRotatef(180, 1, 0, 0)
            draw_cylinder(self.thickness, length, 16)
            glPopMatrix()

# Bounding box for the pipes to stay within
bounds = [-8, 8, -6, 6, -4, 4]

# Function to check if a position is within bounds
def within_bounds(x, y, z):
    return (bounds[0] <= x <= bounds[1] and
            bounds[2] <= y <= bounds[3] and
            bounds[4] <= z <= bounds[5])

# Function to create a new pipe at the end of the last segment of an existing pipe
def create_new_pipe(last_pipe):
    new_direction = random.choice(directions)
    while new_direction == last_pipe.direction or new_direction == tuple(-i for i in last_pipe.direction):
        new_direction = random.choice(directions)
    return Pipe(last_pipe.x, last_pipe.y, last_pipe.z, new_direction, random.choice(COLORS), THICKNESS)

# Function to reset the scene
def reset_scene():
    return [Pipe(0, 0, 0, random.choice(directions), random.choice(COLORS), THICKNESS)]

# Main loop
running = True
while running:
    pipes = reset_scene()
    num_pipes = 1
    start_time = time.time()
    
    while time.time() - start_time < 10:  # Draw for 10 seconds then reset
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                    break

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Draw all pipes
        for pipe in pipes:
            pipe.draw()

        # Add new segment to the last pipe
        if pipes:
            last_pipe = pipes[-1]
            if within_bounds(last_pipe.x + last_pipe.direction[0], last_pipe.y + last_pipe.direction[1], last_pipe.z + last_pipe.direction[2]):
                last_pipe.add_segment(1.0)
            else:
                if len(pipes) < COMPLEXITY:
                    pipes.append(create_new_pipe(last_pipe))
                else:
                    last_pipe.change_direction(random.choice(directions))

        # Occasionally create new pipes
        if len(pipes) < COMPLEXITY and random.random() < 0.1:
            pipes.append(create_new_pipe(random.choice(pipes)))

        pg.display.flip()
        pg.time.wait(SPEED)
    
pg.quit()
