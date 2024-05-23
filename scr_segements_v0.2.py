import numpy as np
import math
import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Define the VertexAttributes class to store vertex attributes
class VertexAttributes:
    def __init__(self):
        self.S = 0.0
        self.T = 0.0
        self.NX = 0.0
        self.NY = 0.0
        self.NZ = 0.0
        self.X = 0.0
        self.Y = 0.0
        self.Z = 0.0

# Define the LodEntry class to store LOD information
class LodEntry:
    def __init__(self):
        self.start = 0
        self.count = 0

# Define the Model class to store the model data
class Model:
    def __init__(self, va, indexArray, lod):
        self.va = va
        self.indexArray = indexArray
        self.lod = lod

# Function to generate arches
def generate_arches(radius, slicesLod, archStacksLod):
    lod = [LodEntry() for _ in range(len(slicesLod))]
    totalVertices = 0
    totalIndices = 0

    for level in range(len(slicesLod)):
        sl = slicesLod[level]
        st = max(3, archStacksLod[level])  # Ensure minimum stacks of 3
        vertices = (sl + 1) * (st + 1)
        indices = ((sl + 1) * 2 + 4) * st - 4
        lod[level].start = totalIndices
        totalVertices += vertices
        totalIndices += indices
        lod[level].count = indices

    indexArray = np.zeros(totalIndices, dtype=int)
    va = [VertexAttributes() for _ in range(totalVertices)]

    vCounter = 0  # Index for vertices
    iCounter = 0  # Indices counter

    for level in range(len(slicesLod)):
        iOffset = vCounter
        slices = slicesLod[level]
        stacks = max(3, archStacksLod[level])

        for st in range(stacks + 1):
            a = math.pi * 0.5 * st / stacks
            texCoordS = st / float(stacks)

            for sl in range(slices + 1):
                b = math.pi * 2 * sl / slices
                texCoordT = sl / float(slices)
                va[vCounter].S = texCoordS
                va[vCounter].T = texCoordT

                # Point on central arch
                x0 = 0.5 * math.sin(a)
                y0 = 0.5 * math.cos(a)
                z0 = 0

                # Point displacement
                rx = radius * math.sin(a) * math.sin(b)
                ry = radius * math.cos(a) * math.sin(b)
                rz = radius * math.cos(b)

                # Normal factor
                nf = 1.0 / math.sqrt(rx * rx + ry * ry + rz * rz)
                va[vCounter].NX = float(rx * nf)
                va[vCounter].NY = float(ry * nf)
                va[vCounter].NZ = float(rz * nf)

                # Position
                va[vCounter].X = float(x0 + rx)
                va[vCounter].Y = float(y0 + ry)
                va[vCounter].Z = float(z0 + rz)
                vCounter += 1

        for stack in range(stacks):
            for slice in range(slices + 1):
                indexArray[iCounter] = iOffset + stack * slices + slice + stack
                iCounter += 1
                indexArray[iCounter] = iOffset + (stack + 1) * slices + slice + 1 + stack
                iCounter += 1
            if stack < stacks - 1:
                indexArray[iCounter] = iOffset + stack * slices + slices + stack
                iCounter += 1
                indexArray[iCounter] = iOffset + stack * slices + slices + stack
                iCounter += 1
                indexArray[iCounter] = iOffset + (stack + 1) * slices + slices + 2 * (stack + 1) - stack
                iCounter += 1
                indexArray[iCounter] = iOffset + (stack + 1) * slices + slices + 2 * (stack + 1) - stack
                iCounter += 1

    return Model(va, indexArray, lod)

# Function to generate cylinders
def generate_cylinders(radius, slicesLod, cylStacksLod):
    lod = [LodEntry() for _ in range(len(slicesLod))]
    totalVertices = 0
    totalIndices = 0

    for level in range(len(slicesLod)):
        sl = slicesLod[level]
        st = cylStacksLod[level]
        vertices = (sl + 1) * (st + 1)
        indices = ((sl + 1) * 2 + 4) * st - 4
        lod[level].start = totalIndices
        totalVertices += vertices
        totalIndices += indices
        lod[level].count = indices

    indexArray = np.zeros(totalIndices, dtype=int)
    va = [VertexAttributes() for _ in range(totalVertices)]

    vCounter = 0  # Index for vertex attributes
    iCounter = 0  # Indices counter

    for level in range(len(slicesLod)):
        iOffset = vCounter
        slices = slicesLod[level]
        stacks = cylStacksLod[level]

        for st in range(stacks + 1):
            i = 0.5 - 0.5 * st / stacks
            texCoordS = st / float(stacks)

            for sl in range(slices + 1):
                b = math.pi * 2 * sl / slices
                texCoordT = sl / float(slices)
                va[vCounter].S = 0.5 * texCoordS
                va[vCounter].T = texCoordT

                # Point on central axis
                x0 = 0
                y0 = 0
                z0 = i

                # Point displacement
                rx = radius * math.cos(b)
                ry = radius * math.sin(b)
                rz = 0

                # Normal factor
                nf = 1.0 / math.sqrt(ry * ry + rx * rx)
                va[vCounter].NX = float(rx * nf)
                va[vCounter].NY = float(ry * nf)
                va[vCounter].NZ = 0.0

                va[vCounter].X = float(x0 + rx)
                va[vCounter].Y = float(y0 + ry)
                va[vCounter].Z = float(z0 + rz)

                vCounter += 1

        for stack in range(stacks):
            for slice in range(slices + 1):
                indexArray[iCounter] = iOffset + stack * slices + slice + stack
                iCounter += 1
                indexArray[iCounter] = iOffset + (stack + 1) * slices + slice + 1 + stack
                iCounter += 1
            if stack < stacks - 1:
                indexArray[iCounter] = iOffset + stack * slices + slices + stack
                iCounter += 1
                indexArray[iCounter] = iOffset + stack * slices + slices + stack
                iCounter += 1
                indexArray[iCounter] = iOffset + (stack + 1) * slices + slices + 2 * (stack + 1) - stack
                iCounter += 1
                indexArray[iCounter] = iOffset + (stack + 1) * slices + slices + 2 * (stack + 1) - stack
                iCounter += 1

    return Model(va, indexArray, lod)

