<script setup lang="ts">
import { PAIRS as TOTAL, maybeCount, results } from '../data/pasda'

// Pairs of the ARDiff benchmark (141) that each tool proves at the six timeouts, and the
// pairs for which PASDA adds a best-effort verdict (data/pasda.ts).
const props = withDefaults(defineProps<{ width?: number }>(), { width: 1100 })

const rows = Object.values(results)
const timeouts = rows.map(r => r.label)
const proven = {
  PASDA: rows.map(r => r.proven.PASDA),
  PRV: rows.map(r => r.proven.PRV),
  ARDiff: rows.map(r => r.proven.ARDiff),
  DSE: rows.map(r => r.proven.DSE),
}
// MAYBE_EQ plus MAYBE_NEQ of PASDA per timeout.
const maybe = rows.map(maybeCount)

const LEFT = 84
const RIGHT = 220
const TOP = 16
const PH = 500
const H = TOP + PH + 78
const x = (i: number) => LEFT + (i / 5) * (props.width - LEFT - RIGHT)
const y = (n: number) => TOP + (1 - n / TOTAL) * PH
const line = (v: number[]) => v.map((n, i) => `${x(i)},${y(n)}`).join(' ')
const band = [...proven.PASDA.map((n, i) => `${x(i)},${y(n)}`),
  ...proven.PASDA.map((n, i) => `${x(i)},${y(n + maybe[i])}`).reverse()].join(' ')
</script>

<template>
  <svg :width="width" :height="H" :viewBox="`0 0 ${width} ${H}`" class="time" role="img"
    aria-label="Proven pairs per tool over the timeout, with PASDA's best-effort verdicts">
    <line v-for="n in [0, 50, 100, 141]" :key="n" :x1="LEFT" :x2="x(5)" :y1="y(n)" :y2="y(n)" class="grid" :class="{ top: n === 141 }" />
    <text v-for="n in [0, 50, 100, 141]" :key="n" :x="LEFT - 14" :y="y(n) + 8" text-anchor="end" class="tick">{{ n }}</text>
    <text :x="LEFT - 60" :y="TOP + PH / 2" text-anchor="middle" class="tick" :transform="`rotate(-90 ${LEFT - 60} ${TOP + PH / 2})`">program pairs</text>
    <text v-for="(t, i) in timeouts" :key="t" :x="x(i)" :y="y(0) + 34" text-anchor="middle" class="tick">{{ t }}</text>
    <text :x="(LEFT + x(5)) / 2" :y="H - 6" text-anchor="middle" class="tick">timeout</text>

    <polygon :points="band" class="band" />
    <text :x="x(2.5)" :y="y(118) + 8" text-anchor="middle" class="inband">best-effort verdict</text>

    <g v-for="(v, tool) in proven" :key="tool">
      <polyline :points="line(v)" class="line" :class="{ main: tool === 'PASDA' }" />
      <circle v-for="(n, i) in v" :key="i" :cx="x(i)" :cy="y(n)" :r="tool === 'PASDA' ? 8 : 6" class="dot" :class="{ main: tool === 'PASDA' }" />
      <text :x="x(5) + 18" :y="y(v[5]) + (tool === 'PRV' ? 16 : tool === 'PASDA' ? -4 : 12)" class="name" :class="{ main: tool === 'PASDA' }">{{ tool }} {{ v[5] }}</text>
    </g>
    <text :x="x(5) + 18" :y="y(120) + 8" class="name maybe">+{{ maybe[5] }}</text>
    <text :x="x(5) + 18" :y="y(139) + 6" class="name">no verdict {{ TOTAL - proven.PASDA[5] - maybe[5] }}</text>
  </svg>
</template>

<style scoped>
.time { display: block; font-family: var(--sans); overflow: visible; flex: none; }
.grid { stroke: var(--rule); stroke-width: 1.5; }
.grid.top { stroke: var(--muted); stroke-dasharray: 5 6; }
.tick { font-size: var(--fs-note); fill: var(--muted); }
.band { fill: var(--maybe); opacity: 0.55; }
.inband { font-size: var(--fs-small); font-weight: 700; fill: var(--chip-ink); }
.line { fill: none; stroke: var(--muted); stroke-width: 3; }
.line.main { stroke: var(--eq); stroke-width: 6; }
.dot { fill: var(--muted); }
.dot.main { fill: var(--eq); }
.name { font-size: var(--fs-small); fill: var(--muted); }
.name.main { font-weight: 700; fill: var(--eq); }
.name.maybe { font-weight: 700; fill: #8a6a00; }
</style>
