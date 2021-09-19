---
layout: default
permalink: /
published: true
---

Hi!, I'm a software developer who builds robots occasionally.

This is my website, and I wonder what this knob does.

<input type="range" class="input-knob" data-src="{{site.baseurl}}/assets/images/knob70.png" data-sprites="100" min="-100" max="150" step="0.4" oninput="inputEventHandler(this)" onchange="changeEventHandler(this)"/>

<div id="knob-div" style="position: absolute; left: -100px; top: 20px; font-size: 100px; width: 100px; text-orientation: mixed; writing-mode: vertical-rl;">
NOT MUCH
</div>

<script type="text/javascript" src="{{site.baseurl}}/assets/scripts/input-knobs.js"></script>
<script type="text/javascript">
function changeEventHandler(a) {
    document.getElementById("knob-div").style.left = a.value -100 + "px";
    console.log(a.value);
}
function inputEventHandler(a) {
    document.getElementById("knob-div").style.left = a.value -100 + "px";
    console.log(a.value);
}
</script>