/**
 * Starfield screensaver — port of src/screensavers/starfield.py
 */
import * as THREE from 'three';
import { Screensaver } from './base.js';

class Star {
  constructor(width, height) {
    this.width = width;
    this.height = height;
    this.reset();
  }

  reset() {
    this.x = Math.random() * this.width - this.width / 2;
    this.y = Math.random() * this.height - this.height / 2;
    this.z = Math.random() * this.width + 1;
  }

  update(speed) {
    this.z -= speed;
    if (this.z <= 0) this.reset();
  }
}

export class StarfieldScreensaver extends Screensaver {
  constructor() {
    super({ title: 'Starfield Screensaver' });
    this.speed = 8;
    this.starCount = 600;

    this.stars = Array.from(
      { length: this.starCount },
      () => new Star(this.width, this.height)
    );

    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(this.starCount * 3);
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));

    const material = new THREE.PointsMaterial({
      color: 0xffffff,
      size: 2,
      sizeAttenuation: true,
    });

    this.points = new THREE.Points(geometry, material);
    this.scene.add(this.points);
  }

  update(delta) {
    const positions = this.points.geometry.attributes.position.array;
    const speed = this.speed * delta * 60;

    for (let i = 0; i < this.stars.length; i++) {
      const star = this.stars[i];
      star.update(speed);

      // Simple perspective-ish placement
      const scale = 200 / (star.z + 1);
      positions[i * 3] = (star.x / this.width) * scale;
      positions[i * 3 + 1] = (star.y / this.height) * scale;
      positions[i * 3 + 2] = -star.z / 80;
    }

    this.points.geometry.attributes.position.needsUpdate = true;
  }
}

// Start when loaded
new StarfieldScreensaver().run();
