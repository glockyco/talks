<script setup lang="ts">
import { computed } from 'vue'

// The input space of approvedAmount: one row per branch of the code, the requested amount
// to scale along the horizontal axis, and in each cell the amount that the code approves.
// v1 caps full approvals at 60, v2 at 50. Verdicts and the failing range come from the
// tool runs on the example (.agent-build/phd-seminar/12-review-answers.md, section 9, in
// the thesis repository).
//   single:    the full approval as one lane, the behavior of v2
//   path:      v1 alone, with the path that the developer test of the full approval
//              follows marked and the other paths dimmed
//   question:  two lanes, with v1 not shown yet
//   both:      v1 and v2, with the range where they differ marked
//   pasda:     both, with a lane for PASDA's verdicts, and with `prior` PRV's above it
//   teralizer: both, each with a lane for the generalized test's sampled inputs, labeled
//              "passes on v1" and "fails on v2"
//   program:   both, veiled by the one verdict for the method as a whole: `verdict` NEQ
//              is the proof a solver would give, UNKNOWN what program-level tools report.
//              `witness` marks the input that proves a difference, the request for 55
//   blank, noproof: both, with a verdict lane that is empty or holds what a
//              partition-level tool reports
// `questions` adds two lanes above the verdicts: what the solver answers to the two
// questions of equivalence checking. It proves whether the outputs differ and cannot
// decide whether inputs reach the path (.agent-build/phd-seminar/solver-check).
const props = withDefaults(defineProps<{
  view?: 'single' | 'path' | 'question' | 'both' | 'pasda' | 'teralizer' | 'program' | 'blank' | 'noproof'
  width?: number
  tests?: boolean
  missed?: boolean
  scale?: number
  // Reads the map as a method summary: the conditions and the cells carry the tints of
  // the path condition and the output formula, with a legend above them.
  summary?: boolean
  // Name of the verdict lane, where it is not the view's own.
  laneLabel?: string
  questions?: boolean
  // Draws the two question lanes. Without it they keep their room and stay empty.
  answers?: boolean
  prior?: boolean
  // Draws the view's own verdict lane. Without it the lane keeps its room and stays empty.
  result?: boolean
  verdict?: 'UNKNOWN' | 'NEQ'
  witness?: boolean
  // Tints the conditions on p in the color of UNKNOWN: the solver cannot decide them.
  undecided?: boolean
  // 'full' draws only the full approval, for a map that continues the one above it. Its
  // condition is on that map, so the room below the name is free for the lane labels.
  only?: 'full'
  // Without the line above the rows (the legend or "approved amount").
  headless?: boolean
  // 'inline' sets the axis label between the first two ticks, where a map has no room
  // for a line of its own.
  axisLabel?: boolean | 'inline'
}>(), { view: 'single', width: 804, tests: true, missed: false, scale: 1, summary: false, questions: false, answers: true, prior: false, result: true, verdict: 'UNKNOWN', witness: false, undecided: false, headless: false, axisLabel: true })

const HEAD = 262
// Room inside the cells on both sides of the axis, so a test at a small amount is not cut.
const PAD = 22
const LANE = 62
const GAP = 16
const TOP = 46
const EXTRA = 64
const SAMPLES = 50

const PW = computed(() => props.width - HEAD - 2 * PAD - 4)
const x = (amount: number) => HEAD + PAD + amount * (PW.value / 100)
const left = (lo: number) => lo === 0 ? HEAD + 2 : x(lo) + 2
const right = (hi: number) => hi === 100 ? HEAD + PW.value + 2 * PAD - 2 : x(hi) - 2

const lanes = computed(() => props.view === 'single' || props.view === 'path' ? 1 : 2)
const known = computed(() => !['single', 'path', 'question'].includes(props.view))
const sampled = computed(() => props.view === 'teralizer')
// The program view keeps the lane's room, so that its rows line up with a map beside it.
const laned = computed(() => ['pasda', 'program', 'blank', 'noproof'].includes(props.view))

const yV1 = TOP
const yV2 = computed(() => lanes.value === 1 ? TOP : sampled.value ? TOP + LANE + SAMPLES + 12 : TOP + LANE + 6)
const yExtra = computed(() => yV2.value + LANE + 14)
const fullEnd = computed(() => laned.value
  ? yExtra.value + laneCount.value * EXTRA
  : yV2.value + LANE + (sampled.value ? SAMPLES : 0))