def R0(slices, level):
    return level * (slices + 2) - int(0.5 * level * (level + 1))

def RL(slices, level):
    return slices - level + 1

# Function to generate sphere segments
def generate_sphere_segment(radius, slicesLod):
    lod = [LodEntry() for _ in range(len(slicesLod))]
    totalVertices = 0
    totalIndices = 0

    for level in range(len(slicesLod)):
        sl = slicesLod[level] >> 2
        vertices = (((2 + sl) * (sl + 1)) >> 1)
        indices = sl * (sl + 3)
        lod[level].start = totalIndices
        totalVertices += vertices
        totalIndices += indices
        lod[level].count = indices

    indexArray = np.zeros(totalIndices, dtype=int)
    va = [VertexAttributes() for _ in range(totalVertices)]

    vCounter = 0  # Index for vertices
    iCounter = 0  # Indices counter

    for level in range(len(slicesLod)):
        sphSlices = slicesLod[level] >> 2
        iOffset = vCounter  # Index offset for level

        for sl in range(sphSlices + 1):
            a = math.pi * sl * 0.5 / sphSlices
            Y = radius * math.sin(a)
            Ry = radius * math.cos(a)

            for st in range(sphSlices - sl + 1):
                if sphSlices > sl:
                    b = math.pi * 0.5 * st / (sphSlices - sl)
                    X = Ry * math.sin(b)
                    Z = Ry * math.cos(b)
                else:
                    X = 0
                    Z = 0
                    b = 0

                va[vCounter].S = float(0.5 / 3 * a)
                va[vCounter].T = float(0.14 * b)
                coeff = 1 / math.sqrt(X * X + Y * Y + Z * Z)
                va[vCounter].NX = float(X * coeff)
                va[vCounter].NY = float(Y * coeff)
                va[vCounter].NZ = float(Z * coeff)
                va[vCounter].X = float(va[vCounter].NX * radius)
                va[vCounter].Y = float(va[vCounter].NY * radius)
                va[vCounter].Z = float(va[vCounter].NZ * radius)
                vCounter += 1

        for k in range(sphSlices):
            lastS = RL(sphSlices, k)

            for s in range(lastS - 1):
                c0 = R0(sphSlices, k) + s
                cn = R0(sphSlices, k) + s + RL(sphSlices, k)
                indexArray[iCounter] = cn + iOffset
                iCounter += 1
                indexArray[iCounter] = c0 + iOffset
                iCounter += 1

            tail = R0(sphSlices, k) + lastS - 1
            indexArray[iCounter] = tail + iOffset
            iCounter += 1
            indexArray[iCounter] = tail + iOffset
            iCounter += 1

    return Model(va, indexArray, lod)

# Example slices and stacks for LOD
slicesLod = [10, 20, 30]
archStacksLod = [5, 10, 15]
cylStacksLod = [5, 10, 15]

# Initialize Pygame
pg.init()
display = (800, 600)
pg.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Enable lighting
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
light_position = [1.0, 1.0, 1.0, 0.0]
glLightfv(GL_LIGHT0, GL_POSITION, light_position)
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.7, 0.7, 0.7, 1.0))
glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

# Set material properties
glMaterialfv(GL_FRONT, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

# Enable depth test
glEnable(GL_DEPTH_TEST)

# Create models
models = {
    "arches": generate_arches(1.0, slicesLod, archStacksLod),
    "cylinders": generate_cylinders(1.0, slicesLod, cylStacksLod),
    "sphere": generate_sphere_segment(1.0, slicesLod)
}

# Current visualization
current_model = "arches"

# Rotation angles
angle_x, angle_y = 0, 0

def draw_model(model):
    glBegin(GL_TRIANGLES)
    for i in model.indexArray:
        v = model.va[i]
        glNormal3f(v.NX, v.NY, v.NZ)
        glVertex3f(v.X, v.Y, v.Z)
    glEnd()

# Main loop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_1:
                current_model = "arches"
            elif event.key == pg.K_2:
                current_model = "cylinders"
            elif event.key == pg.K_3:
                current_model = "sphere"
            elif event.key == pg.K_UP:
                angle_x -= 5
            elif event.key == pg.K_DOWN:
                angle_x += 5
            elif event.key == pg.K_LEFT:
                angle_y -= 5
            elif event.key == pg.K_RIGHT:
                angle_y += 5
            elif event.key == pg.K_w:
                light_position[1] += 0.1
            elif event.key == pg.K_s:
                light_position[1] -= 0.1
            elif event.key == pg.K_a:
                light_position[0] -= 0.1
            elif event.key == pg.K_d:
                light_position[0] += 0.1
            elif event.key == pg.K_z:
                light_position[2] += 0.1
            elif event.key == pg.K_x:
                light_position[2] -= 0.1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    draw_model(models[current_model])
    pg.display.flip()
    pg.time.wait(10)

pg.quit()

# Switch Visualization: Use keys 1, 2, and 3 to switch between arches, cylinders, and sphere segments
# Rotation: The model can be rotated using the arrow keys.
# Light Movement: The light source can be moved using the W, A, S, D, Z, and X keys.
# 