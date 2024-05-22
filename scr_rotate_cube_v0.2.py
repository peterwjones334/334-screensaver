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

def initLighting():
    """Initialize lighting"""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, 1, 0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))

def loadTexture(image_path):
    """Load a texture for the cube"""
    textureSurface = pg.image.load(image_path)
    textureData = pg.image.tostring(textureSurface, "RGB", 1)
    width, height = textureSurface.get_size()

    glEnable(GL_TEXTURE_2D)
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture

def texturedCube(texture):
    """Render the cube with a texture"""
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    for i, quad in enumerate(cubeQuads):
        for j, vertex in enumerate(quad):
            glTexCoord2fv([(0, 0), (1, 0), (1, 1), (0, 1)][j])
            glVertex3fv(cubeVertices[vertex])
    glEnd()

def renderBackground(image_path):
    """Render the background image"""
    backgroundSurface = pg.image.load(image_path)
    bgData = pg.image.tostring(backgroundSurface, "RGB", 1)
    width, height = backgroundSurface.get_size()

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glRasterPos2i(0, 0)
    glDrawPixels(width, height, GL_RGB, GL_UNSIGNED_BYTE, bgData)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def main():
    pg.init()
    display = (800, 600)
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    initLighting()
    texture = loadTexture('square_texture1.png')
    background_image = 'background_flowers.png'

    rotate_x, rotate_y, rotate_z = 1, 1, 1
    backface_culling = False
    show_textured = True

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_LEFT:
                    rotate_y = (rotate_y - 5) % 360
                elif event.key == pg.K_RIGHT:
                    rotate_y = (rotate_y + 5) % 360
                elif event.key == pg.K_UP:
                    rotate_x = (rotate_x - 5) % 360
                elif event.key == pg.K_DOWN:
                    rotate_x = (rotate_x + 5) % 360
                elif event.key == pg.K_c:
                    backface_culling = not backface_culling
                elif event.key == pg.K_t:
                    show_textured = not show_textured

        if backface_culling:
            glEnable(GL_CULL_FACE)
        else:
            glDisable(GL_CULL_FACE)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Render the background
        renderBackground(background_image)
        
        # Restore perspective projection
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5)
        glRotatef(rotate_x, 1, 0, 0)
        glRotatef(rotate_y, 0, 1, 0)
        glRotatef(rotate_z, 0, 0, 1)

        # Automatic rotation
        rotate_x = (rotate_x + 1) % 360
        rotate_y = (rotate_y + 1) % 360
        rotate_z = (rotate_z + 1) % 360

        if show_textured:
            texturedCube(texture)
        else:
            solidCube()

        pg.display.flip()
        pg.time.wait(10)

    pg.quit()

if __name__ == "__main__":
    main()

