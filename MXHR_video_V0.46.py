import pygame
import cv2
import numpy as np
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame and OpenGL
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
gluOrtho2D(0, 800, 0, 600)
clock = pygame.time.Clock()

# Load the video
video_path = 'D:\\Process\\Project52\\Code6\\video\\black\\MH_Screentest_take2.mp4'
video = cv2.VideoCapture(video_path)
if not video.isOpened():
    print("Error: Could not open video.")
    exit()

ret, frame = video.read()
if not ret:
    print("Error: Could not read video frame.")
    exit()

frame_height, frame_width, frame_channels = frame.shape
frame_texture = glGenTextures(1)

# Color bar positions
horizontal_bars = [random.randint(0, height) for _ in range(5)]
vertical_bars = [random.randint(0, width) for _ in range(5)]

def draw_frame():
    ret, frame = video.read()
    if not ret:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = video.read()
        if not ret:
            return  # If still no frame, skip drawing

    # Convert frame to RGBA and set alpha based on a condition (e.g., color keying)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    
    # Example: make pure black pixels transparent
    black = np.all(frame[:, :, :3] == [0, 0, 0], axis=-1)
    frame[black, 3] = 0  # Set alpha to 0 for black pixels
    
    frame = cv2.flip(frame, 0)
    glBindTexture(GL_TEXTURE_2D, frame_texture)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, frame_width, frame_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, frame)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Set color to white to avoid affecting the video texture
    glColor4f(1, 1, 1, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(0, 0)
    glTexCoord2f(1, 0); glVertex2f(800, 0)
    glTexCoord2f(1, 1); glVertex2f(800, 600)
    glTexCoord2f(0, 1); glVertex2f(0, 600)
    glEnd()
    
    glDisable(GL_BLEND)
    glDisable(GL_TEXTURE_2D)

def draw_grid_and_bars(step_x, step_y, angle):
    glPushMatrix()
    glTranslatef(width // 2, height // 2, 0)
    glRotatef(angle, 0, 0, 1)
    glTranslatef(-width // 2, -height // 2, 0)
    
    # Draw grid lines
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    for x in range(0, width, step_x):
        glVertex2f(x, 0)
        glVertex2f(x, height)
    for y in range(0, height, step_y):
        glVertex2f(0, y)
        glVertex2f(width, y)
    glEnd()

    # Draw horizontal color bars
    for y in horizontal_bars:
        glColor3f(random.random(), random.random(), random.random())
        glBegin(GL_QUADS)
        glVertex2f(0, y)
        glVertex2f(width, y)
        glVertex2f(width, y + 10)
        glVertex2f(0, y + 10)
        glEnd()

    # Draw vertical color bars
    for x in vertical_bars:
        glColor3f(random.random(), random.random(), random.random())
        glBegin(GL_QUADS)
        glVertex2f(x, 0)
        glVertex2f(x + 10, 0)
        glVertex2f(x + 10, height)
        glVertex2f(x, height)
        glEnd()
    
    glPopMatrix()

def main():
    running = True
    angle = 0
    step_x, step_y = 50, 50

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update bar positions randomly
        for i in range(len(horizontal_bars)):
            horizontal_bars[i] += random.randint(-1, 1) * 5
            horizontal_bars[i] = max(0, min(height, horizontal_bars[i]))
        
        for i in range(len(vertical_bars)):
            vertical_bars[i] += random.randint(-1, 1) * 5
            vertical_bars[i] = max(0, min(width, vertical_bars[i]))

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Draw the rotating grid background with color bars
        draw_grid_and_bars(step_x, step_y, angle)
        angle += 1  # Rotate the grid

        # Draw the video frame on top of the background
        draw_frame()

        pygame.display.flip()
        clock.tick(30)

    video.release()
    pygame.quit()

if __name__ == "__main__":
    main()

