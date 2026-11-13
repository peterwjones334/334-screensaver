/**
 * Japanese Ornamental Garden — Shinto Zen screensaver.
 *
 * Precise natural composition: raked gravel, still pond with gentle ripples,
 * stone lantern, maple, bamboo, and soft wind. Ambient music generated
 * with the Web Audio API for a calm, joyful listening experience.
 */
import * as THREE from 'three';
import { Screensaver } from './base.js';

export class ZenGardenScreensaver extends Screensaver {
  constructor() {
    super({ title: 'Zen Garden' });

    this.scene.background = new THREE.Color(0x1a1a22);
    this.scene.fog = new THREE.Fog(0x1a1a22, 12, 40);

    // Soft ambient + warm lantern light
    this.ambient = new THREE.AmbientLight(0x445566, 0.6);
    this.scene.add(this.ambient);

    this.lanternLight = new THREE.PointLight(0xffaa66, 1.4, 12);
    this.lanternLight.position.set(-2.2, 1.8, 1.5);
    this.scene.add(this.lanternLight);

    this.moonLight = new THREE.DirectionalLight(0xaaccff, 0.4);
    this.moonLight.position.set(8, 12, 6);
    this.scene.add(this.moonLight);

    this.buildGarden();
    this.buildWater();
    this.buildWindElements();

    this.camera.position.set(0, 3.2, 10);
    this.camera.lookAt(0, 0.5, 0);

    this.audioCtx = null;
    this.musicNodes = [];
    this.setupMusicOnInteraction();

    this.windPhase = 0;
  }

