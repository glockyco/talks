<script setup lang="ts">
import '@fontsource-variable/inter'
import '@fontsource-variable/jetbrains-mono'
import { talk } from '../talk'

// The title slide: the deck's fonts, colors and logos, without the section bar and the
// footer bar, because it stands before the talk. What it shows comes from talk.ts.
</script>

<template>
  <div class="slidev-layout frame cover">
    <div class="logos">
      <img class="aau" src="/aau-logo.png" alt="Universität Klagenfurt">
      <img class="scch" src="/scch-logo.svg" alt="Software Competence Center Hagenberg">
    </div>
    <div class="head">
      <h1><span v-for="l in talk.titleLines" :key="l">{{ l }}<br></span></h1>
      <p class="sub"><span v-for="l in talk.subtitleLines" :key="l">{{ l }}<br></span></p>
    </div>
    <div class="people">
      <div class="card who"><div class="label">Speaker</div>{{ talk.speaker }}</div>
      <div class="card who"><div class="label">Supervisors</div><span v-for="s in talk.supervisors" :key="s">{{ s }}<br></span></div>
      <div class="card who"><div class="label">{{ talk.event }}</div>{{ talk.date }}</div>
    </div>
  </div>
</template>

<style scoped>
.logos { position: absolute; top: 64px; right: 64px; display: flex; align-items: center; gap: 36px; }
img.aau { height: 96px; width: 261px; }
img.scch { height: 122px; width: 153px; }
/* The class in front outranks the theme's rule for h1. */
.cover h1 { margin: 0; font-size: 128px; font-weight: 700; letter-spacing: -3px; line-height: 1.14; }
.cover .sub { margin: 40px 0 0; font-size: 52px; line-height: 1.25; color: var(--muted); opacity: 1; }
.head { position: absolute; top: 250px; left: 64px; right: 64px; }
.people { position: absolute; left: 64px; right: 64px; bottom: 64px; display: flex; gap: 24px; font-size: var(--fs-body); line-height: 1.3; }
.who { flex: 1; }
.label { margin-bottom: 8px; font-size: var(--fs-note); font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); }
</style>
