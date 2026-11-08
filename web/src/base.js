/**
 * Shared base for 334 screensavers (Three.js / WebGL).
 *
 * Subclass and override update(delta). Call run() to start.
 */
import * as THREE from 'three';

export class Screensaver {
  constructor({
    title = '334 Screensaver',
    width = window.innerWidth,
    height = window.innerHeight,
    fullscreen = false,
  } = {}) {
    this.width = width;
    this.height = height;
    this.fullscreen = fullscreen;
    this.running = true;
    this.title = title;

    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setPixelRatio(window.devicePixelRatio);
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
      if (e.key === 'Escape' || e.key === ' ') {
        this.running = false;
      }
    });
    window.addEventListener('pointerdown', () => {
      this.running = false;
    });
    window.addEventListener('resize', () => this.onResize());
  }

  onResize() {
    this.width = window.innerWidth;
    this.height = window.innerHeight;
    this.camera.aspect = this.width / this.height;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(this.width, this.height);
  }

  /** Override: advance simulation. delta is in seconds. */
  update(delta) {}

  /** Override if you need custom drawing beyond the scene graph. */
  draw() {}

  run() {
    const loop = () => {
      if (!this.running) {
        this.renderer.domElement.remove();
        return;
      }
      const delta = this.clock.getDelta();
      this.update(delta);
      this.draw();
      this.renderer.render(this.scene, this.camera);
      requestAnimationFrame(loop);
    };
    loop();
  }
}
