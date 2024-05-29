import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from numpy import array

def loadTexture(texture):
    try:
        text = Image.open(texture)
    except IOError as ex:
        print("Failed to open texture file: ", texture)
        text = Image.open("default.png")

    text = text.transpose(Image.FLIP_TOP_BOTTOM)
    textData = array(list(text.getdata()), dtype='uint8')
    textID = glGenTextures(1)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glBindTexture(GL_TEXTURE_2D, textID)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text.size[0], text.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, textData)
    text.close()
    return textID, text.size

def drawQuad(centerX, centerY, textureID, width, height):
    halfWidth = width / 2
    halfHeight = height / 2
    verts = (
        (centerX - halfWidth, centerY - halfHeight),
        (centerX + halfWidth, centerY - halfHeight),
        (centerX + halfWidth, centerY + halfHeight),
        (centerX - halfWidth, centerY + halfHeight)
    )
    texts = ((0, 0), (1, 0), (1, 1), (0, 1))

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textureID)

    glBegin(GL_QUADS)
    for i in range(4):
        glTexCoord2f(texts[i][0], texts[i][1])
        glVertex2f(verts[i][0], verts[i][1])
    glEnd()
    
    glDisable(GL_TEXTURE_2D)

def main():
    pygame.init()
    disp = (1024, 768)
    pygame.display.set_mode(disp, DOUBLEBUF | OPENGL)
    gluOrtho2D(0, disp[0], 0, disp[1])
    glTranslatef(0.0, 0.0, 0.0)
    
    textureID, (texWidth, texHeight) = loadTexture("/mnt/data/image.png")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        drawQuad(disp[0] / 2, disp[1] / 2, textureID, texWidth, texHeight)
        pygame.display.flip()
        pygame.time.wait(10)
        
main()
