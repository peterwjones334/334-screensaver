"""Shared base for 334 screensavers.

Provides asset path resolution and a simple Screensaver base class that
handles window creation, event loop, and clean exit.
"""

import os
import sys
import pygame


def find_assets_dir() -> str:
    """Locate the assets directory relative to this package or the repo root."""
    # Prefer assets/ next to src/
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.abspath(os.path.join(here, "..", "..", "assets")),  # src/screensavers -> repo/assets
        os.path.abspath(os.path.join(here, "..", "assets")),        # fallback
        os.path.abspath(os.path.join(os.getcwd(), "assets")),
        os.getcwd(),  # last resort: current dir (legacy behaviour)
    ]
    for path in candidates:
        if os.path.isdir(path):
            return path
    return candidates[0]


ASSETS_DIR = find_assets_dir()


def asset_path(*parts: str) -> str:
    """Return an absolute path inside the assets directory."""
    return os.path.join(ASSETS_DIR, *parts)


def load_image(*parts: str, convert_alpha: bool = True) -> pygame.Surface:
    """Load an image from the assets directory.

    Examples:
        load_image("toaster.png")
        load_image("sprites", "toaster.png")
    """
    path = asset_path(*parts)
    if not os.path.exists(path):
        # Fallback to bare filename in cwd for transition period
        fallback = os.path.join(os.getcwd(), parts[-1])
        if os.path.exists(fallback):
            path = fallback
        else:
            raise FileNotFoundError(f"Asset not found: {path}")
    img = pygame.image.load(path)
    return img.convert_alpha() if convert_alpha else img.convert()


class Screensaver:
    """Base class for a screensaver.

    Subclass and override update() and draw(). Call run() to start.
    """

    def __init__(self, title: str = "334 Screensaver", width: int = 800, height: int = 600, fullscreen: bool = False, fps: int = 60):
        pygame.init()
        self.width = width
        self.height = height
        self.fullscreen = fullscreen or "--fullscreen" in sys.argv or "/s" in sys.argv
        flags = pygame.FULLSCREEN if self.fullscreen else 0
        self.screen = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True
        self.title = title

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.running = False
            elif event.type == pygame.VIDEORESIZE and not self.fullscreen:
                self.width, self.height = event.w, event.h
                self.screen = pygame.display.set_mode((self.width, self.height))

    def update(self) -> None:
        """Override: update simulation state."""
        pass

    def draw(self) -> None:
        """Override: draw the current frame."""
        pass

    def run(self) -> None:
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()
