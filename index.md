---
layout: default
permalink: /
published: true
---

Hi!, I'm a robotics researcher currently working in marine robotics.

This is my website. Wanna <i>press</i> the button?

<input type="range" class="input-knob" data-src="{{site.baseurl}}/assets/images/knob70.png" data-sprites="100" min="-150" max="150" step="0.4" oninput="inputEventHandler(this)" onchange="changeEventHandler(this)"/>

<canvas id="tangerineCanvas" style="position: fixed; top: 0; left: 0; z-index: -1;"></canvas>

<script type="text/javascript" src="{{site.baseurl}}/assets/scripts/input-knobs.js"></script>
<script type="text/javascript">
let tangerines = [];
let speedFactor = 1;
let ctx;
let initialized = false;
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

  tangerines = []; // Clear existing oranges
  for (let i = 0; i < orangeCount; i++) {
    tangerines.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 2,
      vy: (Math.random() - 0.5) * 2
    });
  }
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
  ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  // Draw lines first (put them behind)
  drawLines();
  // Then draw tangerines on top
  ctx.font = "48px Arial";
  tangerines.forEach(t => {
    t.x += t.vx * speedFactor;
    t.y += t.vy * speedFactor;
    // Center the emoji to its coordinates
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("🍊", t.x, t.y);
    if (t.x < 0 || t.x > ctx.canvas.width ) t.vx *= -1;
    if (t.y < 0 || t.y > ctx.canvas.height ) t.vy *= -1;
  });
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

function changeEventHandler(a) {
    console.log(a.value);
}
function inputEventHandler(a) {
    console.log(a.value);
    speedFactor = parseFloat(a.value) * 0.1;
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
