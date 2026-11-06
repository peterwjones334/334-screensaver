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

> **Note:** Restructuring of text files is in progress. Many main screensaver scripts have been moved into `src/screensavers/` and utilities into `tools/`. Large image and video assets remain in the repository root for now (bulk binary moves are being handled carefully). Scripts currently still expect assets in the working directory; path updates will be part of the code-improvement phase.

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
python matrix.py
python aquarium.py
python flying_toasters.py
```

Most scripts exit on key press, mouse button, or window close. Fullscreen and proper screensaver integration (Windows `.scr` modes, etc.) are planned improvements.

## Available Screensavers (moved so far)

- starfield.py
- aquarium.py
- matrix.py / chinese_matrix.py
- pipes.py
- flying_plane.py
- flying_toasters.py
- flying_appliances.py
- haunted_house.py
- and more being moved

See `src/screensavers/` for the current scripts.

## Platform Notes

Detailed setup instructions are in the `docs/` folder:

- [Windows](docs/windows.md)
- [macOS](docs/macos.md)
- [Linux / Raspberry Pi](docs/linux-raspberry-pi.md)
- [About After Dark](docs/about-afterdark.md)

## License

MIT
