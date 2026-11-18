<script setup lang="ts">
import { computed } from 'vue'

// Detected mutants against the time to create the tests (EvoSuite's search, plus Teralizer's
// generalization where it runs), for EvoSuite alone and for EvoSuite followed by
// Teralizer. From Tables tab:pareto-eqbench and tab:pareto-commons of the thesis (the
// Pareto points) and Section sec:teralizer-rq4 (EvoSuite with 60 s on EqBench, which is
// not on the frontier).
// One line per EvoSuite search budget, from EvoSuite alone through its generalized
// configurations. Dots and lines take the color of their search budget, so each generalized
// configuration shows which tests it started from.
const props = withDefaults(defineProps<{
  dataset?: 'eqbench' | 'commons'
  width?: number
  height?: number
}>(), { dataset: 'eqbench', width: 1100, height: 430 })

type Point = { budget: string, det: number, s: number }
const point = ([budget, det, s]: (string | number)[]): Point => ({ budget: budget as string, det: det as number, s: s as number })
const data = {
  eqbench: {
    alone: [['1 s', 48.1, 26479], ['10 s', 50.6, 29861], ['60 s', 51.6, 55075]].map(point),
    combined: [
      ['1 s', 50.7, 36728], ['1 s', 51.4, 37457], ['1 s', 51.7, 37532],
      ['10 s', 51.9, 41525], ['10 s', 53.6, 42256], ['10 s', 53.8, 45398], ['10 s', 53.8, 48269], ['10 s', 54.1, 62938],
      ['60 s', 54.5, 68093], ['60 s', 54.7, 68782], ['60 s', 54.8, 75081], ['60 s', 55.0, 93017],
    ].map(point),
    hours: [6, 27], det: [45.6, 56], xTicks: [10, 15, 20, 25], yTicks: [48, 50, 52, 54],
  },
  commons: {
    alone: [['1 s', 56.8, 4649], ['10 s', 57.3, 5597], ['60 s', 58.1, 10240]].map(point),
    combined: [
      ['1 s', 57.9, 7294],
      ['10 s', 58.1, 10445], ['10 s', 58.4, 10603], ['10 s', 58.4, 11082], ['10 s', 58.5, 13270],
      ['60 s', 59.3, 13939], ['60 s', 59.4, 14728], ['60 s', 59.5, 15736],
    ].map(point),
    hours: [1, 4.7], det: [55.8, 60], xTicks: [2, 3, 4], yTicks: [57, 58, 59],
  },
}
const d = computed(() => data[props.dataset])

const LEFT = 118
const RIGHT = 36
const TOP = 44
const H = computed(() => TOP + props.height + 78)
const x = (s: number) => LEFT + ((s / 3600 - d.value.hours[0]) / (d.value.hours[1] - d.value.hours[0])) * (props.width - LEFT - RIGHT)
const y = (det: number) => TOP + (1 - (det - d.value.det[0]) / (d.value.det[1] - d.value.det[0])) * props.height
// The class of a search budget: b1, b10 or b60.
const cls = (budget: string) => `b${Number.parseInt(budget)}`
const xEnd = computed(() => props.width - RIGHT)
const yBase = computed(() => TOP + props.height)

const chains = computed(() => d.value.alone.map(a => ({
  budget: a.budget,
  points: [a, ...d.value.combined.filter(c => c.budget === a.budget)].map(p => `${x(p.s)},${y(p.det)}`).join(' '),
})))
</script>

<template>
  <svg :width="width" :height="H" :viewBox="`0 0 ${width} ${H}`" class="pareto" role="img"
    aria-label="Detected mutants against the time to create the tests, for EvoSuite alone and with Teralizer">
    <line v-for="t in d.yTicks" :key="t" :x1="LEFT" :x2="xEnd" :y1="y(t)" :y2="y(t)" class="grid" />
    <text v-for="t in d.yTicks" :key="t" :x="LEFT - 14" :y="y(t) + 8" text-anchor="end" class="tick">{{ t }}%</text>
    <text :x="LEFT - 98" :y="TOP + height / 2" text-anchor="middle" class="tick" :transform="`rotate(-90 ${LEFT - 98} ${TOP + height / 2})`">detected mutants</text>
    <line :x1="LEFT" :x2="xEnd" :y1="yBase" :y2="yBase" class="axis" />
    <text v-for="t in d.xTicks" :key="t" :x="x(t * 3600)" :y="yBase + 34" text-anchor="middle" class="tick">{{ t }} h</text>
    <text :x="(LEFT + xEnd) / 2" :y="H - 6" text-anchor="middle" class="tick">time to create the tests</text>

    <polyline v-for="c in chains" :key="c.budget" :points="c.points" :class="['chain', cls(c.budget)]" />

    <circle v-for="p in d.combined" :key="p.s" :cx="x(p.s)" :cy="y(p.det)" r="9" :class="['dot', cls(p.budget)]" />
    <g v-for="p in d.alone" :key="p.s">
      <circle :cx="x(p.s)" :cy="y(p.det)" r="12" :class="['dot', 'alone', cls(p.budget)]" />
      <!-- Each label avoids the line that leaves its point. -->
      <text v-if="p.budget === '10 s'" :x="x(p.s) - 22" :y="y(p.det) + 9" text-anchor="end" :class="['budget', cls(p.budget)]">{{ p.budget }}</text>
      <text v-else :x="x(p.s) + 8" :y="y(p.det) + 46" :class="['budget', cls(p.budget)]">{{ p.budget }}</text>
    </g>
  </svg>
</template>

<style scoped>
.pareto { display: block; font-family: var(--sans); overflow: visible; flex: none; }
.grid { stroke: var(--rule); stroke-width: 1.5; }
.axis { stroke: var(--muted); stroke-width: 2; }
.tick { font-size: var(--fs-note); fill: var(--muted); }
.chain { fill: none; stroke-width: 5; stroke-linejoin: round; }
.chain.b1 { stroke: var(--budget-1); }
.chain.b10 { stroke: var(--budget-10); }
.chain.b60 { stroke: var(--budget-60); }
.dot { stroke: #fff; stroke-width: 2; }
.dot.b1 { fill: var(--budget-1); }
.dot.b10 { fill: var(--budget-10); }
.dot.b60 { fill: var(--budget-60); }
.dot.alone { stroke: var(--ink); stroke-width: 5; }
.budget { font-size: var(--fs-note); font-weight: 700; }
.budget.b1 { fill: #0c7a78; }
.budget.b10 { fill: var(--budget-10); }
.budget.b60 { fill: var(--budget-60); }
</style>
