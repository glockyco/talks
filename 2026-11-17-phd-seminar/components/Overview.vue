<script setup lang="ts">
// The talk's overview: the research question, and one panel per part with a before-and-
// after picture in the deck's marks. The deck shows it before each part, so that the
// audience gets a pause and knows that a new part starts.
//   active: 0 shows all three parts alike, 1 to 3 marks the part that starts and dims
//           the other two
// A part's head is the keyword of the talk's title, with the tool's name beside it.
const props = withDefaults(defineProps<{ active?: number }>(), { active: 0 })
// The line under each picture.
const texts = [
  'Use the partial results of an incomplete proof',
  'Use the analysis to strengthen existing tests',
  'Summary of the results, and what to improve next',
]
const state = (part: number) => ({ dim: props.active !== 0 && props.active !== part, on: props.active === part })
</script>

<template>
  <div class="over">
    <div class="ask">How can symbolic analysis support regression detection<br>without a complete proof?</div>
    <div class="parts">
      <div class="card part" :class="state(1)">
        <PartHead :no="1" name="PASDA" keyword="Semantic Differencing" />
        <svg width="480" height="152" viewBox="0 0 480 152">
          <text x="0" y="18" class="cap">existing equivalence checking</text>
          <rect x="0" y="28" width="72" height="40" rx="6" class="eq" /><text x="36" y="55" class="in light">EQ</text><rect x="76" y="28" width="74" height="40" rx="6" class="neq" /><text x="113" y="55" class="in light">NEQ</text>
          <rect x="154" y="28" width="326" height="40" rx="6" class="unk" /><text x="317" y="55" class="in">UNKNOWN</text>
          <text x="0" y="102" class="cap">PASDA</text>
          <rect x="0" y="112" width="72" height="40" rx="6" class="eq" /><text x="36" y="139" class="in light">EQ</text><rect x="76" y="112" width="74" height="40" rx="6" class="neq" /><text x="113" y="139" class="in light">NEQ</text>
          <rect x="154" y="112" width="140" height="40" rx="6" class="meq" /><text x="224" y="139" class="in">MAYBE_EQ</text>
          <rect x="298" y="112" width="152" height="40" rx="6" class="mneq" /><text x="374" y="139" class="in light">MAYBE_NEQ</text>
          <rect x="454" y="112" width="26" height="40" rx="6" class="unk" />
        </svg>
        <p>{{ texts[0] }}</p>
      </div>
      <div class="card part" :class="state(2)">
        <PartHead :no="2" name="Teralizer" keyword="Test Generalization" />
        <svg width="480" height="152" viewBox="0 0 480 152">
          <text x="0" y="18" class="cap">developer test: one input</text>
          <line x1="4" x2="476" y1="48" y2="48" class="off" /><circle cx="96" cy="48" r="11" class="test" />
          <text x="0" y="102" class="cap">generalized test: sampled inputs, <tspan class="x">&#10005;</tspan> fails</text>
          <line x1="4" x2="288" y1="132" y2="132" class="axis" /><line x1="302" x2="476" y1="132" y2="132" class="off" />
          <line x1="288" x2="288" y1="120" y2="144" class="cap-line" />
          <circle v-for="a in [20, 53, 130, 158, 192, 226]" :key="a" :cx="a" cy="132" r="9" class="pass" />
          <path v-for="a in [250, 272]" :key="a" :d="`M${a - 8},124 l16,16 m0,-16 l-16,16`" class="fail" />
        </svg>
        <p>{{ texts[1] }}</p>
      </div>
      <div class="card part" :class="state(3)">
        <PartHead :no="3" name="Conclusion" />
        <svg width="480" height="152" viewBox="0 0 480 152">
          <rect x="0" y="8" width="200" height="136" rx="12" class="has" /><text x="100" y="70" class="step">symbolic</text><text x="100" y="98" class="step">analysis</text>
          <line x1="204" x2="286" y1="37" y2="37" class="flow" /><path d="M286,30 L298,37 L286,44 z" class="tipm" />
          <line x1="204" x2="286" y1="115" y2="115" class="flow" /><path d="M286,108 L298,115 L286,122 z" class="tipm" />
          <rect x="302" y="10" width="178" height="54" rx="10" class="dark" /><text x="391" y="45" class="step light">PASDA</text>
          <rect x="302" y="88" width="178" height="54" rx="10" class="dark" /><text x="391" y="123" class="step light">Teralizer</text>
        </svg>
        <p>{{ texts[2] }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.over { width: 100%; display: flex; flex-direction: column; gap: 28px; }
.ask { padding: 34px 40px 38px; border-radius: 16px; background: var(--aau-dark); color: #fff; font-size: var(--fs-lead); line-height: 1.35; font-weight: 700; text-align: center; }
.parts { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; }
.part { display: flex; flex-direction: column; gap: 20px; padding-top: 26px; padding-bottom: 28px; }
.part.dim { opacity: 0.35; }
.part.on { box-shadow: inset 0 0 0 4px var(--aau-dark); }
.part p { margin: 0; font-size: var(--fs-small); line-height: 1.3; text-wrap: balance; }
.part svg { display: block; overflow: visible; }
.part svg .cap { font-size: 22px; fill: var(--muted); }
.part svg .cap .x { fill: #c2410c; font-weight: 700; }
.part svg .in { font-size: 20px; font-weight: 700; fill: #111; text-anchor: middle; }
.part svg .in.light { fill: #fff; }
.part svg .eq { fill: var(--eq); }
.part svg .neq { fill: var(--neq); }
.part svg .unk { fill: var(--unknown); }
.part svg .meq { fill: var(--maybe); }
.part svg .mneq { fill: var(--maybe-neq); }
.part svg .axis { stroke: var(--ink); stroke-width: 4; stroke-linecap: round; }
.part svg .off { stroke: var(--muted); stroke-width: 4; stroke-dasharray: 2 12; stroke-linecap: round; }
.part svg .cap-line { stroke: var(--ink); stroke-width: 5; stroke-linecap: round; }
.part svg .test { fill: var(--ink); }
.part svg .pass { fill: #fff; stroke: var(--ink); stroke-width: 3; }
.part svg .fail { fill: none; stroke: #c2410c; stroke-width: 5; stroke-linecap: round; }
.part svg .has { fill: #fff; stroke: var(--ink); stroke-width: 2.5; }
.part svg .step { font-size: 24px; font-weight: 700; fill: var(--ink); text-anchor: middle; }
.part svg .step.light { fill: #fff; }
.part svg .dark { fill: var(--aau-dark); }
.part svg .flow { stroke: var(--muted); stroke-width: 4; }
.part svg .tipm { fill: var(--muted); }
</style>
