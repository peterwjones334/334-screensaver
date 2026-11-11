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

- http://localhost:8000/          → starfield
- http://localhost:8000/haunted.html → haunted house (with procedural creepy audio)

## Structure

```
web/
├── index.html
├── haunted.html
├── src/
│   ├── base.js
│   ├── starfield.js
│   └── haunted_house.js
└── README.md
```

Three.js is loaded via import map from unpkg (no build step required).

## Haunted House

`src/haunted_house.js` is a self-contained scene:

- Foggy night with a simple house silhouette and glowing windows
- Drifting translucent ghosts
- Flying bats
- Occasional lightning flashes
- Procedural ambient loop (low drone + filtered wind noise + random creaks) generated with the Web Audio API — no external audio files needed. Click or press a key once to start audio (browser autoplay policy).

## Adding another screensaver

1. Create `src/my_saver.js` that imports `Screensaver` from `./base.js`.
2. Subclass it, implement `update(delta)`, and add objects to `this.scene`.
3. Point a new HTML file at the script (or extend the existing ones).

See `../docs/porting-to-javascript.md` for the full porting guide.
