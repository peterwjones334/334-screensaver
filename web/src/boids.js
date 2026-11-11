/**
 * Boids Flocking Simulator — miscalculated lab green-screen experiment.
 *
 * Pseudo-vector graphics look:
 * - Classic boids (separation / alignment / cohesion)
 * - Fading trails behind each agent
 * - Phosphor / screen-burn overlay that slowly accumulates green glow
 * - Monochrome green on black with occasional glitch flicker
 */
import * as THREE from 'three';
import { Screensaver } from './base.js';

class Boid {
  constructor() {
    this.position = new THREE.Vector3(
      (Math.random() - 0.5) * 20,
      (Math.random() - 0.5) * 12,
      (Math.random() - 0.5) * 10
    );
    this.velocity = new THREE.Vector3(
      (Math.random() - 0.5) * 2,
      (Math.random() - 0.5) * 2,
      (Math.random() - 0.5) * 2
    );
    this.acceleration = new THREE.Vector3();
    this.maxSpeed = 3.5;
    this.maxForce = 0.08;
    this.perception = 3.2;

    // Trail history
    this.trail = [];
    this.maxTrail = 18;
  }

  edges() {
    const margin = 12;
    if (this.position.x > margin) this.position.x = -margin;
    if (this.position.x < -margin) this.position.x = margin;
    if (this.position.y > margin * 0.7) this.position.y = -margin * 0.7;
    if (this.position.y < -margin * 0.7) this.position.y = margin * 0.7;
    if (this.position.z > margin * 0.6) this.position.z = -margin * 0.6;
    if (this.position.z < -margin * 0.6) this.position.z = margin * 0.6;
  }

  flock(boids) {
    const sep = this.separation(boids).multiplyScalar(1.6);
    const ali = this.alignment(boids).multiplyScalar(1.0);
    const coh = this.cohesion(boids).multiplyScalar(0.9);
    this.acceleration.add(sep).add(ali).add(coh);
  }

  separation(boids) {
    const steer = new THREE.Vector3();
    let count = 0;
    for (const other of boids) {
      const d = this.position.distanceTo(other.position);
      if (other !== this && d > 0 && d < this.perception * 0.6) {
        const diff = this.position.clone().sub(other.position);
        diff.normalize().divideScalar(d);
        steer.add(diff);
        count++;
      }
    }
    if (count > 0) {
      steer.divideScalar(count);
      steer.setLength(this.maxSpeed);
      steer.sub(this.velocity);
      steer.clampLength(0, this.maxForce);
    }
    return steer;
  }

  alignment(boids) {
    const sum = new THREE.Vector3();
    let count = 0;
    for (const other of boids) {
      const d = this.position.distanceTo(other.position);
      if (other !== this && d > 0 && d < this.perception) {
        sum.add(other.velocity);
        count++;
      }
    }
    if (count > 0) {
      sum.divideScalar(count);
      sum.setLength(this.maxSpeed);
      const steer = sum.sub(this.velocity);
      steer.clampLength(0, this.maxForce);
      return steer;
    }
    return new THREE.Vector3();
  }

  cohesion(boids) {
    const sum = new THREE.Vector3();
    let count = 0;
    for (const other of boids) {
      const d = this.position.distanceTo(other.position);
      if (other !== this && d > 0 && d < this.perception) {
        sum.add(other.position);
        count++;
      }
    }
    if (count > 0) {
      sum.divideScalar(count);
      return this.seek(sum);
    }
    return new THREE.Vector3();
  }

  seek(target) {
    const desired = target.clone().sub(this.position);
    desired.setLength(this.maxSpeed);
    const steer = desired.sub(this.velocity);
    steer.clampLength(0, this.maxForce);
    return steer;
  }

  update(delta) {
    this.velocity.add(this.acceleration);
    this.velocity.clampLength(0, this.maxSpeed);
    this.position.add(this.velocity.clone().multiplyScalar(delta * 60));
    this.acceleration.set(0, 0, 0);
    this.edges();

    // Trail
    this.trail.push(this.position.clone());
    if (this.trail.length > this.maxTrail) this.trail.shift();
  }
}