const yPartial = computed(() => fullEnd.value + GAP)
const yReject = computed(() => yPartial.value + LANE + GAP)
// The rows below the full approval: partial approval and rejection.
const below = computed(() => props.only !== 'full')
const yAxis = computed(() => (below.value ? yReject.value + LANE : fullEnd.value) + 10)
const H = computed(() => yAxis.value + (props.axisLabel === true ? 78 : 44))
const SKIP = computed(() => props.headless ? TOP - 8 : 0)

type Cell = { lo: number, hi: number, y: number, label: string, at: number, kind?: 'changed' | 'open' | 'path' | 'dim' }
const allCells = computed<Cell[]>(() => {
  const out: Cell[] = []
  if (props.view === 'path') return [
    { lo: 0, hi: 60, y: yV1, label: 'amount', at: 35, kind: 'path' },
    { lo: 60, hi: 100, y: yV1, label: '60', at: 80, kind: 'dim' },
    { lo: 0, hi: 100, y: yPartial.value, label: 'min(amount, 5)', at: 50, kind: 'dim' },
    { lo: 0, hi: 100, y: yReject.value, label: '0', at: 50, kind: 'dim' },
  ]
  if (props.view === 'question') out.push({ lo: 0, hi: 100, y: yV1, label: '?', at: 50, kind: 'open' })
  if (known.value) {
    out.push({ lo: 0, hi: 60, y: yV1, label: 'amount', at: 35 })
    out.push({ lo: 60, hi: 100, y: yV1, label: '60', at: 80 })
  }
  out.push({ lo: 0, hi: 50, y: yV2.value, label: 'amount', at: 35 })
  out.push({ lo: 50, hi: 100, y: yV2.value, label: '50', at: 75, kind: known.value ? 'changed' : undefined })
  out.push({ lo: 0, hi: 100, y: yPartial.value, label: 'min(amount, 5)', at: 50 })
  out.push({ lo: 0, hi: 100, y: yReject.value, label: '0', at: 50 })
  return out
})
const cells = computed(() => allCells.value.filter(c => below.value || c.y < yPartial.value))

const rows = computed(() => [
  { name: 'full approval', cond: 'p >= 0.8', cls: 'full', y: yV1, h: fullEnd.value - yV1 },
  { name: 'partial approval', cond: '0.5 <= p < 0.8', cls: 'partial', y: yPartial.value, h: LANE },
  { name: 'rejection', cond: 'p < 0.5', cls: 'reject', y: yReject.value, h: LANE },
].filter(r => below.value || r.cls === 'full'))

// Developer tests (income, debt, amount): (300, 10, 20), (60, 10, 8) and (10, 30, 1).
const dots = computed(() => {
  if (props.view === 'path') return [{ a: 20, y: yV1 }]
  const out = [{ a: 20, y: yV2.value }, { a: 8, y: yPartial.value }, { a: 1, y: yReject.value }]
  if (known.value) out.push({ a: 20, y: yV1 })
  return out.filter(d => below.value || d.y < yPartial.value)
})
// Dashed guides tie the limits of the two versions to the axis. One lane needs none.
const guides = computed(() => known.value ? [50, 60] : props.view === 'path' ? [60] : [])
const ticks = computed(() => known.value ? [0, 50, 60, 100] : props.view === 'path' ? [0, 60, 100] : [0, 50, 100])

