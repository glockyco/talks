<script setup lang="ts">
import { computed } from 'vue'

// What PASDA reports for the 141 ARDiff benchmark pairs at one timeout: its proofs, the
// pairs it cannot prove by best-effort verdict and correctness, and the proofs of the
// other three tools. From Tables 4.5 to 4.7 of the thesis
// (tab:program-level-classifications-1 to -3). "No verdict" counts UNKNOWN plus
// depth-limit, timeout and error results.
const props = withDefaults(defineProps<{ timeout?: 10 | 30 | 90 | 300 | 900 | 3600 }>(), { timeout: 3600 })

const TOTAL = 141
// Per timeout: pairs proven by PASDA, PRV, ARDiff and DSE, then PASDA's MAYBE_EQ correct
// and wrong, and its MAYBE_NEQ correct and wrong.
const table: Record<number, number[]> = {
  10: [86, 82, 78, 51, 28, 10, 4, 2],
  30: [91, 87, 83, 51, 28, 9, 4, 2],
  90: [95, 89, 83, 51, 23, 8, 5, 3],
  300: [99, 93, 84, 51, 19, 7, 5, 4],
  900: [102, 93, 85, 51, 20, 7, 5, 1],
  3600: [104, 95, 86, 51, 19, 8, 4, 1],
}
const row = computed(() => table[props.timeout])
const proven = computed(() => row.value[0])
const open = computed(() => TOTAL - proven.value)
const others = computed(() => ['PRV', 'ARDiff', 'DSE'].map((tool, i) => ({ tool, proven: row.value[i + 1] })))
const parts = computed(() => {
  const [, , , , meq, meqWrong, mneq, mneqWrong] = row.value
  return [
    { n: meq, cls: 'meq' },
    { n: meqWrong, cls: 'meq wrong' },
    { n: mneq, cls: 'mneq' },
    { n: mneqWrong, cls: 'mneq wrong' },
    { n: open.value - meq - meqWrong - mneq - mneqWrong, cls: 'none' },
  ]
})
const pct = (n: number, of: number) => `${(100 * n) / of}%`
</script>

<template>
  <div class="zoom">
    <div class="row main">
      <div class="tool">PASDA</div>
      <div class="bar top">
        <div class="proven" :style="{ width: pct(proven, TOTAL) }">{{ proven }} proven</div>
        <div class="open focus" :style="{ width: pct(open, TOTAL) }">{{ open }} not proven</div>
      </div>
    </div>
    <div class="row">
      <div />
      <svg class="funnel" viewBox="0 0 141 60" preserveAspectRatio="none" aria-hidden="true">
        <polygon :points="`${proven},0 141,0 141,60 0,60`" />
      </svg>
    </div>
    <div class="row detail">
      <div class="tool">of these {{ open }}</div>
      <div class="bar tall">
        <div v-for="p in parts" :key="p.cls" :class="p.cls" :style="{ width: pct(p.n, open) }">{{ p.n }}</div>
      </div>
    </div>
    <div class="legend">
      <span><i class="meq" />MAYBE_EQ, correct</span>
      <span><i class="mneq" />MAYBE_NEQ, correct</span>
      <span><i class="meq wrong" /><i class="mneq wrong" />wrong</span>
      <span><i class="none" />no verdict</span>
    </div>
    <div class="rows">
      <div v-for="t in others" :key="t.tool" class="row">
        <div class="tool">{{ t.tool }}</div>
        <div class="bar">
          <div class="proven" :style="{ width: pct(t.proven, TOTAL) }">{{ t.proven }} proven</div>
          <div class="open" :style="{ width: pct(TOTAL - t.proven, TOTAL) }">{{ TOTAL - t.proven }} not proven</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.zoom { width: 100%; }
.rows { display: flex; flex-direction: column; gap: 12px; margin-top: 28px; }
.row { display: grid; grid-template-columns: 216px 1fr; column-gap: 24px; align-items: center; font-size: var(--fs-body); }
.row.main { font-weight: 700; }
.bar { display: flex; height: 52px; border-radius: 8px; overflow: hidden; font-size: var(--fs-small); font-weight: 700; font-variant-numeric: tabular-nums; }
.bar.tall { height: 72px; border-radius: 0 0 8px 8px; }
/* The connector attaches to square corners, so no gap shows between the bars. */
.bar.top { border-radius: 8px 8px 0 8px; }
.bar > div { display: flex; align-items: center; justify-content: center; white-space: nowrap; }
.proven { background: var(--eq); color: #fff; }
.open { background: var(--unknown); color: #111; }
.open.focus { background: var(--maybe); }
.funnel { display: block; width: 100%; height: 60px; }
.funnel polygon { fill: #f3dc8c; }
.meq { background: var(--maybe); color: #111; }
.mneq { background: var(--maybe-neq); color: #fff; }
.wrong { color: #111; }
.wrong { background-image: repeating-linear-gradient(135deg, rgba(255, 255, 255, 0.7) 0 9px, transparent 9px 14px); }
.none { background: var(--unknown); color: #111; }
.legend { display: flex; justify-content: flex-end; gap: 32px; margin-top: 16px; font-size: var(--fs-small); color: var(--muted); }
.legend i { display: inline-block; width: 22px; height: 22px; border-radius: 4px; margin-right: 8px; vertical-align: -4px; }
</style>
