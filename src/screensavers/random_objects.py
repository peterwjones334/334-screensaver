import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from numpy import array
from base import asset_path


class ImageSprite:
    def __init__(self, texture, size, position, velocity, angle, rotation_speed):
        self.texture = texture
        self.size = size
        self.position = position
        self.velocity = velocity
        self.angle = angle
        self.rotation_speed = rotation_speed

    def update(self, screen_width, screen_height):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.angle += self.rotation_speed
        if self.position[0] < 0 or self.position[0] + self.size[0] > screen_width:
            self.velocity[0] = -self.velocity[0]
        if self.position[1] < 0 or self.position[1] + self.size[1] > screen_height:
            self.velocity[1] = -self.velocity[1]

    def draw(self):
        half_width = self.size[0] / 2
        half_height = self.size[1] / 2
        glPushMatrix()
        glTranslatef(self.position[0] + half_width, self.position[1] + half_height, 0)
        glRotatef(self.angle, 0, 0, 1)
        glTranslatef(-half_width, -half_height, 0)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(0, 0)
        glTexCoord2f(1, 0); glVertex2f(self.size[0], 0)
        glTexCoord2f(1, 1); glVertex2f(self.size[0], self.size[1])
        glTexCoord2f(0, 1); glVertex2f(0, self.size[1])
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()


def load_texture(path):
    full = asset_path(path)
    image = Image.open(full).convert("RGBA")
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image_data = array(list(image.getdata()), dtype="uint8")
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    return texture_id, (image.width, image.height)


def draw_background(texture_id, screen_width, screen_height):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(0, 0)
    glTexCoord2f(1, 0); glVertex2f(screen_width, 0)
    glTexCoord2f(1, 1); glVertex2f(screen_width, screen_height)
    glTexCoord2f(0, 1); glVertex2f(0, screen_height)
    glEnd()
    glDisable(GL_TEXTURE_2D)


def run():
    pygame.init()
    screen_size = (1024, 768)
    pygame.display.set_mode(screen_size, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Random Objects")
    gluOrtho2D(0, screen_size[0], 0, screen_size[1])
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    background_texture, _ = load_texture("background3.png")
    image_paths = ["object1.png", "object2.png", "object3.png", "object4.png"]
    sprites = []
    for path in image_paths:
        texture, size = load_texture(path)
        position = [random.randint(0, screen_size[0] - size[0]), random.randint(0, screen_size[1] - size[1])]
        velocity = [random.choice([-1, 1]), random.choice([-1, 1])]
        angle = random.uniform(0, 360)
        rotation_speed = random.uniform(-1, 1)
        sprites.append(ImageSprite(texture, size, position, velocity, angle, rotation_speed))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_background(background_texture, screen_size[0], screen_size[1])
        for sprite in sprites:
            sprite.update(screen_size[0], screen_size[1])
            sprite.draw()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()


if __name__ == "__main__":
    run()
