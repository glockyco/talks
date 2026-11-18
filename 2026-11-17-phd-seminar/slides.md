---
# The deck: the title slide and About This Talk here, the talk from the second title slide
# to Papers in main.md, and the backup slides in backup.md. The website's PDF
# (slides-web.md) shows main.md alone.
theme: default
title: Formal Guarantees Meet Practical Constraints
author: Johann Glock
canvasWidth: 1920
aspectRatio: 16/9
fonts:
  sans: Inter Variable
  mono: JetBrains Mono Variable
  provider: none
transition: none
mcp: false
layout: cover
---

---
layout: bars
title: About This Talk
section: Before the talk
message: ""
---

<!-- About This Talk: three panels on the speaker and the thesis, and a dark one for what the talk is and which feedback is wanted. Dates: SCCH since September 2026, PhD since 2021 (glockyco.com). -->

<div class="about">
  <div class="card"><div class="card-head">Me</div><b>Johann Glock</b>at SCCH since September 2026,<br>AISYS (Software Science)</div>
  <div class="card"><div class="card-head">PhD</div><b>University of Klagenfurt</b>since 2021, supervisors:<br>Martin Pinzger and Johann Eder</div>
  <div class="card"><div class="card-head">Thesis</div><b>Final stages</b>preliminary reviews received,<br>aiming to defend in early 2027</div>
  <div class="card today"><div class="card-head">Today</div><b>The whole thesis in 20 minutes</b>Does the storyline make sense? Is anything big missing? Please let me know. :)</div>
</div>

<style>
.about { width: 100%; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.12fr) minmax(0, 1fr); gap: 24px; font-size: var(--fs-body); line-height: 1.3; }
.about .card { padding: 30px 32px 36px; }
.about .card b { display: block; margin-bottom: 6px; font-size: var(--fs-lead); line-height: 1.2; }
.about .today { grid-column: 1 / 4; padding: 36px 40px 42px; background: var(--aau-dark); color: #fff; }
.about .today .card-head { color: rgba(255, 255, 255, 0.8); }
</style>

---
src: ./main.md
---

---
src: ./backup.md
---
