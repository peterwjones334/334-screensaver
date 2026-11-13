/**
 * Galaxians Arcade Clone Screensaver — plays itself.
 *
 * 3 levels + boss level.
 * 4 alien types with different movement and points.
 * Score counter, sound effects, and an annoying screensaver
 * that keeps announcing its presence.
 */
import * as THREE from 'three';
import { Screensaver } from './base.js';

export class GalaxiansScreensaver extends Screensaver {
  constructor() {
    super({ title: 'Galaxians Screensaver' });

    this.scene.background = new THREE.Color(0x000011);

    this.score = 0;
    this.level = 1;
    this.maxLevel = 3;
    this.bossActive = false;
    this.annoyTimer = 0;

    this.player = this.createPlayer();
    this.scene.add(this.player);

    this.aliens = [];
    this.bullets = [];
    this.enemyBullets = [];

    this.spawnLevel(1);

    this.buildHud();

    this.camera.position.set(0, 0, 12);
    this.camera.lookAt(0, 0, 0);

    this.audioCtx = null;
    this.setupAudio();

    this.announce("GALAXIANS SCREENSAVER ACTIVATED — DO NOT DISTURB");
  }

  setupAudio() {
    const start = () => {
      if (this.audioCtx) return;
      this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      window.removeEventListener('pointerdown', start);
      window.removeEventListener('keydown', start);
    };
    window.addEventListener('pointerdown', start);
    window.addEventListener('keydown', start);
  }

  beep(freq, dur, type = 'square', vol = 0.08) {
    if (!this.audioCtx) return;
    const o = this.audioCtx.createOscillator();
    const g = this.audioCtx.createGain();
    o.type = type;
    o.frequency.value = freq;
    g.gain.value = vol;
    o.connect(g);
    g.connect(this.audioCtx.destination);
    o.start();
    o.stop(this.audioCtx.currentTime + dur);
  }

  announce(text) {
    this.announcement = text;
    this.annoyTimer = 0;
    this.drawHud();
    this.beep(440, 0.15, 'square', 0.12);
    setTimeout(() => this.beep(660, 0.12, 'square', 0.1), 160);
  }

  createPlayer() {
    const geo = new THREE.ConeGeometry(0.3, 0.8, 4);
    const mat = new THREE.MeshBasicMaterial({ color: 0x00ffff });
    const ship = new THREE.Mesh(geo, mat);
    ship.rotation.x = Math.PI;
    ship.position.y = -4.2;
    return ship;
  }

