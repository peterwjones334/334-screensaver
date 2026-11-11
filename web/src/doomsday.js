/**
 * Doomsday Clock Simulator screensaver.
 *
 * A classic clock face that creeps toward midnight as a scrolling
 * ticker of global events raises the alert level.
 */
import * as THREE from 'three';
import { Screensaver } from './base.js';

const EVENTS = [
  "NUCLEAR TEST DETECTED — ALERT LEVEL +2",
  "CLIMATE TIPPING POINT CROSSED — ALERT LEVEL +1",
  "AI ALIGNMENT FAILURE REPORTED — ALERT LEVEL +3",
  "PANDEMIC VARIANT ESCAPES CONTAINMENT — ALERT LEVEL +2",
  "CYBER ATTACK ON POWER GRID — ALERT LEVEL +1",
  "ASTEROID IMPACT PROBABILITY REVISED UPWARD — ALERT LEVEL +2",
  "DIPLOMATIC CHANNELS CLOSED — ALERT LEVEL +1",
  "SUPPLY CHAIN COLLAPSE IN THREE REGIONS — ALERT LEVEL +1",
  "UNKNOWN SUBTERRANEAN SIGNAL — ALERT LEVEL +2",
  "MUTUAL ASSURED DESTRUCTION DOCTRINE REAFFIRMED — ALERT LEVEL +1",
  "OCEAN ACIDIFICATION CRITICAL — ALERT LEVEL +1",
  "AUTONOMOUS WEAPONS DEPLOYED — ALERT LEVEL +3",
  "POLAR ICE SHEET COLLAPSE ACCELERATING — ALERT LEVEL +1",
  "GLOBAL FINANCIAL FLASH CRASH — ALERT LEVEL +1",
  "BIOWEAPON RESEARCH LEAK — ALERT LEVEL +2",
];

export class DoomsdayScreensaver extends Screensaver {
  constructor() {
    super({ title: 'Doomsday Clock' });

    this.scene.background = new THREE.Color(0x0a0a0a);

    // Minutes to midnight (starts at 90 seconds = 1.5 min, classic-ish)
    this.secondsToMidnight = 90;
    this.targetSeconds = 90;
    this.alertLevel = 1;

    this.buildClock();
    this.buildTicker();
    this.buildAlertText();

    this.camera.position.set(0, 0, 8);
    this.camera.lookAt(0, 0, 0);

    this.eventTimer = 0;
    this.nextEvent = 4 + Math.random() * 6;
    this.tickerOffset = 0;
    this.currentEvent = EVENTS[0];
  }

  buildClock() {
    this.clockGroup = new THREE.Group();

    // Face
    const face = new THREE.Mesh(
      new THREE.CircleGeometry(2.8, 64),
      new THREE.MeshBasicMaterial({ color: 0x111111 })
    );
    this.clockGroup.add(face);

    // Rim
    const rim = new THREE.Mesh(
      new THREE.RingGeometry(2.75, 2.95, 64),
      new THREE.MeshBasicMaterial({ color: 0xcc2222 })
    );
    this.clockGroup.add(rim);

    // Tick marks
    for (let i = 0; i < 60; i++) {
      const isHour = i % 5 === 0;
      const len = isHour ? 0.18 : 0.08;
      const tick = new THREE.Mesh(
        new THREE.BoxGeometry(0.02, len, 0.01),
        new THREE.MeshBasicMaterial({ color: isHour ? 0xffffff : 0x888888 })
      );
      const angle = (i / 60) * Math.PI * 2 - Math.PI / 2;
      tick.position.set(Math.cos(angle) * 2.55, Math.sin(angle) * 2.55, 0.01);
      tick.rotation.z = angle + Math.PI / 2;
      this.clockGroup.add(tick);
    }

    // Hands (minute hand points to remaining time)
    this.minuteHand = new THREE.Mesh(
      new THREE.BoxGeometry(0.06, 1.6, 0.02),
      new THREE.MeshBasicMaterial({ color: 0xff4444 })
    );
    this.minuteHand.position.y = 0.8;
    this.clockGroup.add(this.minuteHand);

    this.hourHand = new THREE.Mesh(
      new THREE.BoxGeometry(0.08, 1.0, 0.02),
      new THREE.MeshBasicMaterial({ color: 0xffffff })
    );
    this.hourHand.position.y = 0.5;
    this.clockGroup.add(this.hourHand);

    // Center pin
    const pin = new THREE.Mesh(
      new THREE.CircleGeometry(0.08, 16),
      new THREE.MeshBasicMaterial({ color: 0xff0000 })
    );
    pin.position.z = 0.02;
    this.clockGroup.add(pin);

    this.scene.add(this.clockGroup);
  }

