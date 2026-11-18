<script setup lang="ts">
import { computed } from 'vue'

// The talk's process as one picture. The input is code: the two versions of the method,
// and for Teralizer a developer test. Symbolic analysis yields a path condition and a
// symbolic output, and two routes use them:
//   top:    a solver, and PASDA, which classifies what the solver leaves without a proof
//   bottom: Teralizer, which builds a generalized test, and property-based testing (PBT),
//           which samples and runs it
// (thesis, Chapter 7: Teralizer "changes the consumer of symbolic analysis results from a
// constraint solver to a property-based test runner").
//   directions: the top route, from `step` 1 the three reasons of the Background slide, and the two
//               directions of thesis Section 4.7 (`step` 2 and 3)
//   summary:    both routes, and from `step` 1 what limits each stage
// The analysis follows all paths for the top route and the one path of a test for the
// bottom route, which the box says at the height of each route.
// A limitation is a chip on the edge of the box it comes from: on the top edge for the top
// route, on the bottom edge for the bottom route. Both stages share one geometry, so that
// the summary is the picture of the transition with the second route filled in.
// The code is from LoanCode (v1 line 7, v2 line 3, the developer test). The results are
// the verdict lane of Best-Effort Classification and the sampled inputs of Test Generalization, which are illustrative.
const props = defineProps<{ stage: 'directions' | 'summary', step: number }>()

const W = 1792
const H = 500
// Both routes are drawn on the summary.
const summary = computed(() => props.stage === 'summary')
// The summary has no direction above the routes, so its picture starts at the labels and
// sits centered on the slide.
const Y0 = computed(() => summary.value ? 104 : 0)
const yA = 192
const yB = 392
const BOX = 112
const top = yA - BOX / 2
const bottom = yB + BOX / 2
const yMid = (yA + yB) / 2

const cards = { x: 60, w: 280 }
const analysis = { x: 384, w: 210 }
const group = { x: 638, w: 260 }
const first = { x: 942, w: 200 }
const second = { x: 1182, w: 200 }
const OUT = { x: 1426, w: 366 }
const ox = (amount: number) => OUT.x + amount * OUT.w / 100
const mid = (b: { x: number, w: number }) => b.x + b.w / 2
// Advance of one character of the code font at 22 px, to place the marks.
const CH = 13.2
const code = cards.x + 16

const samples = [4, 11, 27, 33, 40, 47, 55]
const chip = (text: string) => 28 + text.length * 11.6
const above = [
  { at: mid(analysis), text: 'path explosion' },
  { at: mid(group), text: 'unmodeled behavior' },
  { at: mid(first), text: 'solver limitations' },
]
const below = [
  { at: mid(analysis), text: 'unsupported tests' },
  { at: mid(group), text: 'unmodeled behavior' },
  { at: mid(second), text: 'unsampled inputs' },
]
</script>

