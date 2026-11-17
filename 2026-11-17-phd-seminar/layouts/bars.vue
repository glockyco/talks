<script setup lang="ts">
import '@fontsource-variable/inter'
import '@fontsource-variable/jetbrains-mono'
import { useSlideContext } from '@slidev/client'

// The deck's frame: the section bar and the footer bar of the earlier AAU-style decks, with
// the title and the slide's message left-aligned between them and both logos beside the
// title. The fonts are bundled, so the slides look the same on every machine. `title`, `message` and `messageAt` come from the frontmatter.
// `sources` adds one line of citations above the footer bar.
const { $frontmatter, $page, $clicks } = useSlideContext()
const sections = ['Introduction', 'Background', 'PASDA', 'Teralizer', 'Conclusion']
</script>

<template>
  <div class="slidev-layout frame bars">
    <nav>
      <span v-for="s in sections" :key="s" :class="{ on: s === $frontmatter.section }">{{ s }}</span>
    </nav>
    <header>
      <div>
        <h1>{{ $frontmatter.title }}</h1>
        <p :class="{ later: $clicks < ($frontmatter.messageAt ?? 0) }">{{ $frontmatter.message }}</p>
      </div>
      <div class="logos">
        <img class="aau" src="/aau-logo.png" alt="Universität Klagenfurt">
        <img class="scch" src="/scch-logo.svg" alt="Software Competence Center Hagenberg">
      </div>
    </header>
    <main :class="{ cited: $frontmatter.sources }"><slot /></main>
    <p v-if="$frontmatter.sources" class="sources">{{ $frontmatter.sources }}</p>
    <footer>
      <span>2026-11-17, SCCH PhD Seminar</span>
      <span>Johann Glock: Formal Guarantees Meet Practical Constraints</span>
      <span>{{ $page }}</span>
    </footer>
  </div>
</template>

<style scoped>
nav { position: absolute; top: 0; left: 0; right: 0; height: 44px; display: grid; grid-auto-flow: column; grid-auto-columns: 1fr; background: var(--aau-dark); font-size: 22px; line-height: 44px; text-align: center; color: rgba(255, 255, 255, 0.85); }
nav span.on { background: var(--aau-light); color: #fff; font-weight: 700; }
header { position: absolute; top: 44px; left: 64px; right: 64px; height: 148px; display: flex; align-items: center; justify-content: space-between; }
h1 { margin: 0; font-size: 58px; line-height: 66px; font-weight: 700; letter-spacing: -1px; }
header p { margin: 4px 0 0; min-height: 36px; font-size: 28px; line-height: 36px; color: var(--muted); opacity: 1; }
header p.later { visibility: hidden; }
.logos { display: flex; align-items: center; gap: 28px; }
main { position: absolute; top: 192px; bottom: 60px; left: 64px; right: 64px; display: flex; align-items: center; }
main.cited { bottom: 82px; }
.sources { position: absolute; left: 64px; right: 64px; bottom: 52px; margin: 0; font-size: 20px; line-height: 24px; color: var(--muted); opacity: 1; }
footer { position: absolute; bottom: 0; left: 0; right: 0; height: 44px; display: grid; grid-template-columns: 1fr 2fr 1fr; background: var(--aau-dark); font-size: 20px; line-height: 44px; text-align: center; color: #fff; }
/* Explicit sizes, because the CSS reset ignores the height attribute of images. */
img.aau { height: 72px; width: 196px; }
img.scch { height: 92px; width: 115px; }
</style>