  buildGarden() {
    // Raked gravel ground
    const gravel = new THREE.Mesh(
      new THREE.PlaneGeometry(24, 16),
      new THREE.MeshLambertMaterial({ color: 0x8a8070 })
    );
    gravel.rotation.x = -Math.PI / 2;
    this.scene.add(gravel);

    // Subtle rake lines (thin boxes)
    for (let i = -8; i <= 8; i += 0.6) {
      const line = new THREE.Mesh(
        new THREE.BoxGeometry(16, 0.01, 0.04),
        new THREE.MeshBasicMaterial({ color: 0x6a6050 })
      );
      line.position.set(0, 0.01, i);
      this.scene.add(line);
    }

    // Stone lantern (tōrō)
    const stoneMat = new THREE.MeshLambertMaterial({ color: 0x666666 });
    const base = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.6, 0.3, 8), stoneMat);
    base.position.set(-2.2, 0.15, 1.5);
    this.scene.add(base);

    const post = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 1.2, 8), stoneMat);
    post.position.set(-2.2, 0.9, 1.5);
    this.scene.add(post);

    const roof = new THREE.Mesh(new THREE.ConeGeometry(0.55, 0.4, 6), stoneMat);
    roof.position.set(-2.2, 1.7, 1.5);
    this.scene.add(roof);

    // Glowing lantern chamber
    const chamber = new THREE.Mesh(
      new THREE.BoxGeometry(0.35, 0.35, 0.35),
      new THREE.MeshBasicMaterial({ color: 0xffcc88 })
    );
    chamber.position.set(-2.2, 1.15, 1.5);
    this.scene.add(chamber);

    // Maple tree (simple)
    const trunk = new THREE.Mesh(
      new THREE.CylinderGeometry(0.12, 0.18, 2.2, 6),
      new THREE.MeshLambertMaterial({ color: 0x4a3020 })
    );
    trunk.position.set(3.5, 1.1, -1);
    this.scene.add(trunk);

    const foliage = new THREE.Mesh(
      new THREE.SphereGeometry(1.4, 8, 6),
      new THREE.MeshLambertMaterial({ color: 0xaa3322 })
    );
    foliage.position.set(3.5, 2.6, -1);
    this.scene.add(foliage);
    this.maple = foliage;

    // Bamboo cluster
    this.bamboo = new THREE.Group();
    for (let i = 0; i < 7; i++) {
      const stalk = new THREE.Mesh(
        new THREE.CylinderGeometry(0.04, 0.05, 3 + Math.random(), 5),
        new THREE.MeshLambertMaterial({ color: 0x3a6a3a })
      );
      stalk.position.set(
        -4 + Math.random() * 1.5,
        1.5,
        -2 + Math.random() * 2
      );
      stalk.userData.phase = Math.random() * Math.PI * 2;
      this.bamboo.add(stalk);
    }
    this.scene.add(this.bamboo);

    // Stepping stones
    const stoneColor = new THREE.MeshLambertMaterial({ color: 0x555555 });
    [[0, 0.05, 2], [0.8, 0.05, 1.2], [-0.6, 0.05, 0.4]].forEach(pos => {
      const stone = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.4, 0.08, 7), stoneColor);
      stone.position.set(...pos);
      this.scene.add(stone);
    });
  }

  buildWater() {
    // Pond
    const pondGeo = new THREE.CircleGeometry(3.2, 32);
    const pondMat = new THREE.MeshPhongMaterial({
      color: 0x224466,
      transparent: true,
      opacity: 0.75,
      shininess: 80,
    });
    this.pond = new THREE.Mesh(pondGeo, pondMat);
    this.pond.rotation.x = -Math.PI / 2;
    this.pond.position.y = 0.02;
    this.scene.add(this.pond);

    // Ripple rings (animated)
    this.ripples = [];
    for (let i = 0; i < 4; i++) {
      const ring = new THREE.Mesh(
        new THREE.RingGeometry(0.3, 0.35, 32),
        new THREE.MeshBasicMaterial({
          color: 0xaaccff,
          transparent: true,
          opacity: 0.4,
          side: THREE.DoubleSide,
        })
      );
      ring.rotation.x = -Math.PI / 2;
      ring.position.y = 0.03;
      ring.userData = { age: i * 1.2, speed: 0.4 };
      this.scene.add(ring);
      this.ripples.push(ring);
    }

    // Small koi-like shapes
    this.koi = [];
    for (let i = 0; i < 3; i++) {
      const k = new THREE.Mesh(
        new THREE.CapsuleGeometry(0.08, 0.35, 4, 6),
        new THREE.MeshLambertMaterial({ color: i === 0 ? 0xff6633 : 0xffffff })
      );
      k.rotation.x = Math.PI / 2;
      k.position.set((Math.random() - 0.5) * 2, 0.1, (Math.random() - 0.5) * 2);
      k.userData = { angle: Math.random() * Math.PI * 2, radius: 0.8 + Math.random() };
      this.scene.add(k);
      this.koi.push(k);
    }
  }

  buildWindElements() {
    // Falling maple leaves
    this.leaves = [];
    const leafMat = new THREE.MeshBasicMaterial({ color: 0xcc4422, side: THREE.DoubleSide });
    for (let i = 0; i < 25; i++) {
      const leaf = new THREE.Mesh(new THREE.PlaneGeometry(0.15, 0.1), leafMat);
      leaf.position.set(
        (Math.random() - 0.5) * 12,
        2 + Math.random() * 4,
        (Math.random() - 0.5) * 8
      );
      leaf.userData = {
        vy: -0.3 - Math.random() * 0.4,
        vx: (Math.random() - 0.5) * 0.3,
        spin: Math.random() * 2,
      };
      this.scene.add(leaf);
      this.leaves.push(leaf);
    }
  }

  setupMusicOnInteraction() {
    const start = () => {
      if (this.audioCtx) return;
      this.startMusic();
      window.removeEventListener('pointerdown', start);
      window.removeEventListener('keydown', start);
    };
    window.addEventListener('pointerdown', start);
    window.addEventListener('keydown', start);
  }

  startMusic() {
    this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const ctx = this.audioCtx;

    const master = ctx.createGain();
    master.gain.value = 0.18;
    master.connect(ctx.destination);

    // Soft pentatonic pad (A minor pentatonic-ish)
    const notes = [220, 261.6, 293.7, 329.6, 392]; // A3 C4 D4 E4 G4
    notes.forEach((freq, i) => {
      const osc = ctx.createOscillator();
      osc.type = 'sine';
      osc.frequency.value = freq;
      const g = ctx.createGain();
      g.gain.value = 0.12 / notes.length;
      osc.connect(g);
      g.connect(master);
      osc.start();
      this.musicNodes.push(osc);
    });

    // Gentle high shimmer
    const shimmer = ctx.createOscillator();
    shimmer.type = 'triangle';
    shimmer.frequency.value = 880;
    const sg = ctx.createGain();
    sg.gain.value = 0.02;
    shimmer.connect(sg);
    sg.connect(master);
    shimmer.start();
    this.musicNodes.push(shimmer);

    // Soft filtered noise for wind / water
    const bufferSize = 2 * ctx.sampleRate;
    const noiseBuf = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
    const data = noiseBuf.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) data[i] = Math.random() * 2 - 1;
    const noise = ctx.createBufferSource();
    noise.buffer = noiseBuf;
    noise.loop = true;
    const filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 600;
    const ng = ctx.createGain();
    ng.gain.value = 0.04;
    noise.connect(filter);
    filter.connect(ng);
    ng.connect(master);
    noise.start();
    this.musicNodes.push(noise);
  }

  update(delta) {
    const t = this.clock.elapsedTime;
    this.windPhase += delta;

    // Gentle camera drift
    this.camera.position.x = Math.sin(t * 0.08) * 1.2;
    this.camera.position.y = 3.2 + Math.sin(t * 0.05) * 0.3;
    this.camera.lookAt(0, 0.4, 0);

    // Bamboo sway
    this.bamboo.children.forEach(stalk => {
      stalk.rotation.z = Math.sin(t * 0.6 + stalk.userData.phase) * 0.08;
    });

    // Maple leaves in wind
    this.leaves.forEach(leaf => {
      const u = leaf.userData;
      leaf.position.x += u.vx * delta + Math.sin(t + leaf.position.z) * 0.15 * delta;
      leaf.position.y += u.vy * delta;
      leaf.rotation.z += u.spin * delta;
      if (leaf.position.y < 0) {
        leaf.position.y = 4 + Math.random() * 2;
        leaf.position.x = (Math.random() - 0.5) * 12;
      }
    });

    // Pond ripples
    this.ripples.forEach(r => {
      r.userData.age += delta;
      const s = 1 + r.userData.age * r.userData.speed;
      r.scale.set(s, s, 1);
      r.material.opacity = Math.max(0, 0.5 - r.userData.age * 0.15);
      if (r.userData.age > 4) r.userData.age = 0;
    });

    // Koi swimming
    this.koi.forEach(k => {
      const u = k.userData;
      u.angle += delta * 0.4;
      k.position.x = Math.cos(u.angle) * u.radius;
      k.position.z = Math.sin(u.angle) * u.radius;
      k.rotation.y = -u.angle;
    });

    // Lantern flicker
    this.lanternLight.intensity = 1.2 + Math.sin(t * 3) * 0.15;
  }

  run() {
    const orig = super.run.bind(this);
    orig();
  }
}

// Start when loaded
new ZenGardenScreensaver().run();