<template>
  <svg :width="W" :height="H - Y0" :viewBox="`0 ${Y0} ${W} ${H - Y0}`" class="routes" role="img"
    aria-label="From the code of two versions through symbolic analysis and a solver to PASDA, and from a developer test through the same analysis to Teralizer and property-based testing">
    <defs>
      <marker id="routes-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto">
        <path d="M0,0 L10,5 L0,10 z" class="tip" />
      </marker>
    </defs>

    <text x="0" :y="yA - 20" class="ver">v1</text>
    <rect :x="cards.x" :y="top" :width="cards.w" height="52" rx="8" class="card" />
    <rect :x="code + 11 * CH - 4" :y="top + 11" :width="2 * CH + 8" height="30" rx="4" class="mark" />
    <text :x="code" :y="top + 34" class="code">p >= <tspan class="num">0.8</tspan> ? <tspan class="num">60</tspan> : <tspan class="num">5</tspan></text>
    <text x="0" :y="yA + 40" class="ver">v2</text>
    <rect :x="cards.x" :y="yA + 4" :width="cards.w" height="52" rx="8" class="card" />
    <rect :x="code + 11 * CH - 4" :y="yA + 15" :width="2 * CH + 8" height="30" rx="4" class="mark" />
    <text :x="code" :y="yA + 38" class="code"><tspan class="kw">int</tspan> <tspan class="num">FULL</tspan> = <tspan class="num">50</tspan></text>
    <line :x1="cards.x + cards.w + 8" :x2="analysis.x - 6" :y1="yA" :y2="yA" class="flow" marker-end="url(#routes-arrow)" />

    <rect :x="analysis.x" :y="top" :width="analysis.w" :height="bottom - top" rx="16" class="given" />
    <text :x="mid(analysis)" :y="yMid - 4" text-anchor="middle" class="step">symbolic</text>
    <text :x="mid(analysis)" :y="yA + 8" text-anchor="middle" class="item">all paths</text>
    <text v-if="summary || step >= 3" :x="mid(analysis)" :y="yB + 8" text-anchor="middle" class="item">one path</text>
    <text :x="mid(analysis)" :y="yMid + 32" text-anchor="middle" class="step">analysis</text>
    <line :x1="analysis.x + analysis.w" :x2="group.x - 6" :y1="yA" :y2="yA" class="flow" marker-end="url(#routes-arrow)" />

    <rect :x="group.x" :y="top" :width="group.w" :height="bottom - top" rx="14" class="group" />
    <rect :x="group.x + 12" :y="yMid - 54" :width="group.w - 24" height="48" rx="8" class="in" />
    <text :x="mid(group)" :y="yMid - 21" text-anchor="middle" class="item">path condition</text>
    <rect :x="group.x + 12" :y="yMid + 6" :width="group.w - 24" height="48" rx="8" class="out" />
    <text :x="mid(group)" :y="yMid + 39" text-anchor="middle" class="item">symbolic output</text>

    <line :x1="group.x + group.w" :x2="first.x - 6" :y1="yA" :y2="yA" class="flow" marker-end="url(#routes-arrow)" />
    <rect :x="first.x" :y="top" :width="first.w" :height="BOX" rx="16" class="given" />
    <text :x="mid(first)" :y="yA + 11" text-anchor="middle" class="step">solver</text>
    <line :x1="first.x + first.w" :x2="second.x - 6" :y1="yA" :y2="yA" class="flow" marker-end="url(#routes-arrow)" />
    <rect :x="second.x" :y="top" :width="second.w" :height="BOX" rx="16" class="new" />
    <text :x="mid(second)" :y="yA + 11" text-anchor="middle" class="step light">PASDA</text>
    <line :x1="second.x + second.w" :x2="OUT.x - 8" :y1="yA" :y2="yA" class="flow" marker-end="url(#routes-arrow)" />
    <rect :x="ox(0)" :y="yA - 22" :width="ox(50) - ox(0) - 3" height="44" rx="8" class="eq" />
    <text :x="ox(25)" :y="yA + 9" text-anchor="middle" class="chiptext">EQ</text>
    <rect :x="ox(50) + 3" :y="yA - 22" :width="ox(100) - ox(50) - 3" height="44" rx="8" class="mneq" />
    <text :x="ox(75)" :y="yA + 9" text-anchor="middle" class="chiptext">MAYBE_NEQ</text>

    <template v-if="summary">
      <rect :x="cards.x" :y="yB - BOX / 2" :width="cards.w" :height="BOX" rx="8" class="card" />
      <text :x="code" :y="yB - 22" class="code"><tspan class="anno">@Test</tspan></text>
      <text :x="code" :y="yB + 12" class="code"><tspan class="call">assertEquals</tspan>(<tspan class="num">20</tspan>, …)</text>
      <line :x1="cards.x + cards.w + 8" :x2="analysis.x - 6" :y1="yB" :y2="yB" class="flow" marker-end="url(#routes-arrow)" />
      <line :x1="analysis.x + analysis.w" :x2="group.x - 6" :y1="yB" :y2="yB" class="flow" marker-end="url(#routes-arrow)" />

      <line :x1="group.x + group.w" :x2="first.x - 6" :y1="yB" :y2="yB" class="flow" marker-end="url(#routes-arrow)" />
      <rect :x="first.x" :y="yB - BOX / 2" :width="first.w" :height="BOX" rx="16" class="new" />
      <text :x="mid(first)" :y="yB + 11" text-anchor="middle" class="step light">Teralizer</text>
      <line :x1="first.x + first.w" :x2="second.x - 6" :y1="yB" :y2="yB" class="flow" marker-end="url(#routes-arrow)" />
      <rect :x="second.x" :y="yB - BOX / 2" :width="second.w" :height="BOX" rx="16" class="given" />
      <text :x="mid(second)" :y="yB + 11" text-anchor="middle" class="step">PBT</text>
      <line :x1="second.x + second.w" :x2="OUT.x - 8" :y1="yB" :y2="yB" class="flow" marker-end="url(#routes-arrow)" />
      <line :x1="ox(0)" :x2="ox(60)" :y1="yB" :y2="yB" class="span ink" />
      <line :x1="ox(60) + 12" :x2="ox(100)" :y1="yB" :y2="yB" class="span off" />
      <line :x1="ox(60)" :x2="ox(60)" :y1="yB - 12" :y2="yB + 12" class="cap" />
      <template v-for="a in samples" :key="a">
        <circle v-if="a <= 50" :cx="ox(a)" :cy="yB" r="8" class="pass" />
        <path v-else :d="`M${ox(a) - 6},${yB - 6} l12,12 m0,-12 l-12,12`" class="fail" />
      </template>
    </template>

    <g v-if="step >= 1">
      <g v-for="b in above" :key="b.text" :transform="`translate(${b.at}, ${top})`">
        <rect :x="-chip(b.text) / 2" y="-21" :width="chip(b.text)" height="42" rx="8" class="limit" />
        <text y="8" text-anchor="middle" class="limittext">{{ b.text }}</text>
      </g>
    </g>
    <g v-if="summary && step >= 1">
      <g v-for="b in below" :key="b.text" :transform="`translate(${b.at}, ${bottom})`">
        <rect :x="-chip(b.text) / 2" y="-21" :width="chip(b.text)" height="42" rx="8" class="limit" />
        <text y="8" text-anchor="middle" class="limittext">{{ b.text }}</text>
      </g>
    </g>

    <template v-if="!summary">
      <g v-if="step >= 2">
        <path :d="`M${analysis.x},${top - 36} V${top - 50} H${first.x + first.w} V${top - 36}`" class="brace" />
        <text :x="analysis.x" :y="top - 68"><tspan class="step">direction 1</tspan><tspan class="item" dx="14">model and solve more</tspan></text>
      </g>
      <g v-if="step >= 3">
        <line :x1="group.x + group.w" :x2="first.x - 6" :y1="yB" :y2="yB" class="flow" marker-end="url(#routes-arrow)" />
        <rect :x="first.x" :y="yB - BOX / 2" :width="second.x + second.w - first.x" :height="BOX" rx="16" class="open" />
        <text :x="(first.x + second.x + second.w) / 2" :y="yB - 6" text-anchor="middle" class="step">direction 2</text>
        <text :x="(first.x + second.x + second.w) / 2" :y="yB + 30" text-anchor="middle" class="item">use them without the solver</text>
      </g>
    </template>
  </svg>