// Illustrative sampled amounts of the generalized test, not the amounts jqwik drew. The
// property covers amounts up to 60, and v2 fails it above 50.
const samples = [4, 11, 27, 33, 40, 47, 52, 57]
const sampleLanes = computed(() => [
  { y: yV1 + LANE + SAMPLES / 2 + 2, limit: 60, result: 'passes', version: 'v1' },
  { y: yV2.value + LANE + SAMPLES / 2 + 2, limit: 50, result: 'fails', version: 'v2' },
])
// The lanes under the full approval, from top to bottom: the solver's answers to the two
// questions, then the verdicts of the tools. The other branches carry the last lane's
// verdict in their cells. One color per verdict across the deck (styles/index.css).
type Lane = { label: string, spans: { lo: number, hi: number, text: string }[], rest?: string, own?: boolean, hidden?: boolean }
const CHIP: Record<string, string> = { 'EQ': 'eq', 'NEQ': 'neq', 'MAYBE_NEQ': 'mneq', 'UNKNOWN': 'unk', 'no answer': 'unk', 'no': 'plain', 'yes': 'plain' }
const split = (l: string, r: string) => [{ lo: 0, hi: 50, text: l }, { lo: 50, hi: 100, text: r }]
const laneRows = computed<Lane[]>(() => {
  const out: Lane[] = []
  const v = props.view
  if (!['pasda', 'noproof'].includes(v)) return out
  if (v === 'pasda' && props.prior) out.push({ label: 'PRV', spans: split('EQ', 'UNKNOWN'), rest: 'EQ' })
  if (props.questions) {
    out.push({ label: 'outputs differ?', spans: split('no', 'yes'), hidden: !props.answers })
    out.push({ label: 'path reachable?', spans: [{ lo: 0, hi: 100, text: 'no answer' }], hidden: !props.answers })
  }
  if (v === 'noproof') out.push({ label: props.laneLabel!, spans: split('EQ', 'UNKNOWN'), rest: 'EQ' })
  if (v === 'pasda') out.push({ label: 'PASDA', spans: split('EQ', 'MAYBE_NEQ'), rest: 'EQ', own: props.prior, hidden: !props.result })
  return out
})
// A view without lanes of its own keeps the room of the lanes beside or before it.
const laneCount = computed(() => laned.value ? (props.questions ? 2 : 0) + 1 + (props.prior ? 1 : 0) : 0)
const laneY = (i: number) => yExtra.value + i * EXTRA + EXTRA / 2
const rest = computed(() => laneRows.value.find(l => !l.hidden && l.rest)?.rest)
const chipWidth = (t: string) => t === t.toUpperCase() ? 32 + t.length * 17 : 30 + t.length * 13
</script>

