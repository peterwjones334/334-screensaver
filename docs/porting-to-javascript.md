# Porting Guide: Pygame → JavaScript / WebGL / Three.js

This guide explains how to port the 334 Screen Savers from Python/Pygame to a browser-based version using JavaScript and [Three.js](https://threejs.org/).

The current architecture is a good fit for porting: most screensavers inherit from a shared `Screensaver` base class that owns the loop, events, and asset loading. The same pattern works cleanly in JavaScript.

## High-level mapping

| Pygame concept | Three.js / JS equivalent |
|----------------|---------------------------|
| `pygame.init()` + `display.set_mode()` | `new THREE.WebGLRenderer()` + `renderer.setSize()` |
| Main `while running:` loop + `clock.tick()` | `requestAnimationFrame` loop |
| `self.screen.fill()` / `blit()` | Clear colour + scene graph / sprites |
| `load_image()` | `THREE.TextureLoader` or `THREE.Sprite` |
| Event loop (`KEYDOWN`, `MOUSEBUTTONDOWN`, `QUIT`) | DOM `keydown`, `pointerdown`, `resize` listeners |
| Fullscreen | `element.requestFullscreen()` |
| Asset path helpers | Relative URLs or a small asset loader |

## Recommended project layout (JS)

```
web/
├── index.html
├── package.json          # optional (if using a bundler)
├── assets/               # same images as the Python version
├── src/
│   ├── base.js           # Screensaver base class
│   ├── starfield.js
│   ├── matrix.js
│   └── ...
└── vendor/
    └── three.min.js     # or import from CDN / npm
```

You can start with a single `index.html` + ES modules and no build step.

## Base class (JavaScript)

```javascript
// src/base.js
import * as THREE from 'three';

export class Screensaver {
  constructor({ title = '334 Screensaver', width = 800, height = 600, fullscreen = false } = {}) {
    this.width = width;
    this.height = height;
    this.fullscreen = fullscreen;
    this.running = true;

    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setSize(width, height);
    this.renderer.setClearColor(0x000000);
    document.body.appendChild(this.renderer.domElement);

    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    this.camera.position.z = 5;

    this.clock = new THREE.Clock();
    this.bindEvents();
  }

  bindEvents() {
    window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' || e.key === ' ') this.running = false;
    });
    window.addEventListener('pointerdown', () => { this.running = false; });
    window.addEventListener('resize', () => this.onResize());
  }

  onResize() {
    this.width = window.innerWidth;
    this.height = window.innerHeight;
    this.camera.aspect = this.width / this.height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(this.width, this.height);
  }

  update(delta) { /* override */ }
  draw() { /* override — or just let the scene graph do the work */ }

  run() {
    const loop = () => {
      if (!this.running) return;
      const delta = this.clock.getDelta();
      this.update(delta);
      this.draw();
      this.renderer.render(this.scene, this.camera);
      requestAnimationFrame(loop);
    };
    loop();
  }
}
```

## Porting a simple screensaver (starfield example)

Pygame version (simplified):

```python
class Star:
    def update(self, speed):
        self.z -= speed
        if self.z <= 0:
            self.reset()

    def show(self, screen):
        # project 3D → 2D and draw circle
        ...
```

Three.js version:

```javascript
// src/starfield.js
import * as THREE from 'three';
import { Screensaver } from './base.js';

class Star {
  constructor(width, height) {
    this.width = width;
    this.height = height;
    this.reset();
    // Use a Points material or a small Sprite for each star
  }

  reset() {
    this.x = Math.random() * this.width - this.width / 2;
    this.y = Math.random() * this.height - this.height / 2;
    this.z = Math.random() * this.width;
  }

  update(speed) {
    this.z -= speed;
    if (this.z <= 0) this.reset();
  }
}

export class StarfieldScreensaver extends Screensaver {
  constructor() {
    super({ title: 'Starfield' });
    this.speed = 10;
    this.stars = Array.from({ length: 400 }, () => new Star(this.width, this.height));

    // Example: one Points object for all stars (much faster)
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(this.stars.length * 3);
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const material = new THREE.PointsMaterial({ color: 0xffffff, size: 2 });
    this.points = new THREE.Points(geometry, material);
    this.scene.add(this.points);
  }

  update(delta) {
    const positions = this.points.geometry.attributes.position.array;
    this.stars.forEach((star, i) => {
      star.update(this.speed * delta * 60); // approximate original speed
      // project or just place in 3D space
      positions[i * 3] = star.x / 100;
      positions[i * 3 + 1] = star.y / 100;
      positions[i * 3 + 2] = -star.z / 100;
    });
    this.points.geometry.attributes.position.needsUpdate = true;
  }
}

// Entry point
new StarfieldScreensaver().run();
```

## Asset loading

| Pygame | Three.js |
|--------|----------|
| `load_image("toaster.png")` | `new THREE.TextureLoader().load('assets/toaster.png')` |
| `convert_alpha=True` | Texture with alpha channel (PNG) |
| Sprite blit | `THREE.Sprite` or `THREE.Mesh` with a plane |
| Background image | Full-screen plane or `scene.background = texture` |

Example sprite:

```javascript
const loader = new THREE.TextureLoader();
const texture = loader.load('assets/toaster.png');
const material = new THREE.SpriteMaterial({ map: texture });
const sprite = new THREE.Sprite(material);
scene.add(sprite);
```

## Event handling differences

- Pygame: pull events each frame with `pygame.event.get()`.
- Browser: push events. Attach listeners once in the base class (as shown above).
- Fullscreen: call `renderer.domElement.requestFullscreen()` on a key or button.
- Exit: set `this.running = false` (or remove the canvas).

## OpenGL / 3D scripts

The existing OpenGL screensavers (`3d_pipes.py`, `haunted_house_gl.py`, etc.) map more directly:

- `gluPerspective` → `PerspectiveCamera`
- Immediate-mode drawing (`glBegin`/`glVertex`) → `BufferGeometry` + `Mesh` / `Line`
- Lighting → `THREE.DirectionalLight` / `AmbientLight` + materials
- Textures → `TextureLoader`

For complex geometry (pipes, rings) prefer building a `BufferGeometry` once and updating only the matrices or a few attributes each frame.

## Performance tips

- Prefer `THREE.Points` or instanced meshes for many similar objects (stars, bubbles, fish).
- Avoid creating new objects inside the animation loop.
- Use `delta` time so speed is independent of frame rate.
- For 2D-style effects you can also use an orthographic camera and sprites.

## Minimal HTML entry point

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>334 Screensavers</title>
  <style> body { margin: 0; overflow: hidden; background: #000; } </style>
</head>
<body>
  <script type="importmap">
    { "imports": { "three": "https://unpkg.com/three@0.160.0/build/three.module.js" } }
  </script>
  <script type="module" src="src/starfield.js"></script>
</body>
</html>
```

## Next steps

1. Port `base.js` as shown above.
2. Port the simplest pure-Pygame scripts first (`starfield`, `pipes`, `flying_toasters`).
3. Add a small selector page that lists available screensavers.
4. Move the existing image assets into the `web/assets/` folder (or serve them from the same origin).

The shared `update()` / `draw()` structure makes the port mechanical for most of the existing scripts.
