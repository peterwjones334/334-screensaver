import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cv2
import numpy as np

# Initialize Pygame and OpenGL
pygame.init()
pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
gluOrtho2D(0, 800, 0, 600)

# Load the background image
background_image = pygame.image.load('background.jpg')
background_texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, background_texture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, background_image.get_width(), background_image.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, pygame.image.tostring(background_image, "RGB", 1))
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# Load the video
video = cv2.VideoCapture('test.mp4')
ret, frame = video.read()
frame_height, frame_width, frame_channels = frame.shape
frame_texture = glGenTextures(1)

def draw_background(x, y):
    glBindTexture(GL_TEXTURE_2D, background_texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x + background_image.get_width(), y)
    glTexCoord2f(1, 1); glVertex2f(x + background_image.get_width(), y + background_image.get_height())
    glTexCoord2f(0, 1); glVertex2f(x, y + background_image.get_height())
    glEnd()

def draw_frame():
    ret, frame = video.read()
    if not ret:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = video.read()
    
    # Add alpha channel
    # alpha = np.ones((frame_height, frame_width, 1), dtype=frame.dtype) * 255
    alpha = np.ones((frame_height, frame_width, 1), dtype=frame.dtype) * 127

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    frame[:, :, 3] = alpha[:, :, 0]  # You can modify this to set different alpha values

    frame = cv2.flip(frame, 0)
    glBindTexture(GL_TEXTURE_2D, frame_texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, frame_width, frame_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, frame)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(200, 150)
    glTexCoord2f(1, 0); glVertex2f(600, 150)
    glTexCoord2f(1, 1); glVertex2f(600, 450)
    glTexCoord2f(0, 1); glVertex2f(200, 450)
    glEnd()
    
    glDisable(GL_BLEND)

x, y = 0, 0
moving_speed = 5

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= moving_speed
            if event.key == pygame.K_RIGHT:
                x += moving_speed
            if event.key == pygame.K_UP:
                y += moving_speed
            if event.key == pygame.K_DOWN:
                y -= moving_speed

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_TEXTURE_2D)

    # Draw the background
    draw_background(x, y)

    # Draw the video frame
    draw_frame()

    glDisable(GL_TEXTURE_2D)
    
    pygame.display.flip()
    clock.tick(30)

video.release()
pygame.quit()

