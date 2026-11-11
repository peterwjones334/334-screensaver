/**
 * Haunted House screensaver — new Three.js version with procedural creepy audio loop.
 *
 * Scene: foggy night, simple house silhouette, floating ghosts, flying bats,
 * occasional lightning, and a looping ambient drone + wind + creaks generated
 * with the Web Audio API (no external audio files required).
 */
import * as THREE from 'three';
import { Screensaver } from './base.js';

export class HauntedHouseScreensaver extends Screensaver {
  constructor() {
    super({ title: 'Haunted House' });

    this.scene.fog = new THREE.Fog(0x0a0a12, 5, 40);
    this.scene.background = new THREE.Color(0x0a0a12);

    // Lighting
    this.ambient = new THREE.AmbientLight(0x222244, 0.4);
    this.scene.add(this.ambient);

    this.moonLight = new THREE.DirectionalLight(0xaaaaff, 0.6);
    this.moonLight.position.set(-10, 15, 5);
    this.scene.add(this.moonLight);

    this.lightning = new THREE.DirectionalLight(0xffffff, 0);
    this.lightning.position.set(5, 10, 10);
    this.scene.add(this.lightning);

    // Simple house (boxes for silhouette)
    const houseGroup = new THREE.Group();
    const wallMat = new THREE.MeshLambertMaterial({ color: 0x1a1a22 });
    const roofMat = new THREE.MeshLambertMaterial({ color: 0x111118 });

    const body = new THREE.Mesh(new THREE.BoxGeometry(6, 4, 5), wallMat);
    body.position.y = 2;
    houseGroup.add(body);

    const roof = new THREE.Mesh(new THREE.ConeGeometry(4.5, 2.5, 4), roofMat);
    roof.position.y = 5.2;
    roof.rotation.y = Math.PI / 4;
    houseGroup.add(roof);

    // Windows that can glow
    const windowGeo = new THREE.PlaneGeometry(0.8, 1.2);
    const windowMat = new THREE.MeshBasicMaterial({ color: 0x220011, side: THREE.DoubleSide });
    this.windows = [];
    [[-1.5, 2.5, 2.51], [1.5, 2.5, 2.51], [0, 2.5, 2.51]].forEach(pos => {
      const win = new THREE.Mesh(windowGeo, windowMat.clone());
      win.position.set(...pos);
      houseGroup.add(win);
      this.windows.push(win);
    });

    houseGroup.position.y = -1;
    this.scene.add(houseGroup);
    this.house = houseGroup;

    // Ghosts (translucent spheres that drift)
    this.ghosts = [];
    for (let i = 0; i < 5; i++) {
      const geo = new THREE.SphereGeometry(0.4 + Math.random() * 0.3, 16, 16);
      const mat = new THREE.MeshBasicMaterial({
        color: 0xaabbcc,
        transparent: true,
        opacity: 0.35,
      });
      const ghost = new THREE.Mesh(geo, mat);
      ghost.position.set(
        (Math.random() - 0.5) * 20,
        1 + Math.random() * 6,
        (Math.random() - 0.5) * 15 - 5
      );
      ghost.userData = {
        vx: (Math.random() - 0.5) * 1.5,
        vy: (Math.random() - 0.5) * 0.8,
        vz: (Math.random() - 0.5) * 1.5,
      };
      this.scene.add(ghost);
      this.ghosts.push(ghost);
    }

    // Bats (small dark triangles / cones that fly)
    this.bats = [];
    for (let i = 0; i < 12; i++) {
      const bat = new THREE.Mesh(
        new THREE.ConeGeometry(0.15, 0.4, 3),
        new THREE.MeshBasicMaterial({ color: 0x111111 })
      );
      bat.position.set(
        (Math.random() - 0.5) * 30,
        3 + Math.random() * 8,
        (Math.random() - 0.5) * 20 - 8
      );
      bat.userData = {
        speed: 2 + Math.random() * 3,
        angle: Math.random() * Math.PI * 2,
        yOffset: Math.random() * Math.PI * 2,
      };
      this.scene.add(bat);
      this.bats.push(bat);
    }

    // Ground plane
    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(80, 80),
      new THREE.MeshLambertMaterial({ color: 0x0d0d12 })
    );
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -1;
    this.scene.add(ground);

    // Camera start
    this.camera.position.set(0, 3, 12);
    this.camera.lookAt(0, 2, 0);

    // Audio (procedural creepy loop)
    this.audioCtx = null;
    this.audioStarted = false;
    this.setupAudioOnInteraction();