  buildTicker() {
    // Scrolling text plane using canvas texture
    this.tickerCanvas = document.createElement('canvas');
    this.tickerCanvas.width = 2048;
    this.tickerCanvas.height = 128;
    this.tickerCtx = this.tickerCanvas.getContext('2d');

    this.tickerTexture = new THREE.CanvasTexture(this.tickerCanvas);
    this.tickerPlane = new THREE.Mesh(
      new THREE.PlaneGeometry(14, 0.9),
      new THREE.MeshBasicMaterial({
        map: this.tickerTexture,
        transparent: true,
      })
    );
    this.tickerPlane.position.set(0, -3.6, 0);
    this.scene.add(this.tickerPlane);

    this.drawTicker();
  }

  drawTicker() {
    const ctx = this.tickerCtx;
    ctx.fillStyle = '#0a0a0a';
    ctx.fillRect(0, 0, 2048, 128);
    ctx.fillStyle = '#ff4444';
    ctx.font = 'bold 48px monospace';
    ctx.textBaseline = 'middle';
    const text = `  ${this.currentEvent}  ·  ALERT LEVEL ${this.alertLevel}  ·  ${this.currentEvent}  ·  `;
    ctx.fillText(text, -this.tickerOffset, 64);
    ctx.fillText(text, -this.tickerOffset + ctx.measureText(text).width, 64);
    this.tickerTexture.needsUpdate = true;
  }

  buildAlertText() {
    this.alertCanvas = document.createElement('canvas');
    this.alertCanvas.width = 1024;
    this.alertCanvas.height = 128;
    this.alertCtx = this.alertCanvas.getContext('2d');
    this.alertTexture = new THREE.CanvasTexture(this.alertCanvas);
    this.alertPlane = new THREE.Mesh(
      new THREE.PlaneGeometry(6, 0.7),
      new THREE.MeshBasicMaterial({ map: this.alertTexture, transparent: true })
    );
    this.alertPlane.position.set(0, 3.4, 0);
    this.scene.add(this.alertPlane);
    this.drawAlert();
  }

  drawAlert() {
    const ctx = this.alertCtx;
    ctx.clearRect(0, 0, 1024, 128);
    ctx.fillStyle = '#ff2222';
    ctx.font = 'bold 42px monospace';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    const mins = Math.floor(this.secondsToMidnight / 60);
    const secs = Math.floor(this.secondsToMidnight % 60);
    ctx.fillText(`${mins}:${secs.toString().padStart(2, '0')} TO MIDNIGHT`, 512, 40);
    ctx.font = '28px monospace';
    ctx.fillStyle = '#aaaaaa';
    ctx.fillText(`ALERT LEVEL ${this.alertLevel}`, 512, 90);
    this.alertTexture.needsUpdate = true;
  }

  update(delta) {
    // Move clock hands toward current seconds-to-midnight
    // Midnight is straight up; each second is 6 degrees on the minute hand
    const minuteAngle = -((60 - (this.secondsToMidnight % 60)) / 60) * Math.PI * 2;
    const hourAngle = -((12 - (this.secondsToMidnight / 60)) / 12) * Math.PI * 2;
    this.minuteHand.rotation.z = minuteAngle;
    this.hourHand.rotation.z = hourAngle;

    // Slowly approach target
    this.secondsToMidnight += (this.targetSeconds - this.secondsToMidnight) * delta * 0.8;

    // Ticker scroll
    this.tickerOffset += delta * 120;
    if (this.tickerOffset > 2000) this.tickerOffset = 0;
    this.drawTicker();

    // New events raise alert
    this.eventTimer += delta;
    if (this.eventTimer > this.nextEvent) {
      const evt = EVENTS[Math.floor(Math.random() * EVENTS.length)];
      this.currentEvent = evt;
      const increase = 1 + Math.floor(Math.random() * 3);
      this.alertLevel = Math.min(10, this.alertLevel + increase);
      // Each alert level removes ~6 seconds
      this.targetSeconds = Math.max(5, this.targetSeconds - increase * 6);
      this.eventTimer = 0;
      this.nextEvent = 5 + Math.random() * 8;

      // Flash rim
      this.clockGroup.children[1].material.color.setHex(0xffffff);
      setTimeout(() => {
        if (this.running) this.clockGroup.children[1].material.color.setHex(0xcc2222);
      }, 120);
    }

    this.drawAlert();

    // Subtle pulse when close to midnight
    if (this.secondsToMidnight < 30) {
      const pulse = 1 + Math.sin(this.clock.elapsedTime * 4) * 0.05;
      this.clockGroup.scale.setScalar(pulse);
    }
  }
}

// Start when loaded
new DoomsdayScreensaver().run();
