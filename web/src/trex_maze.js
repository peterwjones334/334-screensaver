/**
 * 3D Vector Maze — Classic Monster Maze with ASCII T-Rex.
 *
 * Wireframe maze. An ASCII art T-Rex lurks inside.
 * When the camera gets close, the T-Rex roars, the screen flashes red,
 * then the maze regenerates and we start again.
 */
import * as THREE from 'three';
import { Screensaver } from './base.js';

const TREX_ASCII = `
               __
              / _)
     _.----._/ /
    /         /
 __/ (  | (  |
/__.-'|_|--|_|
`;

export class TrexMazeScreensaver extends Screensaver {
  constructor() {
    super({ title: 'T-Rex Maze' });

    this.scene.background = new THREE.Color(0x001100);

    this.mazeSize = 15;
    this.cellSize = 2;
    this.walls = [];
    this.trex = null;
    this.trexPos = new THREE.Vector3();
    this.state = 'exploring'; // exploring | roaring | resetting
    this.roarTimer = 0;
    this.resetTimer = 0;

    this.lineMat = new THREE.LineBasicMaterial({ color: 0x33ff66 });
    this.redMat = new THREE.LineBasicMaterial({ color: 0xff2222 });

    this.generateMaze();
    this.placeTrex();
    this.createTrexSprite();

    this.camera.position.set(1, 1.2, 1);
    this.camera.lookAt(this.cellSize, 1, this.cellSize);

    this.dir = new THREE.Vector3(1, 0, 0);
    this.moveSpeed = 1.8;
    this.turnTimer = 0;
  }

  generateMaze() {
    // Clear old walls
    this.walls.forEach(w => this.scene.remove(w));
    this.walls = [];

    // Simple recursive-backtracker style grid (simplified open corridors)
    const grid = Array.from({ length: this.mazeSize }, () =>
      Array.from({ length: this.mazeSize }, () => ({ n: true, e: true, s: true, w: true }))
    );

    const stack = [[1, 1]];
    const visited = new Set(['1,1']);

    const dirs = [
      [0, -1, 'n', 's'],
      [1, 0, 'e', 'w'],
      [0, 1, 's', 'n'],
      [-1, 0, 'w', 'e'],
    ];

    while (stack.length) {
      const [x, y] = stack[stack.length - 1];
      const neighbors = dirs
        .map(([dx, dy, wall, opp]) => [x + dx, y + dy, wall, opp])
        .filter(([nx, ny]) =>
          nx > 0 && nx < this.mazeSize - 1 &&
          ny > 0 && ny < this.mazeSize - 1 &&
          !visited.has(`${nx},${ny}`)
        );

      if (neighbors.length) {
        const [nx, ny, wall, opp] = neighbors[Math.floor(Math.random() * neighbors.length)];
        grid[y][x][wall] = false;
        grid[ny][nx][opp] = false;
        visited.add(`${nx},${ny}`);
        stack.push([nx, ny]);
      } else {
        stack.pop();
      }
    }

    // Build line walls
    const h = 2.2;
    for (let y = 0; y < this.mazeSize; y++) {
      for (let x = 0; x < this.mazeSize; x++) {
        const cell = grid[y][x];
        const px = x * this.cellSize;
        const pz = y * this.cellSize;

        if (cell.n) this.addWall(px, 0, pz, px + this.cellSize, 0, pz, h);
        if (cell.e) this.addWall(px + this.cellSize, 0, pz, px + this.cellSize, 0, pz + this.cellSize, h);
        if (cell.s) this.addWall(px, 0, pz + this.cellSize, px + this.cellSize, 0, pz + this.cellSize, h);
        if (cell.w) this.addWall(px, 0, pz, px, 0, pz + this.cellSize, h);
      }
    }

    this.grid = grid;
  }

  addWall(x1, y1, z1, x2, y2, z2, height) {
    const points = [
      new THREE.Vector3(x1, y1, z1),
      new THREE.Vector3(x2, y2, z2),
      new THREE.Vector3(x2, y2 + height, z2),
      new THREE.Vector3(x1, y1 + height, z1),
      new THREE.Vector3(x1, y1, z1),
    ];
    const geo = new THREE.BufferGeometry().setFromPoints(points);
    const line = new THREE.Line(geo, this.lineMat);
    this.scene.add(line);
    this.walls.push(line);
  }

