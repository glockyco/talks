<script setup lang="ts">
import { computed } from 'vue'

// Detected mutants against the time to create the tests (EvoSuite's search, plus Teralizer's
// generalization where it runs), for EvoSuite alone and for EvoSuite followed by
// Teralizer. From Tables tab:pareto-eqbench and tab:pareto-commons of the thesis (the
// Pareto points) and Section sec:teralizer-rq4 (EvoSuite with 60 s on EqBench, which is
// not on the frontier).
//   stairs: for each of the two, the most detection that a runtime budget buys
//   chains: one line per EvoSuite search budget, from EvoSuite alone through its
//           generalized configurations
// Dots and chains take the color of their EvoSuite search budget, so each generalized
// configuration shows which tests it started from.
//   gains:  the two comparisons against EvoSuite with 60 s on EqBench, as arrows, with
//           their numbers unless gainLabels is off
const props = withDefaults(defineProps<{
  dataset?: 'eqbench' | 'commons'
  mode?: 'stairs' | 'chains'
  width?: number
  height?: number
  gains?: boolean
  gainLabels?: boolean
}>(), { dataset: 'eqbench', mode: 'stairs', width: 1100, height: 430, gains: false, gainLabels: true })

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

// A staircase: the detection of the best configuration that fits into a runtime.
function stairs(points: Point[]) {
  const out = [`${x(points[0].s)},${y(points[0].det)}`]
  for (let i = 1; i < points.length; i++) {
    out.push(`${x(points[i].s)},${y(points[i - 1].det)}`, `${x(points[i].s)},${y(points[i].det)}`)
  }
  out.push(`${xEnd.value},${y(points[points.length - 1].det)}`)
  return out
}
const area = (points: Point[]) => [`${x(points[0].s)},${yBase.value}`, ...stairs(points), `${xEnd.value},${yBase.value}`].join(' ')
const chains = computed(() => d.value.alone.map(a => ({
  budget: a.budget,
  points: [a, ...d.value.combined.filter(c => c.budget === a.budget)].map(p => `${x(p.s)},${y(p.det)}`).join(' '),
})))

