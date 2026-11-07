import time
import random
import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from base import asset_path

SPEED = 1
COMPLEXITY = 1000
THICKNESS = 0.1
COLORS = [
    (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0),
    (1.0, 1.0, 0.0), (1.0, 0.0, 1.0), (0.0, 1.0, 1.0), (1.0, 1.0, 1.0),
]
DIRECTIONS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
BOUNDS = [-8, 8, -6, 6, -4, 4]


def draw_cylinder(radius, height, slices):
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluCylinder(quad, radius, radius, height, slices, 1)


def set_material_color(color):
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (*color, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50.0)


def within_bounds(x, y, z):
    return (BOUNDS[0] <= x <= BOUNDS[1] and
            BOUNDS[2] <= y <= BOUNDS[3] and
            BOUNDS[4] <= z <= BOUNDS[5])


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


def create_new_pipe(last_pipe):
    new_direction = random.choice(DIRECTIONS)
    while new_direction == last_pipe.direction or new_direction == tuple(-i for i in last_pipe.direction):
        new_direction = random.choice(DIRECTIONS)
    return Pipe(last_pipe.x, last_pipe.y, last_pipe.z, new_direction, random.choice(COLORS), THICKNESS)


def run():
    pg.init()
    display = (800, 600)
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)
    pg.display.set_caption("3D Pipes")
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -20)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, 10, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
    glEnable(GL_DEPTH_TEST)

    running = True
    while running:
        pipes = [Pipe(0, 0, 0, random.choice(DIRECTIONS), random.choice(COLORS), THICKNESS)]
        start_time = time.time()

        while time.time() - start_time < 10 and running:
            for event in pg.event.get():
                if event.type in (pg.QUIT, pg.KEYDOWN, pg.MOUSEBUTTONDOWN):
                    if event.type == pg.KEYDOWN and event.key != pg.K_ESCAPE:
                        continue
                    running = False
                    break

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            for pipe in pipes:
                pipe.draw()

            if pipes:
                last_pipe = pipes[-1]
                if within_bounds(last_pipe.x + last_pipe.direction[0],
                                 last_pipe.y + last_pipe.direction[1],
                                 last_pipe.z + last_pipe.direction[2]):
                    last_pipe.add_segment(1.0)
                else:
                    if len(pipes) < COMPLEXITY:
                        pipes.append(create_new_pipe(last_pipe))
                    else:
                        last_pipe.change_direction(random.choice(DIRECTIONS))

            if len(pipes) < COMPLEXITY and random.random() < 0.1:
                pipes.append(create_new_pipe(random.choice(pipes)))

            pg.display.flip()
            pg.time.wait(SPEED)

    pg.quit()


if __name__ == "__main__":
    run()
