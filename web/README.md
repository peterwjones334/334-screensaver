# 334 Screensavers — Web / Three.js starter

Minimal browser version of the 334 screensavers.

## Run locally

Any static file server works. Examples:

```bash
# Python
cd web
python -m http.server 8000

# or Node
npx serve web
```

Then open:

- http://localhost:8000/                 → starfield
- http://localhost:8000/haunted.html     → haunted house (procedural audio)
- http://localhost:8000/asylum.html      → insane asylum aquarium
- http://localhost:8000/boids.html       → boids flocking lab experiment

## Structure

```
web/
├── index.html
├── haunted.html
├── asylum.html
├── boids.html
├── src/
│   ├── base.js
│   ├── starfield.js
│   ├── haunted_house.js
│   ├── asylum_aquarium.js
│   └── boids.js
└── README.md
```

Three.js is loaded via import map from unpkg (no build step required).

## Screensavers

- **starfield.js** — classic starfield
- **haunted_house.js** — foggy house, ghosts, bats, lightning + procedural creepy audio
- **asylum_aquarium.js** — cracked asylum tank with Dread Octopus, Mad Barracuda, and frantic Shrimpies
- **boids.js** — classic flocking (separation / alignment / cohesion) rendered as green phosphor vector lines with fading trails and a slow screen-burn overlay. Styled as a miscalculated computer-science lab experiment.

## Adding another screensaver

1. Create `src/my_saver.js` that imports `Screensaver` from `./base.js`.
2. Subclass it, implement `update(delta)`, and add objects to `this.scene`.
3. Point a new HTML file at the script.

See `../docs/porting-to-javascript.md` for the full porting guide.
