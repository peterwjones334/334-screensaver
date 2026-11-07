# 334 Screen Savers

Classic After Dark–style screensavers implemented in Pygame (with a few OpenGL variants).

Works on Linux, Raspberry Pi OS, Windows, and macOS.

## Project Structure

```
334-screensaver/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── docs/                      # Platform setup guides and notes
├── assets/                    # (recommended) images, sprites, backgrounds, media
├── src/
│   └── screensavers/          # Main screensaver scripts + shared base
│       ├── base.py             # Shared Screensaver class and asset helper
│       ├── __init__.py
│       └── *.py                # Individual screensavers
├── tools/                     # Utility scripts (background removal, video helpers)
└── archive/                   # Older versioned experiments
```

> **Note on assets:** Large image and video files currently remain in the repository root. Scripts look for assets in `assets/` first, then fall back to the current working directory. Moving the media into `assets/` is recommended (best done with a local `git mv`).

## Prerequisites

- Python 3.8+
- Pygame

```bash
pip install -r requirements.txt
```

OpenGL scripts also need PyOpenGL (and optionally Pillow for some of them):

```bash
pip install PyOpenGL PyOpenGL-accelerate Pillow
```

## Running a Screensaver

```bash
cd src/screensavers
python starfield.py
python matrix.py
python aquarium.py
python flying_toasters.py
python haunted_house.py
# etc.
```

### Options

- Most scripts exit on any key press, mouse button, or window close.
- `--fullscreen` or `/s` enables fullscreen mode (supported by the shared base).
- Some scripts have extra keyboard controls (arrow keys, colour cycling, etc.).

### Shared base

Pure-Pygame screensavers subclass `Screensaver` from `base.py`. This provides:

- Window / fullscreen setup
- Consistent event handling and exit behaviour
- Asset path resolution via `load_image()` / `asset_path()`

OpenGL scripts keep their own context but use the same asset helper and a consistent `run()` entry point.

## Adding a New Screensaver

1. Create a new file in `src/screensavers/` (e.g. `my_screensaver.py`).
2. Subclass `Screensaver` and implement `update()` and `draw()`.
3. Load any images with `load_image()` (place files in `assets/` or the working directory).
4. Add a `if __name__ == "__main__":` block that instantiates and runs the class.

Minimal example:

```python
import random
from base import Screensaver, load_image

class MyScreensaver(Screensaver):
    def __init__(self):
        super().__init__(title="My Screensaver")
        # self.image = load_image("my_sprite.png")  # optional
        self.x = self.width // 2
        self.y = self.height // 2
        self.dx = random.choice([-3, 3])

    def update(self):
        self.x += self.dx
        if self.x < 0 or self.x > self.width:
            self.dx = -self.dx

    def draw(self):
        self.screen.fill((0, 0, 0))
        # self.screen.blit(self.image, (self.x, self.y))

if __name__ == "__main__":
    MyScreensaver().run()
```

### Tips

- Use `self.width`, `self.height`, `self.screen`, and `self.clock` from the base class.
- Override `handle_events()` only if you need custom keyboard behaviour (still call `super()` or handle quit yourself).
- For fullscreen by default: `super().__init__(..., fullscreen=True)`.
- OpenGL screensavers should create their own `DOUBLEBUF | OPENGL` context and use `asset_path()` / `load_image()` for files; see `3d_pipes.py` or `random_objects.py` for the pattern.

## Available Screensavers

### Pure Pygame
- `starfield.py`
- `flying_toasters.py` / `flying_appliances.py`
- `matrix.py` / `chinese_matrix.py`
- `pipes.py`
- `flying_plane.py`
- `aquarium.py`
- `astronaut.py`
- `haunted_house.py`
- `one_ring.py`
- `stars_toaster_camel.py`

### OpenGL
- `3d_pipes.py`
- `3d_text.py`
- `haunted_house_gl.py`
- `random_objects.py`

## Platform Notes

Detailed setup instructions are in the `docs/` folder:

- [Windows](docs/windows.md)
- [macOS](docs/macos.md)
- [Linux / Raspberry Pi](docs/linux-raspberry-pi.md)
- [About After Dark](docs/about-afterdark.md)

## License

MIT
