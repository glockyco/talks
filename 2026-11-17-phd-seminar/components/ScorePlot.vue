<script setup lang="ts">
import { computed } from 'vue'

// The repayment score p of approvedAmount over the variable risk of the code, with the two
// thresholds and the three branches they select.
// risk = (3.0 * debt - income) / 100.0, p = 1 / (1 + Math.exp(risk))
const props = withDefaults(defineProps<{ width?: number }>(), { width: 800 })

const LEFT = 50
const TOP = 14
const NAMES = 236
const PH = 250
const H = TOP + PH + 70
const R = 4.2

const PW = computed(() => props.width - LEFT - NAMES)
const p = (risk: number) => 1 / (1 + Math.exp(risk))
const x = (risk: number) => LEFT + ((risk + R) / (2 * R)) * PW.value
const y = (v: number) => TOP + (1 - v) * PH
const curve = computed(() => Array.from({ length: 121 }, (_, i) => -R + (i * 2 * R) / 120)
  .map(r => `${x(r)},${y(p(r))}`).join(' '))

const bands = [
  { name: 'full approval', lo: 0.8, hi: 1, cls: 'full' },
  { name: 'partial approval', lo: 0.5, hi: 0.8, cls: 'partial' },
  { name: 'rejection', lo: 0, hi: 0.5, cls: 'reject' },
]
</script>

<template>
  <svg :width="width" :height="H" :viewBox="`0 0 ${width} ${H}`" class="score" role="img"
    aria-label="Repayment score p over the risk, with the thresholds 0.5 and 0.8">
    <g v-for="b in bands" :key="b.name">
      <rect :x="LEFT" :y="y(b.hi)" :width="PW" :height="y(b.lo) - y(b.hi) - 2" :class="['band', b.cls]" />
      <rect :x="LEFT + PW + 14" :y="y(b.hi) + 4" width="8" :height="y(b.lo) - y(b.hi) - 10" rx="4" :class="['key', b.cls]" />
      <text :x="LEFT + PW + 34" :y="(y(b.hi) + y(b.lo)) / 2 + 8" class="name">{{ b.name }}</text>
    </g>
    <text v-for="v in [0, 0.5, 0.8, 1]" :key="v" :x="LEFT - 12" :y="y(v) + 8" text-anchor="end" class="tick">{{ v }}</text>
    <line :x1="LEFT" :x2="LEFT + PW" :y1="y(0)" :y2="y(0)" class="axis" />
    <text v-for="r in [-4, -2, 0, 2, 4]" :key="r" :x="x(r)" :y="y(0) + 30" text-anchor="middle" class="tick">{{ r }}</text>
    <text :x="LEFT + PW / 2" :y="H - 6" text-anchor="middle" class="var">risk</text>
    <text :x="LEFT + PW - 14" :y="TOP + 30" text-anchor="end" class="var">p</text>
    <polyline :points="curve" class="curve" />
  </svg>
</template>

<style scoped>
.score { display: block; font-family: var(--sans); overflow: visible; flex: none; }
.band.full { fill: var(--branch-full); opacity: 0.28; }
.band.partial { fill: var(--branch-partial); opacity: 0.28; }
.band.reject { fill: var(--branch-reject); opacity: 0.28; }
.key.full { fill: var(--branch-full); }
.key.partial { fill: var(--branch-partial); }
.key.reject { fill: var(--branch-reject); }
.name { font-size: var(--fs-note); font-weight: 700; fill: var(--ink); }
.tick { font-size: var(--fs-note); fill: var(--muted); }
.var { font-family: var(--mono); font-size: var(--fs-detail); fill: var(--ink); }
.axis { stroke: var(--muted); stroke-width: 2; }
.curve { fill: none; stroke: var(--ink); stroke-width: 5; stroke-linejoin: round; }
</style>
