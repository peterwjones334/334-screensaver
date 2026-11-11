/**
 * Insane Asylum Aquarium screensaver.
 *
 * A cracked tiled asylum tank filled with murky water.
 * Features:
 * - Dread Octopus (slow, tentacle-waving horror)
 * - Mad Barracuda (fast, aggressive darting)
 * - Many Shrimpies (swarm of tiny frantic shrimp)
 * - Flickering fluorescent lights, padded wall fragments, floating bubbles, and occasional "code red" flashes.
 */
import * as THREE from 'three';
import { Screensaver } from './base.js';

export class AsylumAquariumScreensaver extends Screensaver {
  constructor() {
    super({ title: 'Insane Asylum Aquarium' });

    this.scene.fog = new THREE.Fog(0x0a1a1a, 8, 35);
    this.scene.background = new THREE.Color(0x071414);

    // Lighting — sickly fluorescent + occasional red alarm
    this.ambient = new THREE.AmbientLight(0x334444, 0.5);
    this.scene.add(this.ambient);

    this.fluorescent = new THREE.PointLight(0xaaffff, 1.2, 40);
    this.fluorescent.position.set(0, 8, 0);
    this.scene.add(this.fluorescent);

    this.alarmLight = new THREE.PointLight(0xff2222, 0, 30);
    this.alarmLight.position.set(-5, 6, 5);
    this.scene.add(this.alarmLight);

    // Tank walls (tiled asylum look)
    this.buildTank();

    // Dread Octopus
    this.octopus = this.createOctopus();
    this.scene.add(this.octopus);

    // Mad Barracuda
    this.barracuda = this.createBarracuda();
    this.scene.add(this.barracuda);

    // Many Shrimpies
    this.shrimpies = this.createShrimpies(80);
    this.shrimpies.forEach(s => this.scene.add(s));

    // Bubbles
    this.bubbles = this.createBubbles(40);
    this.bubbles.forEach(b => this.scene.add(b));

    this.camera.position.set(0, 2, 14);
    this.camera.lookAt(0, 0, 0);

    this.flickerTimer = 0;
    this.alarmTimer = 0;
    this.nextAlarm = 12 + Math.random() * 15;
  }

  buildTank() {
    const tileMat = new THREE.MeshLambertMaterial({ color: 0x2a3a3a });
    const crackMat = new THREE.MeshBasicMaterial({ color: 0x111111, wireframe: true });

    // Floor
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(24, 16), tileMat);
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = -4;
    this.scene.add(floor);

    // Back wall with padded-cell style panels
    const wall = new THREE.Mesh(new THREE.PlaneGeometry(24, 12), tileMat);
    wall.position.z = -8;
    wall.position.y = 1;
    this.scene.add(wall);

    // Side walls
    const sideGeo = new THREE.PlaneGeometry(16, 12);
    const left = new THREE.Mesh(sideGeo, tileMat);
    left.rotation.y = Math.PI / 2;
    left.position.x = -12;
    left.position.y = 1;
    this.scene.add(left);

    const right = left.clone();
    right.position.x = 12;
    this.scene.add(right);

