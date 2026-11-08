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

Then open http://localhost:8000

## Structure

```
web/
├── index.html
├── src/
│   ├── base.js         # Screensaver base class
│   └── starfield.js    # Example port
└── README.md
```

Three.js is loaded via import map from unpkg (no build step required).

## Adding another screensaver

1. Create `src/my_saver.js` that imports `Screensaver` from `./base.js`.
2. Subclass it, implement `update(delta)`, and add objects to `this.scene`.
3. Point `index.html` at the new script (or add a simple selector).

See `../docs/porting-to-javascript.md` for the full porting guide.
