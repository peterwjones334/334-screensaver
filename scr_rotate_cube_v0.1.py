import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Define vertices, edges, and quads of the cube
cubeVertices = (
    (1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1),
    (-1, 1, 1), (-1, -1, -1), (-1, -1, 1), (-1, 1, -1)
)

cubeEdges = (
    (0, 1), (0, 3), (0, 4), (1, 2), (1, 7), (2, 5),
    (2, 3), (3, 6), (4, 6), (4, 7), (5, 6), (5, 7)
)

cubeQuads = (
    (0, 3, 6, 4), (2, 5, 6, 3), (1, 2, 5, 7),
    (1, 0, 4, 7), (7, 4, 6, 5), (2, 3, 0, 1)
)

# Define colors for each face of the cube
cubeColors = (
    (1, 0, 0),  # Red
    (0, 1, 0),  # Green
    (0, 0, 1),  # Blue
    (1, 1, 0),  # Yellow
    (1, 0, 1),  # Magenta
    (0, 1, 1)   # Cyan
)

def wireCube():
    """Render the cube as wireframe"""
    glBegin(GL_LINES)
    for edge in cubeEdges:
        for vertex in edge:
            glVertex3fv(cubeVertices[vertex])
    glEnd()

def solidCube():
    """Render the cube as solid with unique colors for each face"""
    glBegin(GL_QUADS)
    for i, quad in enumerate(cubeQuads):
        glColor3fv(cubeColors[i])
        for vertex in quad:
            glVertex3fv(cubeVertices[vertex])
    glEnd()

def main():
    pg.init()
    display = (800, 600)
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    rotate_x, rotate_y, rotate_z = 1, 1, 1
    backface_culling = False

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_LEFT:
                    rotate_y = (rotate_y + 5) % 360
                elif event.key == pg.K_RIGHT:
                    rotate_y = (rotate_y - 5) % 360
                elif event.key == pg.K_UP:
                    rotate_x = (rotate_x + 5) % 360
                elif event.key == pg.K_DOWN:
                    rotate_x = (rotate_x - 5) % 360
                elif event.key == pg.K_c:
                    backface_culling = not backface_culling

        if backface_culling:
            glEnable(GL_CULL_FACE)
        else:
            glDisable(GL_CULL_FACE)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(1, rotate_x, rotate_y, rotate_z)
        solidCube()
        #wireCube()  # Uncomment to see wireframe
        pg.display.flip()
        pg.time.wait(10)

    pg.quit()

if __name__ == "__main__":
    main()