    // Floating padded fragments / restraints
    for (let i = 0; i < 6; i++) {
      const pad = new THREE.Mesh(
        new THREE.BoxGeometry(1.2, 0.8, 0.3),
        new THREE.MeshLambertMaterial({ color: 0x4a3a3a })
      );
      pad.position.set(
        (Math.random() - 0.5) * 16,
        Math.random() * 6 - 1,
        (Math.random() - 0.5) * 10
      );
      pad.rotation.set(Math.random(), Math.random(), Math.random());
      this.scene.add(pad);
    }
  }

  createOctopus() {
    const group = new THREE.Group();
    const bodyMat = new THREE.MeshLambertMaterial({ color: 0x4a2a4a });
    const tentacleMat = new THREE.MeshLambertMaterial({ color: 0x5a3a5a });

    // Body
    const body = new THREE.Mesh(new THREE.SphereGeometry(1.4, 16, 16), bodyMat);
    group.add(body);

    // Eyes (mad)
    const eyeMat = new THREE.MeshBasicMaterial({ color: 0xff4444 });
    const eye1 = new THREE.Mesh(new THREE.SphereGeometry(0.25, 8, 8), eyeMat);
    eye1.position.set(-0.5, 0.4, 1.1);
    group.add(eye1);
    const eye2 = eye1.clone();
    eye2.position.x = 0.5;
    group.add(eye2);

    // Tentacles
    this.tentacles = [];
    for (let i = 0; i < 8; i++) {
      const tentacle = new THREE.Mesh(
        new THREE.CylinderGeometry(0.08, 0.25, 4, 6),
        tentacleMat
      );
      tentacle.position.y = -1.5;
      tentacle.rotation.x = Math.PI / 2;
      tentacle.rotation.y = (i / 8) * Math.PI * 2;
      tentacle.userData = { phase: Math.random() * Math.PI * 2, speed: 0.8 + Math.random() * 0.6 };
      group.add(tentacle);
      this.tentacles.push(tentacle);
    }

    group.position.set(0, 0, -2);
    return group;
  }

  createBarracuda() {
    const group = new THREE.Group();
    const mat = new THREE.MeshLambertMaterial({ color: 0x8a9a6a });

    // Body (elongated)
    const body = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.35, 2.8, 8), mat);
    body.rotation.z = Math.PI / 2;
    group.add(body);

    // Head / snout
    const head = new THREE.Mesh(new THREE.ConeGeometry(0.3, 0.9, 8), mat);
    head.rotation.z = -Math.PI / 2;
    head.position.x = 1.6;
    group.add(head);

    // Tail
    const tail = new THREE.Mesh(new THREE.ConeGeometry(0.4, 0.8, 6), mat);
    tail.rotation.z = Math.PI / 2;
    tail.position.x = -1.6;
    group.add(tail);

    // Mad eye
    const eye = new THREE.Mesh(
      new THREE.SphereGeometry(0.12, 6, 6),
      new THREE.MeshBasicMaterial({ color: 0xffff00 })
    );
    eye.position.set(1.2, 0.15, 0.2);
    group.add(eye);

    group.position.set(-6, 1, 2);
    group.userData = {
      target: new THREE.Vector3(),
      speed: 3.5,
      nextTargetTime: 0,
    };
    return group;
  }

  createShrimpies(count) {
    const shrimpies = [];
    const mat = new THREE.MeshLambertMaterial({ color: 0xffaa77 });
    for (let i = 0; i < count; i++) {
      const shrimp = new THREE.Mesh(new THREE.CapsuleGeometry(0.06, 0.25, 4, 6), mat);
      shrimp.position.set(
        (Math.random() - 0.5) * 18,
        (Math.random() - 0.5) * 6,
        (Math.random() - 0.5) * 12
      );
      shrimp.userData = {
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 1.5,
        vz: (Math.random() - 0.5) * 2,
        wiggle: Math.random() * Math.PI * 2,
      };
      shrimpies.push(shrimp);
    }
    return shrimpies;
  }

  createBubbles(count) {
    const bubbles = [];
    const mat = new THREE.MeshBasicMaterial({
      color: 0xaaddff,
      transparent: true,
      opacity: 0.4,
    });
    for (let i = 0; i < count; i++) {
      const b = new THREE.Mesh(new THREE.SphereGeometry(0.08 + Math.random() * 0.12, 8, 8), mat);
      b.position.set(
        (Math.random() - 0.5) * 16,
        -4 + Math.random() * 2,
        (Math.random() - 0.5) * 10
      );
      b.userData = { speed: 0.8 + Math.random() * 1.2 };
      bubbles.push(b);
    }
    return bubbles;
  }

  update(delta) {
    const t = this.clock.elapsedTime;

    // Octopus tentacle waving + slow body pulse
    this.octopus.position.y = Math.sin(t * 0.4) * 0.6;
    this.octopus.rotation.y = Math.sin(t * 0.2) * 0.3;
    this.tentacles.forEach((tent, i) => {
      const u = tent.userData;
      tent.rotation.z = Math.sin(t * u.speed + u.phase) * 0.8;
      tent.rotation.x = Math.PI / 2 + Math.cos(t * u.speed * 0.7 + i) * 0.4;
    });

    // Mad Barracuda — aggressive darting
    const b = this.barracuda;
    b.userData.nextTargetTime -= delta;
    if (b.userData.nextTargetTime <= 0) {
      b.userData.target.set(
        (Math.random() - 0.5) * 14,
        (Math.random() - 0.5) * 5,
        (Math.random() - 0.5) * 8
      );
      b.userData.nextTargetTime = 1.2 + Math.random() * 2.5;
    }
    const dir = b.userData.target.clone().sub(b.position);
    if (dir.length() > 0.5) {
      dir.normalize();
      b.position.add(dir.multiplyScalar(b.userData.speed * delta));
      b.lookAt(b.position.clone().add(dir));
    }

    // Shrimpies frenzy
    this.shrimpies.forEach(s => {
      const u = s.userData;
      s.position.x += u.vx * delta;
      s.position.y += u.vy * delta;
      s.position.z += u.vz * delta;
      // bounce in tank
      if (Math.abs(s.position.x) > 10) u.vx *= -1;
      if (s.position.y > 4 || s.position.y < -3) u.vy *= -1;
      if (Math.abs(s.position.z) > 6) u.vz *= -1;
      // wiggle
      s.rotation.z = Math.sin(t * 12 + u.wiggle) * 0.4;
      // occasional panic burst
      if (Math.random() < 0.005) {
        u.vx = (Math.random() - 0.5) * 4;
        u.vy = (Math.random() - 0.5) * 3;
        u.vz = (Math.random() - 0.5) * 4;
      }
    });

    // Bubbles rise
    this.bubbles.forEach(b => {
      b.position.y += b.userData.speed * delta;
      if (b.position.y > 6) {
        b.position.y = -4;
        b.position.x = (Math.random() - 0.5) * 16;
        b.position.z = (Math.random() - 0.5) * 10;
      }
    });

    // Fluorescent flicker
    this.flickerTimer += delta;
    if (this.flickerTimer > 0.08) {
      this.fluorescent.intensity = 0.7 + Math.random() * 0.8;
      this.flickerTimer = 0;
    }

    // Occasional code-red alarm flash
    this.alarmTimer += delta;
    if (this.alarmTimer > this.nextAlarm) {
      this.alarmLight.intensity = 4;
      this.ambient.color.setHex(0x442222);
      setTimeout(() => {
        if (!this.running) return;
        this.alarmLight.intensity = 0;
        this.ambient.color.setHex(0x334444);
      }, 150 + Math.random() * 200);
      this.alarmTimer = 0;
      this.nextAlarm = 10 + Math.random() * 18;
    }

    // Slow camera drift
    this.camera.position.x = Math.sin(t * 0.12) * 3;
    this.camera.position.y = 2 + Math.sin(t * 0.08) * 0.8;
    this.camera.lookAt(0, 0, 0);
  }
}

// Start when loaded
new AsylumAquariumScreensaver().run();
