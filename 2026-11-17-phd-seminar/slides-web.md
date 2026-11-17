---
# The deck for the website's PDF: the slides of slides.md from the title slide to
# Papers. This first slide only carries the headmatter, which has to equal slides.md's.
# It is hidden, because a slide that imports others overrides their keys, and `title`
# would replace the title of every imported slide.
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
hide: true
---

---
# Slidev's `--range` has no effect on a PDF export, so the range stands here. Update it
# when slides before Papers are added or removed.
src: ./slides.md#3-18
---
