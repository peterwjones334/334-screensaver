import pygame
import sys
import random
import time

def main(image_path, ghost_image_paths, eyes_image_path, bat_image_path, logo_image_path, skull_image_path):
    pygame.init()

    # Define the size of the window
    window_size = (1025, 768)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Pygame PNG Image Display with Moving Ghost Sprites and Eyes")

    # Load the PNG image with transparency
    image = pygame.image.load(image_path).convert_alpha()

    # Create a sprite group for ghosts
    ghosts = pygame.sprite.Group()

    # Create a sprite class for ghost images
    class GhostSprite(pygame.sprite.Sprite):
        def __init__(self, image_path, x, y):
            super().__init__()
            self.image = pygame.image.load(image_path).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        def update(self):
            # Randomly move the ghost within a small range to create a shaky effect
            self.rect.x += random.randint(-5, 5)
            self.rect.y += random.randint(-5, 5)

            # Keep the ghosts within the window bounds
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x > window_size[0] - self.rect.width:
                self.rect.x = window_size[0] - self.rect.width

            if self.rect.y < 0:
                self.rect.y = 0
            elif self.rect.y > window_size[1] - self.rect.height:
                self.rect.y = window_size[1] - self.rect.height

    # Add ghost sprites from the provided image paths
    ghost_positions = [(256, 384), (512, 384), (600, 384)]  # Example positions
    for i, ghost_image_path in enumerate(ghost_image_paths):
        ghost = GhostSprite(ghost_image_path, *ghost_positions[i])
        ghosts.add(ghost)

    # Create a sprite for the eyes
    class EyesSprite(pygame.sprite.Sprite):
        def __init__(self, image_path, x, y):
            super().__init__()
            self.image = pygame.image.load(image_path).convert_alpha()
            self.original_image = self.image  # Store the original image for blinking
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.blinking = False

        def blink(self):
            if not self.blinking:
                self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                self.blinking = True
            else:
                self.image = self.original_image
                self.blinking = False

        def move(self, dx, dy):
            self.rect.x += dx
            self.rect.y += dy

            # Keep the eyes within the window bounds
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x > window_size[0] - self.rect.width:
                self.rect.x = window_size[0] - self.rect.width

            if self.rect.y < 0:
                self.rect.y = 0
            elif self.rect.y > window_size[1] - self.rect.height:
                self.rect.y = window_size[1] - self.rect.height

    # Initialize the eyes sprite
    eyes = EyesSprite(eyes_image_path, 512, 268)  # Example position

    # Create a sprite class for bat images
    class BatSprite(pygame.sprite.Sprite):
        def __init__(self, image_path, x, y, direction):
            super().__init__()
            self.image = pygame.image.load(image_path).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.direction = direction
            self.vertical_movement = 0

        def update(self):
            # Move the bat left or right depending on its direction
            if self.direction == "right":
                self.rect.x += 5
                if self.rect.x > window_size[0]:
                    self.rect.x = -self.rect.width
            else:
                self.rect.x -= 5
                if self.rect.x < -self.rect.width:
                    self.rect.x = window_size[0]

            # Add vertical shakiness
            self.vertical_movement += random.choice([-1, 1])
            self.rect.y += self.vertical_movement
            self.vertical_movement = -self.vertical_movement

            # Keep the bats within the top half of the window bounds
            if self.rect.y < 0:
                self.rect.y = 0
            elif self.rect.y > window_size[1] // 2 - self.rect.height:
                self.rect.y = window_size[1] // 2 - self.rect.height

    # Create bat sprites
    bats = pygame.sprite.Group()
    bat_positions = [(60, 50), (750, 100), (70, 150)]  # Example positions
    for i, position in enumerate(bat_positions):
        direction = "right" if i % 2 == 0 else "left"
        bat = BatSprite(bat_image_path, position[0], position[1], direction)
        bats.add(bat)

    # Load the logo image
    logo_image = pygame.image.load(logo_image_path).convert_alpha()

    # Load the skull image
    skull_image = pygame.image.load(skull_image_path).convert_alpha()
    skull_image = pygame.transform.scale(skull_image, (200, 200))

    # Main loop
    def show_logo():
        screen.fill((0, 0, 0))
        logo_rect = logo_image.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
        screen.blit(logo_image, logo_rect)
        pygame.display.flip()
        time.sleep(5)

    show_logo()

    running = True
    flash_skull = False
    flash_time = 0
    skull_flash_interval = random.randint(10, 30)  # Random interval for skull flash

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_b:
                    eyes.blink()

        # Get the state of all keyboard keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            eyes.move(-5, 0)
        if keys[pygame.K_RIGHT]:
            eyes.move(5, 0)
        if keys[pygame.K_UP]:
            eyes.move(0, -5)
        if keys[pygame.K_DOWN]:
            eyes.move(0, 5)

        # Clear the screen
        screen.fill((0, 0, 0))



        # Update and draw the ghost sprites behind the main image
        ghosts.update()
        ghosts.draw(screen)

        # Draw the main image with transparency
        screen.blit(image, (0, 0))

        # Draw the eyes sprite in front of the main image
        screen.blit(eyes.image, eyes.rect)

        # Update and draw the bat sprites
        bats.update()
        bats.draw(screen)

        # Check if it's time to flash the skull image
        if time.time() - flash_time > skull_flash_interval:
            flash_skull = True
            flash_time = time.time()
            skull_flash_interval = random.randint(10, 30)  # Reset interval

        # Flash the skull image for a short duration
        if flash_skull:
            screen.blit(skull_image, ((window_size[0] - skull_image.get_width()) // 2, 
                                      (window_size[1] - skull_image.get_height()) // 2))
            pygame.display.flip()
            time.sleep(0.5)
            flash_skull = False

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main('haunted_house7.png', ['ghost1.png', 'ghost2.png', 'ghost3.png'], 'eyes1.png', 'bat1.png', 'logo.png', 'skull1.png')