export class BoidsScreensaver extends Screensaver {
  constructor() {
    super({ title: 'Boids — Lab Experiment' });

    this.scene.background = new THREE.Color(0x001100);

    // Orthographic-ish camera for flatter vector look
    this.camera = new THREE.PerspectiveCamera(60, this.width / this.height, 0.1, 100);
    this.camera.position.set(0, 0, 22);
    this.camera.lookAt(0, 0, 0);

    this.boids = Array.from({ length: 120 }, () => new Boid());

    // Line material for trails and bodies (green phosphor)
    this.lineMat = new THREE.LineBasicMaterial({
      color: 0x33ff66,
      transparent: true,
      opacity: 0.85,
    });

    // Screen-burn overlay (accumulating green glow)
    this.burnCanvas = document.createElement('canvas');
    this.burnCanvas.width = 512;
    this.burnCanvas.height = 512;
    this.burnCtx = this.burnCanvas.getContext('2d');
    this.burnCtx.fillStyle = '#001100';
    this.burnCtx.fillRect(0, 0, 512, 512);

    this.burnTexture = new THREE.CanvasTexture(this.burnCanvas);
    this.burnPlane = new THREE.Mesh(
      new THREE.PlaneGeometry(40, 24),
      new THREE.MeshBasicMaterial({
        map: this.burnTexture,
        transparent: true,
        opacity: 0.35,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
      })
    );
    this.burnPlane.position.z = -8;
    this.scene.add(this.burnPlane);

    // Trail line objects (reused)
    this.trailLines = [];
    for (let i = 0; i < this.boids.length; i++) {
      const geo = new THREE.BufferGeometry();
      const positions = new Float32Array(this.boids[0].maxTrail * 3);
      geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      const line = new THREE.Line(geo, this.lineMat.clone());
      this.scene.add(line);
      this.trailLines.push(line);
    }

    // Simple triangular "heads" as short lines
    this.headLines = [];
    for (let i = 0; i < this.boids.length; i++) {
      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(6), 3));
      const line = new THREE.Line(geo, this.lineMat);
      this.scene.add(line);
      this.headLines.push(line);
    }

    this.glitchTimer = 0;
  }

  updateBurn() {
    const ctx = this.burnCtx;
    // Slow fade (phosphor decay)
    ctx.fillStyle = 'rgba(0, 17, 0, 0.04)';
    ctx.fillRect(0, 0, 512, 512);

    // Stamp current positions as bright green dots (burn)
    ctx.fillStyle = 'rgba(51, 255, 102, 0.15)';
    for (const boid of this.boids) {
      const x = ((boid.position.x + 12) / 24) * 512;
      const y = ((boid.position.y + 8) / 16) * 512;
      ctx.beginPath();
      ctx.arc(x, 512 - y, 1.5, 0, Math.PI * 2);
      ctx.fill();
    }
    this.burnTexture.needsUpdate = true;
  }

  update(delta) {
    const t = this.clock.elapsedTime;

    // Flock
    for (const boid of this.boids) {
      boid.flock(this.boids);
      boid.update(delta);
    }

    // Update trail lines
    for (let i = 0; i < this.boids.length; i++) {
      const boid = this.boids[i];
      const line = this.trailLines[i];
      const positions = line.geometry.attributes.position.array;
      const len = boid.trail.length;
      for (let j = 0; j < boid.maxTrail; j++) {
        const idx = j * 3;
        if (j < len) {
          const p = boid.trail[j];
          positions[idx] = p.x;
          positions[idx + 1] = p.y;
          positions[idx + 2] = p.z;
        } else {
          positions[idx] = positions[idx + 1] = positions[idx + 2] = 0;
        }
      }
      line.geometry.attributes.position.needsUpdate = true;
      line.geometry.setDrawRange(0, Math.max(2, len));

      // Head direction indicator
      const head = this.headLines[i];
      const hp = head.geometry.attributes.position.array;
      const dir = boid.velocity.clone().normalize().multiplyScalar(0.6);
      hp[0] = boid.position.x;
      hp[1] = boid.position.y;
      hp[2] = boid.position.z;
      hp[3] = boid.position.x + dir.x;
      hp[4] = boid.position.y + dir.y;
      hp[5] = boid.position.z + dir.z;
      head.geometry.attributes.position.needsUpdate = true;
    }

    // Screen burn
    this.updateBurn();

    // Occasional glitch flicker
    this.glitchTimer += delta;
    if (this.glitchTimer > 0.4 + Math.random() * 2) {
      this.lineMat.opacity = 0.4 + Math.random() * 0.6;
      this.burnPlane.material.opacity = 0.2 + Math.random() * 0.3;
      this.glitchTimer = 0;
    } else {
      this.lineMat.opacity = 0.85;
      this.burnPlane.material.opacity = 0.35;
    }

    // Slow camera drift
    this.camera.position.x = Math.sin(t * 0.05) * 2;
    this.camera.lookAt(0, 0, 0);
  }
}

// Start when loaded
new BoidsScreensaver().run();
