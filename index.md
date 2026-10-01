---
layout: default
permalink: /
published: true
---

<div class="abstract">
<p class="abstract-title">Abstract</p>
<p>I am a robotics researcher and Ph.D. candidate in Marine Technology at NTNU, where I develop risk-aware and safeguarding control systems that keep autonomous ships safe as their propulsion, power, and control systems interact. Before NTNU, I built a generic guidance, navigation, and control framework for marine vehicles and the software and electronics for a seabed-mapping AUV at the University of Rhode Island. Before that, I spent several years writing mission-critical software for indoor logistics robots and doing swarm robotics research. My interests include marine vehicle control and guidance, marine autonomy, safety-critical controllers, and risk awareness. Outside the lab, I collaborate with artists on interactive audio-visual installations.</p>
<p class="keywords"><em>Keywords</em>&mdash;marine autonomy, safety-critical control, risk awareness, guidance and control.</p>
</div>

<figure class="latex-slider">
  <input type="range" id="speed" min="-150" max="150" step="0.4" value="0" aria-label="Tangerine velocity" oninput="inputEventHandler(this)"/>
  <div class="axis" aria-hidden="true"><span>&minus;15</span><span>0</span><span>15</span></div>
  <figcaption><span class="fig-label">Figure 1:</span> Tangerine velocity, <output for="speed" id="speed-value"><i>v</i> = 0.0</output>. Drag to excite the system; a control barrier function keeps \(h_{ij} = \|p_i - p_j\|^2 - D^2 \geq 0\).</figcaption>
</figure>

<canvas id="tangerineCanvas" style="position: fixed; top: 0; left: 0; z-index: -1;"></canvas>

<script type="text/javascript">
let tangerines = [];
let speedFactor = 1;
let ctx;
let initialized = false;

// Collision avoidance with a control barrier function (CBF) safety filter.
// Each tangerine is a single integrator, p+ = p + u, whose nominal input is
// its velocity scaled by the slider. For every pair, h = |pi - pj|^2 - D^2
// must stay >= 0. Since h+ = h + 2 dp.(ui - uj) + |ui - uj|^2, enforcing the
// linear constraint 2 dp.(ui - uj) >= -GAMMA h gives h+ >= (1 - GAMMA) h, so
// safety holds exactly in discrete time. Each tangerine enforces half of
// every pair constraint, plus barriers keeping it inside the window, by
// solving min |u - u_nom|^2 subject to those constraints.
const RADIUS = 24;            // half the emoji size, px
const D = 2 * RADIUS + 4;     // minimum distance between centres, px
const GAMMA = 0.5;            // CBF decay rate per frame, in (0, 1]

function initTangerines() {
  const canvas = document.getElementById("tangerineCanvas");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  ctx = canvas.getContext("2d");

  // Calculate number of oranges based on screen size
  const screenArea = canvas.width * canvas.height;
  const baseArea = 1920 * 1080; // Reference screen size
  const baseCount = 20; // Base number of oranges for reference screen

  // Calculate orange count with min and max limits
  let orangeCount = Math.floor((screenArea / baseArea) * baseCount);
  orangeCount = Math.max(10, Math.min(orangeCount, 40)); // Between 10 and 40 oranges

  // Start from a safe set: inside the window and not overlapping
  tangerines = [];
  for (let tries = 0; tangerines.length < orangeCount && tries < 5000; tries++) {
    const x = RADIUS + Math.random() * (canvas.width - 2 * RADIUS);
    const y = RADIUS + Math.random() * (canvas.height - 2 * RADIUS);
    if (tangerines.every(t => (t.x - x) ** 2 + (t.y - y) ** 2 > D * D)) {
      tangerines.push({
        x: x,
        y: y,
        vx: (Math.random() - 0.5) * 2,
        vy: (Math.random() - 0.5) * 2
      });
    }
  }
}

// Solve min |u - u_nom|^2 s.t. a_k.u >= b_k with Hildreth's method
// (coordinate ascent on the dual). u = 0 is always feasible, so fall back to
// it unless the result checks out.
function solveQP(ux, uy, A, B) {
  const lambda = new Array(A.length).fill(0);
  for (let iter = 0; iter < 200; iter++) {
    let change = 0;
    for (let k = 0; k < A.length; k++) {
      const [ax, ay] = A[k];
      const violation = B[k] - (ax * ux + ay * uy);
      const next = Math.max(0, lambda[k] + violation / (ax * ax + ay * ay));
      const step = next - lambda[k];
      lambda[k] = next;
      ux += step * ax;
      uy += step * ay;
      change = Math.max(change, Math.abs(step) * Math.hypot(ax, ay));
    }
    if (change < 1e-9) break;
  }
  const feasible = A.every(([ax, ay], k) => ax * ux + ay * uy >= B[k] - 1e-9);
  return feasible ? [ux, uy] : [0, 0];
}