  spawnLevel(level) {
    this.clearAliens();
    this.bossActive = false;

    if (level > this.maxLevel) {
      this.spawnBoss();
      return;
    }

    const rows = 3 + level;
    const cols = 8;
    const types = ['scout', 'fighter', 'bomber', 'elite'];

    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const type = types[Math.min(r, types.length - 1)];
        const alien = this.createAlien(type);
        alien.position.set((c - cols / 2) * 1.1, 3.5 - r * 0.7, 0);
        alien.userData.baseX = alien.position.x;
        alien.userData.phase = Math.random() * Math.PI * 2;
        this.scene.add(alien);
        this.aliens.push(alien);
      }
    }
    this.announce(`LEVEL ${level} — ${this.aliens.length} HOSTILES DETECTED`);
  }

  spawnBoss() {
    this.bossActive = true;
    const boss = this.createAlien('boss');
    boss.position.set(0, 2.5, 0);
    boss.scale.set(2.2, 2.2, 2.2);
    boss.userData.hp = 12;
    boss.userData.phase = 0;
    this.scene.add(boss);
    this.aliens.push(boss);
    this.announce("BOSS LEVEL — THE QUEEN HAS ARRIVED");
  }

  createAlien(type) {
    let geo, color, points, behavior;
    switch (type) {
      case 'scout':
        geo = new THREE.OctahedronGeometry(0.28);
        color = 0x44ff44;
        points = 50;
        behavior = 'zigzag';
        break;
      case 'fighter':
        geo = new THREE.TetrahedronGeometry(0.32);
        color = 0xffaa00;
        points = 80;
        behavior = 'dive';
        break;
      case 'bomber':
        geo = new THREE.BoxGeometry(0.4, 0.3, 0.3);
        color = 0xff4444;
        points = 120;
        behavior = 'slow';
        break;
      case 'elite':
        geo = new THREE.IcosahedronGeometry(0.3);
        color = 0xaa44ff;
        points = 200;
        behavior = 'erratic';
        break;
      case 'boss':
        geo = new THREE.DodecahedronGeometry(0.6);
        color = 0xff00aa;
        points = 1000;
        behavior = 'boss';
        break;
      default:
        geo = new THREE.SphereGeometry(0.3);
        color = 0xffffff;
        points = 10;
        behavior = 'zigzag';
    }
    const mat = new THREE.MeshBasicMaterial({ color, wireframe: true });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.userData = { type, points, behavior, hp: type === 'boss' ? 12 : 1 };
    return mesh;
  }

  clearAliens() {
    this.aliens.forEach(a => this.scene.remove(a));
    this.aliens = [];
  }

  buildHud() {
    this.hudCanvas = document.createElement('canvas');
    this.hudCanvas.width = 1024;
    this.hudCanvas.height = 128;
    this.hudCtx = this.hudCanvas.getContext('2d');
    this.hudTexture = new THREE.CanvasTexture(this.hudCanvas);
    this.hudPlane = new THREE.Mesh(
      new THREE.PlaneGeometry(10, 1.2),
      new THREE.MeshBasicMaterial({ map: this.hudTexture, transparent: true })
    );
    this.hudPlane.position.set(0, 5.2, 0);
    this.scene.add(this.hudPlane);
    this.drawHud();
  }

  drawHud() {
    const ctx = this.hudCtx;
    ctx.fillStyle = '#000011';
    ctx.fillRect(0, 0, 1024, 128);
    ctx.fillStyle = '#00ffff';
    ctx.font = 'bold 36px monospace';
    ctx.textAlign = 'left';
    ctx.fillText(`SCORE ${this.score.toString().padStart(6, '0')}`, 20, 50);
    ctx.fillText(`LEVEL ${this.level}${this.bossActive ? ' BOSS' : ''}`, 20, 100);
    ctx.textAlign = 'right';
    ctx.fillStyle = '#ffaa00';
    ctx.font = '28px monospace';
    ctx.fillText(this.announcement || 'SCREENSAVER MODE', 1000, 70);
    this.hudTexture.needsUpdate = true;
  }

  update(delta) {
    const t = this.clock.elapsedTime;

    // Auto-play player: track nearest alien and shoot
    if (this.aliens.length) {
      const target = this.aliens[0];
      const dx = target.position.x - this.player.position.x;
      this.player.position.x += Math.sign(dx) * Math.min(Math.abs(dx), 4 * delta);
      this.player.position.x = Math.max(-5.5, Math.min(5.5, this.player.position.x));

      if (Math.random() < 0.08) this.shoot();
    }

    // Update aliens
    this.aliens.forEach(a => {
      const u = a.userData;
      u.phase += delta;
      if (u.behavior === 'zigzag') {
        a.position.x = u.baseX + Math.sin(u.phase * 2) * 0.8;
        a.position.y -= 0.15 * delta;
      } else if (u.behavior === 'dive') {
        a.position.y -= 0.6 * delta;
        a.position.x += Math.sin(u.phase * 4) * 0.4 * delta;
      } else if (u.behavior === 'slow') {
        a.position.y -= 0.08 * delta;
        a.rotation.y += delta;
      } else if (u.behavior === 'erratic') {
        a.position.x += Math.sin(u.phase * 6) * 1.2 * delta;
        a.position.y -= 0.3 * delta;
      } else if (u.behavior === 'boss') {
        a.position.x = Math.sin(u.phase * 0.8) * 3;
        a.rotation.y += delta * 0.5;
        a.rotation.x += delta * 0.3;
        if (Math.random() < 0.03) this.enemyShoot(a);
      }

      if (a.position.y < -5) {
        a.position.y = 4;
        u.baseX = (Math.random() - 0.5) * 8;
      }

      // Occasional enemy fire
      if (u.type !== 'boss' && Math.random() < 0.004) this.enemyShoot(a);
    });

    // Bullets
    this.bullets.forEach(b => {
      b.position.y += 12 * delta;
    });
    this.enemyBullets.forEach(b => {
      b.position.y -= 6 * delta;
    });

    this.checkCollisions();

    // Clean off-screen
    this.bullets = this.bullets.filter(b => {
      if (b.position.y > 6) { this.scene.remove(b); return false; }
      return true;
    });
    this.enemyBullets = this.enemyBullets.filter(b => {
      if (b.position.y < -6) { this.scene.remove(b); return false; }
      return true;
    });

    // Level clear
    if (this.aliens.length === 0) {
      this.level++;
      if (this.level > this.maxLevel + 1) {
        this.level = 1;
        this.announce("CYCLE COMPLETE — SCREENSAVER STILL RUNNING");
      }
      this.spawnLevel(this.level);
    }

    // Annoying announcements
    this.annoyTimer += delta;
    if (this.annoyTimer > 18) {
      const messages = [
        "THIS IS A SCREENSAVER — PLEASE IGNORE",
        "GALAXIANS IS DEFENDING YOUR IDLE SCREEN",
        "DO NOT ATTEMPT TO PLAY — IT PLAYS ITSELF",
        "SCREENSAVER PROTOCOL ACTIVE",
        "ALIEN INVASION SIMULATION IN PROGRESS",
      ];
      this.announce(messages[Math.floor(Math.random() * messages.length)]);
      this.annoyTimer = 0;
    }

    this.drawHud();
  }

  shoot() {
    const b = new THREE.Mesh(
      new THREE.SphereGeometry(0.08, 6, 6),
      new THREE.MeshBasicMaterial({ color: 0x00ffff })
    );
    b.position.copy(this.player.position);
    b.position.y += 0.5;
    this.scene.add(b);
    this.bullets.push(b);
    this.beep(880, 0.05, 'square', 0.06);
  }

  enemyShoot(alien) {
    const b = new THREE.Mesh(
      new THREE.SphereGeometry(0.07, 6, 6),
      new THREE.MeshBasicMaterial({ color: 0xff4444 })
    );
    b.position.copy(alien.position);
    b.position.y -= 0.4;
    this.scene.add(b);
    this.enemyBullets.push(b);
    this.beep(220, 0.04, 'sawtooth', 0.04);
  }

  checkCollisions() {
    // Player bullets vs aliens
    for (let i = this.bullets.length - 1; i >= 0; i--) {
      const b = this.bullets[i];
      for (let j = this.aliens.length - 1; j >= 0; j--) {
        const a = this.aliens[j];
        if (b.position.distanceTo(a.position) < 0.5 * a.scale.x) {
          a.userData.hp--;
          this.scene.remove(b);
          this.bullets.splice(i, 1);
          this.beep(660, 0.08, 'square', 0.07);
          if (a.userData.hp <= 0) {
            this.score += a.userData.points;
            this.scene.remove(a);
            this.aliens.splice(j, 1);
            this.beep(330, 0.12, 'square', 0.1);
          }
          break;
        }
      }
    }

    // Enemy bullets vs player (just visual flash, no game over — it's a screensaver)
    for (let i = this.enemyBullets.length - 1; i >= 0; i--) {
      const b = this.enemyBullets[i];
      if (b.position.distanceTo(this.player.position) < 0.4) {
        this.scene.remove(b);
        this.enemyBullets.splice(i, 1);
        this.player.material.color.setHex(0xff0000);
        setTimeout(() => {
          if (this.running) this.player.material.color.setHex(0x00ffff);
        }, 80);
        this.beep(110, 0.1, 'sawtooth', 0.08);
      }
    }
  }
}

// Start when loaded
new GalaxiansScreensaver().run();