// EvoSuite with 60 s, the first generalized configuration with as much detection, and the
// detection that the generalized configurations reach within its runtime.
const ref = computed(() => d.value.alone[2])
const same = computed(() => d.value.combined.find(c => c.det >= ref.value.det)!)
const within = computed(() => Math.max(...d.value.combined.filter(c => c.s <= ref.value.s).map(c => c.det)))
const best = computed(() => [...d.value.combined].reverse().find(c => c.s <= ref.value.s && c.det === within.value)!)
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

    <template v-if="mode === 'stairs'">
      <polygon :points="area(d.combined)" class="area with" />
      <polygon :points="area(d.alone)" class="area alone" />
      <polyline :points="stairs(d.combined).join(' ')" class="stair with" />
      <polyline :points="stairs(d.alone).join(' ')" class="stair alone" />
      <text :x="xEnd - 8" :y="y(d.combined[d.combined.length - 1].det) - 18" text-anchor="end" class="label with">EvoSuite + Teralizer</text>
      <text :x="xEnd - 8" :y="y(ref.det) + 36" text-anchor="end" class="label">EvoSuite alone</text>
    </template>
    <template v-else>
      <polyline v-for="c in chains" :key="c.budget" :points="c.points" :class="['chain', cls(c.budget)]" />
    </template>

    <template v-if="gains">
      <line :x1="x(ref.s) - 16" :x2="x(same.s) + 14" :y1="y(ref.det)" :y2="y(ref.det)" class="gain" />
      <path :d="`M${x(same.s) + 26},${y(ref.det) - 10} l-14,10 l14,10`" class="gain head" />
      <text v-if="gainLabels" :x="x(ref.s) - 24" :y="y(ref.det) + 36" text-anchor="end" class="gaintext">31.9% less time</text>
      <!-- The detection that the arrow reaches belongs to a configuration with less runtime. -->
      <line v-if="mode === 'chains'" :x1="x(best.s) + 12" :x2="x(ref.s)" :y1="y(within)" :y2="y(within)" class="level" />
      <line :x1="x(ref.s)" :x2="x(ref.s)" :y1="y(ref.det) - 16" :y2="y(within) + 8" class="gain" />
      <path :d="`M${x(ref.s) - 10},${y(within) + 20} l10,-14 l10,14`" class="gain head" />
      <text v-if="gainLabels" :x="x(ref.s) - 20" :y="(y(ref.det) + y(within)) / 2 + 4" text-anchor="end" class="gaintext">+2.2 points</text>
    </template>

    <circle v-for="p in d.combined" :key="p.s" :cx="x(p.s)" :cy="y(p.det)" r="9" :class="['dot', cls(p.budget)]" />
    <g v-for="p in d.alone" :key="p.s">
      <circle :cx="x(p.s)" :cy="y(p.det)" r="12" :class="['dot', 'alone', cls(p.budget)]" />
      <!-- Each label avoids the line that leaves its point. -->
      <template v-if="mode === 'stairs'">
        <text v-if="p.budget === '1 s'" :x="x(p.s)" :y="y(p.det) + 44" text-anchor="middle" :class="['budget', cls(p.budget)]">{{ p.budget }}</text>
        <text v-else-if="p.budget === '10 s'" :x="x(p.s) - 22" :y="y(p.det) + 9" text-anchor="end" :class="['budget', cls(p.budget)]">{{ p.budget }}</text>
        <text v-else :x="x(p.s) + 22" :y="y(p.det) + 38" :class="['budget', cls(p.budget)]">{{ p.budget }}</text>
      </template>
      <template v-else>
        <text v-if="p.budget === '10 s'" :x="x(p.s) - 22" :y="y(p.det) + 9" text-anchor="end" :class="['budget', cls(p.budget)]">{{ p.budget }}</text>
        <text v-else :x="x(p.s) + 8" :y="y(p.det) + 46" :class="['budget', cls(p.budget)]">{{ p.budget }}</text>
      </template>
    </g>
  </svg>
</template>

<style scoped>
.pareto { display: block; font-family: var(--sans); overflow: visible; flex: none; }
.grid { stroke: var(--rule); stroke-width: 1.5; }
.axis { stroke: var(--muted); stroke-width: 2; }
.tick { font-size: var(--fs-note); fill: var(--muted); }
.area.with { fill: #8fa6ad; opacity: 0.32; }
.area.alone { fill: var(--panel); }
.stair { fill: none; stroke-width: 4; stroke-linejoin: round; }
.stair.with { stroke: #4a626b; }
.stair.alone { stroke: var(--ink); }
.chain { fill: none; stroke-width: 5; stroke-linejoin: round; }
.chain.b1 { stroke: var(--budget-1); }
.chain.b10 { stroke: var(--budget-10); }
.chain.b60 { stroke: var(--budget-60); }
.dot { stroke: #fff; stroke-width: 2; }
.dot.b1 { fill: var(--budget-1); }
.dot.b10 { fill: var(--budget-10); }
.dot.b60 { fill: var(--budget-60); }
.dot.alone { stroke: var(--ink); stroke-width: 5; }
.label { font-size: var(--fs-small); font-weight: 700; fill: var(--ink); }
.label.with { fill: #3a5059; }
.budget { font-size: var(--fs-note); font-weight: 700; }
.budget.b1 { fill: #0c7a78; }
.budget.b10 { fill: var(--budget-10); }
.budget.b60 { fill: var(--budget-60); }
.gain { stroke: var(--ink); stroke-width: 5; stroke-linecap: round; fill: none; }
.gain.head { stroke-linejoin: round; }
.level { stroke: var(--ink); stroke-width: 2.5; stroke-dasharray: 6 7; }
.gaintext { font-size: var(--fs-note); font-weight: 700; fill: var(--ink); }
</style>