function safeInput(i, ux, uy) {
  const t = tangerines[i];
  const W = ctx.canvas.width, H = ctx.canvas.height;
  const A = [[1, 0], [-1, 0], [0, 1], [0, -1]];
  const B = [
    -GAMMA * (t.x - RADIUS), -GAMMA * (W - RADIUS - t.x),
    -GAMMA * (t.y - RADIUS), -GAMMA * (H - RADIUS - t.y)
  ];
  // The safe input is never longer than the nominal one (0 is feasible), so
  // a neighbour with 2 |dp| |u_nom| <= GAMMA h / 2 cannot constrain it.
  const speed = Math.hypot(ux, uy);
  tangerines.forEach((o, j) => {
    if (j === i) return;
    const dx = t.x - o.x, dy = t.y - o.y;
    const h = dx * dx + dy * dy - D * D;
    if (2 * Math.hypot(dx, dy) * speed <= GAMMA * h / 2) return;
    A.push([2 * dx, 2 * dy]);
    B.push(-GAMMA * h / 2);
  });
  return solveQP(ux, uy, A, B);
}

function drawLines() {
  ctx.strokeStyle = "orange";
  for (let i = 0; i < tangerines.length; i++) {
    for (let j = i+1; j < tangerines.length; j++) {
      const dx = tangerines[i].x - tangerines[j].x;
      const dy = tangerines[i].y - tangerines[j].y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      // Only draw lines if oranges are within a certain distance
      const maxDistance = 250; // Maximum distance for drawing lines
      if (dist <= maxDistance) {
        // Make lines thinner
        const thickness = Math.max(0.5, 3 - dist/100);
        ctx.lineWidth = thickness;
        ctx.beginPath();
        ctx.moveTo(tangerines[i].x, tangerines[i].y);
        ctx.lineTo(tangerines[j].x, tangerines[j].y);
        ctx.stroke();
      }
    }
  }
}

function updateTangerines() {
  if (!initialized) return;
  const W = ctx.canvas.width, H = ctx.canvas.height;

  // Filter every input against the same snapshot of positions, then move
  const inputs = tangerines.map((t, i) => safeInput(i, t.vx * speedFactor, t.vy * speedFactor));
  tangerines.forEach((t, i) => {
    const [ux, uy] = inputs[i];
    const nx = t.vx * speedFactor, ny = t.vy * speedFactor;
    t.x += ux;
    t.y += uy;

    // Bounce the nominal velocity off the walls
    if ((t.x - RADIUS < Math.abs(nx) + 1 && nx < 0) || (W - RADIUS - t.x < Math.abs(nx) + 1 && nx > 0)) t.vx *= -1;
    if ((t.y - RADIUS < Math.abs(ny) + 1 && ny < 0) || (H - RADIUS - t.y < Math.abs(ny) + 1 && ny > 0)) t.vy *= -1;

    // Symmetric encounters can stall the filter (a known CBF deadlock);
    // steer the nominal heading so they slide past each other.
    const nominal = Math.hypot(nx, ny);
    if (nominal > 0.1 && Math.hypot(ux, uy) < 0.25 * nominal) {
      const c = Math.cos(0.1), s = Math.sin(0.1);
      [t.vx, t.vy] = [c * t.vx - s * t.vy, s * t.vx + c * t.vy];
    }
  });

  ctx.clearRect(0, 0, W, H);
  // Draw lines first (put them behind)
  drawLines();
  // Then draw tangerines on top
  ctx.font = "48px Arial";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  tangerines.forEach(t => ctx.fillText("🍊", t.x, t.y));
  requestAnimationFrame(updateTangerines);
}

// Add debounce function to handle resize smoothly
let resizeTimeout;
window.addEventListener('resize', function() {
  // Clear the previous timeout to cancel pending resize operations
  if (resizeTimeout) {
    clearTimeout(resizeTimeout);
  }

  // Set a new timeout - will execute resize logic after 300ms of resize inactivity
  resizeTimeout = setTimeout(function() {
    if (initialized) {
      initTangerines();
    } else {
      // Just update canvas dimensions if animation not yet started
      const canvas = document.getElementById("tangerineCanvas");
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      ctx = canvas.getContext("2d");
    }
  }, 300); // Wait 300ms after resize finishes before updating
});

function inputEventHandler(a) {
    speedFactor = parseFloat(a.value) * 0.1;
    document.getElementById("speed-value").innerHTML = "<i>v</i> = " + speedFactor.toFixed(1).replace("-", "\u2212");
    if (!initialized) {
      initialized = true;
      initTangerines();
      updateTangerines();
    }
}
// Initialize canvas but don't start animation yet
const canvas = document.getElementById("tangerineCanvas");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
ctx = canvas.getContext("2d");
</script>