</template>

<style scoped>
.routes { display: block; font-family: var(--sans); overflow: visible; flex: none; }
.group { fill: none; stroke: var(--rule); stroke-width: 2; stroke-dasharray: 6 6; }
.given { fill: var(--panel); stroke: var(--rule); stroke-width: 2; }
.new { fill: var(--aau-dark); }
.open { fill: none; stroke: var(--aau-dark); stroke-width: 3; stroke-dasharray: 10 8; }
.card { fill: #fff; stroke: var(--rule); stroke-width: 2; }
.mark { fill: #fbe3cf; stroke: #e2711d; stroke-width: 2; }
.step { font-size: var(--fs-small); font-weight: 700; fill: var(--ink); }
.step.light { fill: #fff; }
.item { font-size: var(--fs-note); font-weight: 400; fill: var(--ink); }
.ver { font-size: var(--fs-note); font-weight: 700; fill: var(--muted); }
.code { font-family: var(--mono); font-variant-ligatures: none; font-size: 22px; fill: var(--ink); white-space: pre; }
.code .kw { fill: #6b4bb0; }
.code .num { fill: #b4530f; }
.code .call { fill: #0b6e8e; }
.code .anno { fill: #6b4bb0; font-weight: 700; }
.in { fill: var(--spec-in); }
.out { fill: var(--spec-out); }
.flow { fill: none; stroke: var(--muted); stroke-width: 4; }
.brace { fill: none; stroke: var(--muted); stroke-width: 3; stroke-linejoin: round; }
.tip { fill: var(--muted); }
.eq { fill: var(--eq); }
.mneq { fill: var(--maybe-neq); }
.chiptext { font-size: 22px; font-weight: 700; fill: #fff; }
.limit { fill: #fff; stroke: var(--ink); stroke-width: 2.5; }
.limittext { font-size: 22px; fill: var(--ink); }
.span.ink { stroke: var(--ink); stroke-width: 4; stroke-linecap: round; }
.span.off { stroke: var(--muted); stroke-width: 4; stroke-linecap: round; stroke-dasharray: 2 12; }
.cap { stroke: var(--ink); stroke-width: 5; stroke-linecap: round; }
.pass { fill: #fff; stroke: var(--ink); stroke-width: 3; }
.fail { stroke: #c2410c; stroke-width: 5; stroke-linecap: round; fill: none; }
</style>