  placeTrex() {
    // Place T-Rex in a random open-ish cell far from start
    let tx, ty;
    do {
      tx = 2 + Math.floor(Math.random() * (this.mazeSize - 4));
      ty = 2 + Math.floor(Math.random() * (this.mazeSize - 4));
    } while (tx < 4 && ty < 4);

    this.trexPos.set(tx * this.cellSize + this.cellSize / 2, 1.1, ty * this.cellSize + this.cellSize / 2);
  }

  createTrexSprite() {
    if (this.trex) this.scene.remove(this.trex);

    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 256;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#001100';
    ctx.fillRect(0, 0, 512, 256);
    ctx.fillStyle = '#33ff66';
    ctx.font = 'bold 28px monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    const lines = TREX_ASCII.trim().split('\n');
    lines.forEach((line, i) => {
      ctx.fillText(line, 256, 40 + i * 32);
    });

    const tex = new THREE.CanvasTexture(canvas);
    const mat = new THREE.SpriteMaterial({ map: tex, transparent: true });
    this.trex = new THREE.Sprite(mat);
    this.trex.scale.set(2.2, 1.1, 1);
    this.trex.position.copy(this.trexPos);
    this.scene.add(this.trex);
  }

  update(delta) {
    if (this.state === 'exploring') {
      this.explore(delta);
    } else if (this.state === 'roaring') {
      this.roar(delta);
    } else if (this.state === 'resetting') {
      this.resetting(delta);
    }
  }

  explore(delta) {
    // Simple auto-wander: move forward, turn at walls or randomly
    const next = this.camera.position.clone().add(this.dir.clone().multiplyScalar(this.moveSpeed * delta));

    // Rough wall check (stay in open space)
    const gx = Math.floor(next.x / this.cellSize);
    const gz = Math.floor(next.z / this.cellSize);
    if (gx < 1 || gx >= this.mazeSize - 1 || gz < 1 || gz >= this.mazeSize - 1) {
      this.turn();
    } else {
      this.camera.position.copy(next);
    }

    this.camera.lookAt(this.camera.position.clone().add(this.dir));

    this.turnTimer += delta;
    if (this.turnTimer > 2.5 + Math.random() * 3) {
      this.turn();
      this.turnTimer = 0;
    }

    // Check proximity to T-Rex
    const dist = this.camera.position.distanceTo(this.trexPos);
    if (dist < 2.2) {
      this.state = 'roaring';
      this.roarTimer = 0;
      this.startRoar();
    }
  }

  turn() {
    const turns = [
      new THREE.Vector3(1, 0, 0),
      new THREE.Vector3(-1, 0, 0),
      new THREE.Vector3(0, 0, 1),
      new THREE.Vector3(0, 0, -1),
    ];
    this.dir = turns[Math.floor(Math.random() * turns.length)];
  }

  startRoar() {
    // Visual roar: scale T-Rex and flash
    this.trex.material.color.setHex(0xff2222);
    this.lineMat.color.setHex(0xff2222);

    // Simple Web Audio roar
    try {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(80, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(40, ctx.currentTime + 0.8);
      gain.gain.setValueAtTime(0.3, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 1.2);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 1.3);
    } catch (e) { /* ignore */ }
  }

  roar(delta) {
    this.roarTimer += delta;
    // Shake and pulse
    this.trex.scale.setScalar(2.2 + Math.sin(this.roarTimer * 20) * 0.4);
    this.scene.background.setHex(this.roarTimer % 0.2 < 0.1 ? 0x330000 : 0x110000);

    if (this.roarTimer > 1.6) {
      this.state = 'resetting';
      this.resetTimer = 0;
      this.scene.background.setHex(0xff0000);
    }
  }

  resetting(delta) {
    this.resetTimer += delta;
    if (this.resetTimer > 0.8) {
      // Restart
      this.generateMaze();
      this.placeTrex();
      this.createTrexSprite();
      this.camera.position.set(1, 1.2, 1);
      this.dir.set(1, 0, 0);
      this.lineMat.color.setHex(0x33ff66);
      this.scene.background.setHex(0x001100);
      this.state = 'exploring';
    }
  }
}

// Start when loaded
new TrexMazeScreensaver().run();
