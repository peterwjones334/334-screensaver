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
