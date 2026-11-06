# 334 Screen Savers

Classic After Dark–style screensavers implemented in Pygame.

Works on Linux, Raspberry Pi OS, Windows, and macOS.

## Project Structure

```
334-screensaver/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── docs/                      # Platform setup guides and notes
├── assets/
│   ├── backgrounds/           # Background images
│   ├── sprites/               # Fish, ghosts, toasters, astronauts, etc.
│   └── media/                 # Videos and other media
├── src/
│   └── screensavers/          # Main screensaver scripts
├── tools/                     # Utility scripts (background removal, video helpers)
└── archive/                   # Older versioned experiments
```

> **Note:** Large image and video assets are currently still in the repository root. They will be moved into `assets/` in a subsequent pass. Scripts currently expect assets in the working directory; path updates will be part of the code-improvement phase.

## Prerequisites

- Python 3.8+
- Pygame

```bash
pip install -r requirements.txt
```

## Running a Screensaver

```bash
cd src/screensavers
python starfield.py          # example
```

Most scripts exit on key press, mouse button, or window close. Fullscreen and proper screensaver integration (Windows `.scr` modes, etc.) are planned improvements.

## Available Screensavers

- Starfield
- Aquarium
- Matrix / Chinese Matrix
- 2D & 3D Pipes
- Flying Toasters / Flying Appliances
- Stars, Toasters & Camels
- Bouncing / Colliding Logos
- Rotating Cube
- 3D Text
- Haunted House
- Floating Objects / Astronaut
- One Ring
- Flying Plane
- Max Headroom variants
- and others

See `src/screensavers/` for the current scripts.

## Platform Notes

Detailed setup instructions are in the `docs/` folder:

- [Windows](docs/windows.md)
- [macOS](docs/macos.md)
- [Linux / Raspberry Pi](docs/linux-raspberry-pi.md)

## License

MIT