<template>
  <svg :width="width * scale" :height="(H - SKIP) * scale" :viewBox="`0 ${SKIP} ${width} ${H - SKIP}`" class="lanes" role="img"
    aria-label="Approved amount per branch of approvedAmount over the requested amount">
    <text v-if="!summary && !headless" :x="HEAD" :y="TOP - 18" class="colhead">approved amount</text>
    <template v-else-if="!headless">
      <rect x="0" :y="TOP - 44" width="212" height="36" rx="8" class="tint in" />
      <text x="14" :y="TOP - 18" class="legend">path condition</text>
      <rect :x="HEAD" :y="TOP - 44" width="470" height="36" rx="8" class="tint out" />
      <text :x="HEAD + 14" :y="TOP - 18" class="legend">symbolic output: approved amount</text>
    </template>

    <g v-for="r in rows" :key="r.name" :class="{ faint: view === 'path' && r.cls !== 'full' }">
      <rect x="0" :y="r.y + 3" width="8" :height="r.h - 6" rx="4" :class="['key', r.cls]" />
      <text x="22" :y="r.y + LANE / 2 - 2" class="name">{{ r.name }}</text>
      <template v-if="below">
        <rect v-if="summary" x="18" :y="r.y + LANE / 2 + 9" :width="14 + r.cond.length * 15.6" height="32" rx="8" class="tint in" />
        <rect v-else-if="undecided" x="16" :y="r.y + LANE / 2 + 6" :width="12 + r.cond.length * 14.4" height="30" rx="8" class="tint unk" />
        <text :x="summary ? 25 : 22" :y="r.y + LANE / 2 + (summary ? 33 : 28)" :class="['cond', { strong: summary }]">{{ r.cond }}</text>
      </template>
    </g>

    <line v-for="a in guides" :key="`under-${a}`" :x1="x(a)" :x2="x(a)" :y1="fullEnd" :y2="yAxis + 8" class="guide" />

    <g v-for="c in cells" :key="`${c.y}-${c.lo}`">
      <rect :x="left(c.lo)" :y="c.y" :width="right(c.hi) - left(c.lo)" :height="LANE" rx="10" :class="['cell', c.kind, { out: summary }]" />
      <text :x="x(c.at)" :y="c.y + LANE / 2 + 9" text-anchor="middle" :class="['value', { faint: c.kind === 'dim' }]">{{ c.label }}</text>
    </g>

    <template v-if="sampled">
      <g v-for="l in sampleLanes" :key="l.y">
        <text :x="HEAD - 16" :y="l.y + 8" text-anchor="end" class="ver"><tspan :class="l.result">{{ l.result }}</tspan> on {{ l.version }}</text>
        <line :x1="x(0)" :x2="x(60)" :y1="l.y" :y2="l.y" class="span ink" />
        <line :x1="x(60) + 12" :x2="x(100)" :y1="l.y" :y2="l.y" class="span off" />
        <line :x1="x(60)" :x2="x(60)" :y1="l.y - 12" :y2="l.y + 12" class="cap" />
        <template v-for="a in samples" :key="a">
          <circle v-if="a <= l.limit" :cx="x(a)" :cy="l.y" r="9" class="pass" />
          <path v-else :d="`M${x(a) - 8},${l.y - 8} l16,16 m0,-16 l-16,16`" class="fail" />
        </template>
      </g>
    </template>

    <line v-for="a in guides" :key="`over-${a}`" :x1="x(a)" :x2="x(a)" :y1="yV1 - 8" :y2="fullEnd" class="guide" />

    <g v-for="(l, i) in laneRows" :key="l.label" :visibility="l.hidden ? 'hidden' : 'visible'">
      <rect v-if="l.own" x="104" :y="laneY(i) - EXTRA / 2 + 4" :width="width - 104" :height="EXTRA - 8" rx="10" class="band" />
      <text :x="HEAD - 16" :y="laneY(i) + 8" text-anchor="end" :class="['ver', { own: l.own }]">{{ l.label }}</text>
      <line v-for="v in l.spans" :key="v.lo" :x1="x(v.lo) + 2" :x2="x(v.hi) - 2" :y1="laneY(i)" :y2="laneY(i)" :class="['span', CHIP[v.text]]" />
      <g v-for="v in l.spans" :key="`chip-${v.lo}`" :transform="`translate(${x((v.lo + v.hi) / 2)}, ${laneY(i)})`">
        <rect :x="-chipWidth(v.text) / 2" y="-22" :width="chipWidth(v.text)" height="44" rx="8" :class="['chip', CHIP[v.text]]" />
        <text y="9" text-anchor="middle" :class="['chiptext', CHIP[v.text]]">{{ v.text }}</text>
      </g>
    </g>
    <template v-if="rest">
      <g v-for="y in [yPartial, yReject]" :key="y" :transform="`translate(${x(91)}, ${y + LANE / 2})`">
        <rect :x="-chipWidth(rest) / 2" y="-22" :width="chipWidth(rest)" height="44" rx="8" :class="['chip', CHIP[rest]]" />
        <text y="9" text-anchor="middle" :class="['chiptext', CHIP[rest]]">{{ rest }}</text>
      </g>
    </template>

    <template v-if="view === 'program'">
      <rect :x="HEAD - 4" :y="yV1 - 6" :width="PW + 2 * PAD + 8" :height="yReject + LANE - yV1 + 12" rx="12" class="veil" />
      <text v-if="laneLabel" :x="HEAD - 16" :y="yExtra + laneCount * EXTRA / 2 + 8" text-anchor="end" class="ver">{{ laneLabel }}</text>
      <template v-if="witness">
        <rect v-for="y in [yV1, yV2]" :key="y" :x="x(55) - 12" :y="y + LANE / 2 - 12" width="24" height="24" class="missed" />
      </template>
      <g :transform="`translate(${x(50)}, ${yExtra + laneCount * EXTRA / 2})`">
        <rect :x="verdict === 'NEQ' ? -64 : -104" y="-30" :width="verdict === 'NEQ' ? 128 : 208" height="60" rx="10" :class="['chip', CHIP[verdict]]" />
        <text y="11" text-anchor="middle" :class="['chiptext', 'big', CHIP[verdict]]">{{ verdict }}</text>
      </g>
    </template>

    <template v-if="lanes === 2">
      <text :x="HEAD + 18" :y="yV1 + LANE / 2 + 8" class="ver">v1</text>
      <text :x="HEAD + 18" :y="yV2 + LANE / 2 + 8" class="ver">v2</text>
      <template v-if="summary && below">
        <text :x="HEAD + 18" :y="yPartial + LANE / 2 + 8" class="ver">v1, v2</text>
        <text :x="HEAD + 18" :y="yReject + LANE / 2 + 8" class="ver">v1, v2</text>
      </template>
    </template>

    <template v-if="props.tests">
      <circle v-for="d in dots" :key="`${d.a}-${d.y}`" :cx="x(d.a)" :cy="d.y + LANE / 2" r="11" class="test" />
    </template>
    <rect v-if="missed" :x="x(55) - 12" :y="yV2 + LANE / 2 - 12" width="24" height="24" class="missed" />

    <line :x1="x(0)" :x2="x(100)" :y1="yAxis" :y2="yAxis" class="axis" />
    <text v-for="a in ticks" :key="a" :x="x(a)" :y="yAxis + 34" text-anchor="middle" class="tick">{{ a }}</text>
    <text v-if="axisLabel === true" :x="x(50)" :y="yAxis + 68" text-anchor="middle" class="tick">requested amount</text>
    <text v-else-if="axisLabel === 'inline'" :x="x(ticks[1] / 2)" :y="yAxis + 34" text-anchor="middle" class="tick">requested amount</text>
  </svg>