    this.lightningTimer = 0;
    this.nextLightning = 4 + Math.random() * 8;
  }

  setupAudioOnInteraction() {
    const start = () => {
      if (this.audioStarted) return;
      this.audioStarted = true;
      this.startCreepyAudio();
      window.removeEventListener('pointerdown', start);
      window.removeEventListener('keydown', start);
    };
    window.addEventListener('pointerdown', start);
    window.addEventListener('keydown', start);
  }

  startCreepyAudio() {
    this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const ctx = this.audioCtx;

    // Master gain (quiet)
    const master = ctx.createGain();
    master.gain.value = 0.25;
    master.connect(ctx.destination);

    // Low drone (two detuned oscillators)
    const drone1 = ctx.createOscillator();
    drone1.type = 'sine';
    drone1.frequency.value = 55;
    const drone2 = ctx.createOscillator();
    drone2.type = 'triangle';
    drone2.frequency.value = 57.5;
    const droneGain = ctx.createGain();
    droneGain.gain.value = 0.4;
    drone1.connect(droneGain);
    drone2.connect(droneGain);
    droneGain.connect(master);
    drone1.start();
    drone2.start();

    // Filtered noise for wind
    const bufferSize = 2 * ctx.sampleRate;
    const noiseBuffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      output[i] = Math.random() * 2 - 1;
    }
    const noise = ctx.createBufferSource();
    noise.buffer = noiseBuffer;
    noise.loop = true;
    const filter = ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 400;
    const noiseGain = ctx.createGain();
    noiseGain.gain.value = 0.15;
    noise.connect(filter);
    filter.connect(noiseGain);
    noiseGain.connect(master);
    noise.start();

    // Occasional creak (high-passed noise burst scheduled randomly)
    this.scheduleCreaks(ctx, master);
  }

  scheduleCreaks(ctx, master) {
    const creak = () => {
      if (!this.running || !this.audioCtx) return;
      const osc = ctx.createOscillator();
      osc.type = 'sawtooth';
      osc.frequency.value = 120 + Math.random() * 80;
      const g = ctx.createGain();
      g.gain.setValueAtTime(0, ctx.currentTime);
      g.gain.linearRampToValueAtTime(0.08, ctx.currentTime + 0.05);
      g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.8);
      osc.connect(g);
      g.connect(master);
      osc.start();
      osc.stop(ctx.currentTime + 0.9);

      setTimeout(creak, 3000 + Math.random() * 7000);
    };
    setTimeout(creak, 2000);
  }

  update(delta) {
    const t = this.clock.elapsedTime;

    // Gentle camera drift
    this.camera.position.x = Math.sin(t * 0.15) * 4;
    this.camera.position.y = 3 + Math.sin(t * 0.1) * 0.5;
    this.camera.lookAt(0, 2, 0);

    // Ghosts drift
    this.ghosts.forEach(g => {
      g.position.x += g.userData.vx * delta;
      g.position.y += g.userData.vy * delta;
      g.position.z += g.userData.vz * delta;
      // bounce in a loose box
      if (Math.abs(g.position.x) > 15) g.userData.vx *= -1;
      if (g.position.y < 0.5 || g.position.y > 8) g.userData.vy *= -1;
      if (g.position.z < -15 || g.position.z > 5) g.userData.vz *= -1;
      g.material.opacity = 0.25 + Math.sin(t * 2 + g.position.x) * 0.15;
    });

    // Bats fly in figure-ish paths
    this.bats.forEach(bat => {
      const d = bat.userData;
      d.angle += d.speed * delta * 0.4;
      bat.position.x = Math.cos(d.angle) * 12 + Math.sin(t * 0.5) * 2;
      bat.position.z = Math.sin(d.angle) * 8 - 6;
      bat.position.y = 4 + Math.sin(t * 3 + d.yOffset) * 1.5;
      bat.rotation.z = Math.sin(t * 8 + d.yOffset) * 0.4;
    });

    // Lightning
    this.lightningTimer += delta;
    if (this.lightningTimer > this.nextLightning) {
      this.lightning.intensity = 8;
      this.ambient.intensity = 1.2;
      this.windows.forEach(w => w.material.color.setHex(0xffeeaa));
      setTimeout(() => {
        if (!this.running) return;
        this.lightning.intensity = 0;
        this.ambient.intensity = 0.4;
        this.windows.forEach(w => w.material.color.setHex(0x220011));
      }, 80 + Math.random() * 120);
      this.lightningTimer = 0;
      this.nextLightning = 5 + Math.random() * 12;
    }

    // Subtle window flicker between strikes
    if (this.lightning.intensity === 0) {
      this.windows.forEach((w, i) => {
        if (Math.random() < 0.02) {
          w.material.color.setHex(Math.random() > 0.5 ? 0x331111 : 0x220011);
        }
      });
    }
  }

  // Override run to clean up audio
  run() {
    const original = super.run.bind(this);
    const check = () => {
      if (!this.running && this.audioCtx) {
        this.audioCtx.close();
        this.audioCtx = null;
      }
    };
    const interval = setInterval(check, 500);
    original();
    // clear interval when stopped (best-effort)
    setTimeout(() => clearInterval(interval), 100);
  }
}

// Start when loaded
new HauntedHouseScreensaver().run();
