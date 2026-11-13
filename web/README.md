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
- http://localhost:8000/doomsday.html    → doomsday clock + event ticker
- http://localhost:8000/trex.html        → 3D vector T-Rex maze
- http://localhost:8000/galaxians.html   → self-playing Galaxians arcade
- http://localhost:8000/zen.html         → Japanese ornamental garden

## Structure

```
web/
├── index.html
├── haunted.html
├── asylum.html
├── boids.html
├── doomsday.html
├── trex.html
├── galaxians.html
├── zen.html
├── src/
│   ├── base.js
│   ├── starfield.js
│   ├── haunted_house.js
│   ├── asylum_aquarium.js
│   ├── boids.js
│   ├── doomsday.js
│   ├── trex_maze.js
│   ├── galaxians.js
│   └── zen_garden.js
└── README.md
```

Three.js is loaded via import map from unpkg (no build step required).

## Screensavers

- **starfield.js** — classic starfield
- **haunted_house.js** — foggy house, ghosts, bats, lightning + procedural creepy audio
- **asylum_aquarium.js** — cracked asylum tank with Dread Octopus, Mad Barracuda, and frantic Shrimpies
- **boids.js** — classic flocking rendered as green phosphor vector lines with trails and screen-burn
- **doomsday.js** — Doomsday Clock that creeps toward midnight while a scrolling ticker of global events raises the alert level
- **trex_maze.js** — 3D wireframe maze. An ASCII T-Rex hides inside. When found it roars, the screen goes red, then a new maze is generated.
- **galaxians.js** — self-playing Galaxians-style shooter. 3 levels + boss. 4 alien types plus a queen boss. Score counter, sound effects, and annoying screensaver announcements.
- **zen_garden.js** — Peaceful Japanese ornamental garden. Raked gravel, stone lantern, maple, bamboo, still pond with ripples and koi, falling leaves in the wind. Soft ambient music (click or key to start).

## Adding another screensaver

1. Create `src/my_saver.js` that imports `Screensaver` from `./base.js`.
2. Subclass it, implement `update(delta)`, and add objects to `this.scene`.
3. Point a new HTML file at the script.

See `../docs/porting-to-javascript.md` for the full porting guide.
