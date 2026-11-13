/**
 * Stylized Koi Pond screensaver.
 *
 * Graceful koi swimming in a clear pond with lily pads, expanding ripples,
 * soft reflections, and a calm overhead view. Peaceful to watch.
 */
import * as THREE from 'three';
import { Screensaver } from './base.js';

export class KoiPondScreensaver extends Screensaver {
  constructor() {
    super({ title: 'Koi Pond' });

    this.scene.background = new THREE.Color(0x0a1a22);
    this.scene.fog = new THREE.Fog(0x0a1a22, 15, 35);

    this.ambient = new THREE.AmbientLight(0x668899, 0.7);
    this.scene.add(this.ambient);

    this.sun = new THREE.DirectionalLight(0xffeedd, 0.6);
    this.sun.position.set(5, 10, 4);
    this.scene.add(this.sun);

    this.buildPond();
    this.buildLilyPads();
    this.buildKoi(8);
    this.buildRipples();

    // Slightly elevated looking-down camera
    this.camera.position.set(0, 8, 6);
    this.camera.lookAt(0, 0, 0);
  }

  buildPond() {
    // Water surface
    const waterGeo = new THREE.CircleGeometry(7, 48);
    const waterMat = new THREE.MeshPhongMaterial({
      color: 0x1a4a66,
      transparent: true,
      opacity: 0.65,
      shininess: 90,
      specular: 0x4488aa,
    });
    this.water = new THREE.Mesh(waterGeo, waterMat);
    this.water.rotation.x = -Math.PI / 2;
    this.water.position.y = 0.05;
    this.scene.add(this.water);

    // Pond floor (visible through water)
    const floor = new THREE.Mesh(
      new THREE.CircleGeometry(6.8, 32),
      new THREE.MeshLambertMaterial({ color: 0x2a3a2a })
    );
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = -0.4;
    this.scene.add(floor);

    // Stone rim
    const rimMat = new THREE.MeshLambertMaterial({ color: 0x555544 });
    for (let i = 0; i < 24; i++) {
      const angle = (i / 24) * Math.PI * 2;
      const stone = new THREE.Mesh(
        new THREE.CylinderGeometry(0.25, 0.3, 0.2, 6),
        rimMat
      );
      stone.position.set(Math.cos(angle) * 6.9, 0.1, Math.sin(angle) * 6.9);
      this.scene.add(stone);
    }
  }

  buildLilyPads() {
    this.pads = [];
    const padMat = new THREE.MeshLambertMaterial({ color: 0x2a6a3a, side: THREE.DoubleSide });
    for (let i = 0; i < 7; i++) {
      const pad = new THREE.Mesh(new THREE.CircleGeometry(0.45 + Math.random() * 0.3, 12), padMat);
      pad.rotation.x = -Math.PI / 2;
      const a = Math.random() * Math.PI * 2;
      const r = 1.5 + Math.random() * 4;
      pad.position.set(Math.cos(a) * r, 0.08, Math.sin(a) * r);
      pad.userData = { phase: Math.random() * Math.PI * 2 };
      this.scene.add(pad);
      this.pads.push(pad);

      // Occasional flower
      if (Math.random() > 0.5) {
        const flower = new THREE.Mesh(
          new THREE.SphereGeometry(0.12, 6, 6),
          new THREE.MeshBasicMaterial({ color: Math.random() > 0.5 ? 0xff6688 : 0xffeeaa })
        );
        flower.position.copy(pad.position);
        flower.position.y = 0.15;
        this.scene.add(flower);
      }
    }
  }