</template>

<style scoped>
.lanes { display: block; font-family: var(--sans); overflow: visible; flex: none; }
.colhead, .tick { font-size: var(--fs-note); fill: var(--muted); }
.key.full { fill: var(--branch-full); }
.key.partial { fill: var(--branch-partial); }
.key.reject { fill: var(--branch-reject); }
.name { font-size: var(--fs-small); font-weight: 700; fill: var(--ink); }
.cond { font-family: var(--mono); font-variant-ligatures: none; font-size: var(--fs-detail); fill: var(--muted); }
.ver { font-size: var(--fs-note); font-weight: 700; fill: var(--muted); }
.ver.own { fill: var(--ink); }
/* The lane that the thesis adds. */
.band { fill: var(--aau-light); opacity: 0.16; }
.ver .passes { fill: var(--pass); }
.ver .fails { fill: var(--fail); }
.cell { fill: #fff; stroke: var(--rule); stroke-width: 2; }
.cell.out { fill: var(--spec-out); stroke: #a9cf95; }
.cell.changed { fill: var(--change-fill); stroke: var(--change); }
.cell.out.changed { fill: var(--spec-out); stroke: var(--change); stroke-width: 4; }
.tint.in { fill: var(--spec-in); }
.tint.out { fill: var(--spec-out); }
.tint.unk { fill: var(--unknown); }
.legend { font-size: var(--fs-note); fill: var(--ink); }
.cond.strong { font-size: var(--fs-note); fill: var(--ink); }
.cell.path, .cell.out.path { stroke: var(--ink); stroke-width: 4; }
.cell.dim { opacity: 0.45; }
.faint { opacity: 0.45; }
.cell.open { fill: none; stroke: var(--muted); stroke-dasharray: 8 8; }
.value { font-family: var(--mono); font-variant-ligatures: none; font-size: var(--fs-note); fill: var(--ink); }
.span { stroke-width: 6; stroke-linecap: round; }
.span.eq { stroke: var(--eq); }
.span.mneq { stroke: var(--maybe-neq); }
.span.unk { stroke: var(--unknown); }
.span.plain { stroke: var(--ink); stroke-width: 3; }
.span.ink { stroke: var(--ink); stroke-width: 4; }
.span.off { stroke: var(--muted); stroke-width: 4; stroke-dasharray: 2 12; }
.cap { stroke: var(--ink); stroke-width: 5; stroke-linecap: round; }
.chip.eq { fill: var(--eq); }
.chip.neq { fill: var(--neq); }
.chip.mneq { fill: var(--maybe-neq); }
.chip.unk { fill: var(--unknown); }
.chip.plain { fill: #fff; stroke: var(--ink); stroke-width: 2.5; }
.chiptext { font-size: var(--fs-label); font-weight: 700; fill: #fff; }
.chiptext.unk, .chiptext.plain { fill: var(--chip-ink); }
.chiptext.plain { font-weight: 400; font-size: var(--fs-detail); }
.chiptext.big { font-size: var(--fs-small); }
.veil { fill: var(--panel); opacity: 0.62; }
.pass { fill: #fff; stroke: var(--ink); stroke-width: 3; }
.fail { stroke: var(--fail); stroke-width: 5; stroke-linecap: round; fill: none; }
.test { fill: var(--ink); stroke: #fff; stroke-width: 3; }
.missed { fill: none; stroke: var(--ink); stroke-width: 4; }
.guide { stroke: var(--muted); stroke-width: 1.5; stroke-dasharray: 5 6; }
.axis { stroke: var(--muted); stroke-width: 2; }
</style>