  buildKoi(count) {
    this.koi = [];
    const colors = [0xff4422, 0xffffff, 0xffaa22, 0x222222, 0xff6688];

    for (let i = 0; i < count; i++) {
      const group = new THREE.Group();

      // Body
      const body = new THREE.Mesh(
        new THREE.CapsuleGeometry(0.12, 0.55, 4, 8),
        new THREE.MeshLambertMaterial({ color: colors[i % colors.length] })
      );
      body.rotation.x = Math.PI / 2;
      group.add(body);

      // Tail
      const tail = new THREE.Mesh(
        new THREE.ConeGeometry(0.15, 0.3, 4),
        new THREE.MeshLambertMaterial({ color: colors[i % colors.length] })
      );
      tail.rotation.x = -Math.PI / 2;
      tail.position.z = -0.4;
      group.add(tail);

      // Eye
      const eye = new THREE.Mesh(
        new THREE.SphereGeometry(0.03, 6, 6),
        new THREE.MeshBasicMaterial({ color: 0x111111 })
      );
      eye.position.set(0.08, 0.05, 0.25);
      group.add(eye);

      group.position.set(
        (Math.random() - 0.5) * 8,
        -0.15,
        (Math.random() - 0.5) * 8
      );
      group.userData = {
        angle: Math.random() * Math.PI * 2,
        speed: 0.4 + Math.random() * 0.5,
        radius: 1.2 + Math.random() * 3.5,
        wobble: Math.random() * Math.PI * 2,
        turnTimer: 0,
      };
      this.scene.add(group);
      this.koi.push(group);
    }
  }

  buildRipples() {
    this.ripples = [];
    for (let i = 0; i < 6; i++) {
      const ring = new THREE.Mesh(
        new THREE.RingGeometry(0.2, 0.28, 24),
        new THREE.MeshBasicMaterial({
          color: 0xaaddff,
          transparent: true,
          opacity: 0.35,
          side: THREE.DoubleSide,
        })
      );
      ring.rotation.x = -Math.PI / 2;
      ring.position.y = 0.06;
      ring.userData = { age: Math.random() * 3, owner: Math.floor(Math.random() * 8) };
      this.scene.add(ring);
      this.ripples.push(ring);
    }
  }

  update(delta) {
    const t = this.clock.elapsedTime;

    // Slow orbiting camera
    this.camera.position.x = Math.sin(t * 0.12) * 2;
    this.camera.position.z = 6 + Math.cos(t * 0.1) * 1.5;
    this.camera.lookAt(0, 0, 0);

    // Koi swimming in gentle curves
    this.koi.forEach((k, i) => {
      const u = k.userData;
      u.angle += u.speed * delta;
      u.wobble += delta * 2;

      // Occasional direction change
      u.turnTimer -= delta;
      if (u.turnTimer <= 0) {
        u.radius = 1 + Math.random() * 4;
        u.turnTimer = 4 + Math.random() * 6;
      }

      k.position.x = Math.cos(u.angle) * u.radius;
      k.position.z = Math.sin(u.angle) * u.radius;
      k.position.y = -0.15 + Math.sin(u.wobble) * 0.04;

      // Face direction of travel
      k.rotation.y = -u.angle + Math.PI / 2;

      // Gentle body sway
      k.children[0].rotation.z = Math.sin(u.wobble * 1.5) * 0.15;
    });

    // Ripples following some koi
    this.ripples.forEach((r, i) => {
      r.userData.age += delta;
      const s = 1 + r.userData.age * 0.8;
      r.scale.set(s, s, 1);
      r.material.opacity = Math.max(0, 0.4 - r.userData.age * 0.12);

      if (r.userData.age > 3.5) {
        r.userData.age = 0;
        const owner = this.koi[r.userData.owner % this.koi.length];
        if (owner) {
          r.position.x = owner.position.x;
          r.position.z = owner.position.z;
        }
      }
    });

    // Lily pads gentle bob
    this.pads.forEach(p => {
      p.position.y = 0.08 + Math.sin(t * 0.8 + p.userData.phase) * 0.015;
    });

    // Water shimmer
    this.water.material.opacity = 0.6 + Math.sin(t * 0.5) * 0.05;
  }
}

// Start when loaded
new KoiPondScreensaver().run();
