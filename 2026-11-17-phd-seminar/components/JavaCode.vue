<script setup lang="ts">
import { computed } from 'vue'

// Java source with line numbers and syntax colors. The deck highlights it itself instead
// of using Markdown code blocks, because slides mark single tokens, color the line numbers
// of the branches and hold marks back until a click.
//   marks:  "line:text" entries, the token that a change touches
//   keys:   line number to a branch color (full, partial, reject), shown beside the number
//   numbers: the line numbers to show, for an excerpt
//   tints:  line number to a background (in, out), for the two specifications of a property
//   focus:  lines to lift from the panel while the speaker explains them. The other lines
//           dim, because white on the light panel alone is hard to see on a projector
const props = withDefaults(defineProps<{
  code: string
  marks?: string[]
  marked?: boolean
  keys?: Record<number, string>
  numbers?: number[]
  tints?: Record<number, string>
  focus?: number[]
  // Without line numbers, for a single line inside a panel.
  bare?: boolean
}>(), { marks: () => [], marked: true, keys: () => ({}), numbers: () => [], tints: () => ({}), focus: () => [], bare: false })

const TOKEN = /(\/\/.*$)|(@\w+)|\b(final|int|double|long|boolean|byte|void|if|else|while|return|static|throws|new)\b|\b(\d+(?:\.\d+)?)\b|\b([A-Za-z_]\w*)(?=\()|\b([A-Z][A-Z_]{2,})\b/g
const KIND = ['', 'comment', 'anno', 'kw', 'num', 'call', 'const']

type Piece = { text: string, kind: string, mark: boolean }
function tokens(text: string, mark: boolean): Piece[] {
  const out: Piece[] = []
  let last = 0
  for (const m of text.matchAll(TOKEN)) {
    if (m.index! > last) out.push({ text: text.slice(last, m.index), kind: '', mark })
    out.push({ text: m[0], kind: KIND[m.findIndex((g, i) => i > 0 && g !== undefined)], mark })
    last = m.index! + m[0].length
  }
  if (last < text.length) out.push({ text: text.slice(last), kind: '', mark })
  return out
}

const lines = computed(() => props.code.split('\n').map((text, i) => {
  const n = props.numbers[i] ?? i + 1
  const mark = props.marks.map(m => m.split(/:(.*)/s)).find(([line]) => Number(line) === n)?.[1]
  const at = mark ? text.lastIndexOf(mark) : -1
  const pieces = at < 0
    ? tokens(text, false)
    : [...tokens(text.slice(0, at), false), ...tokens(mark!, true), ...tokens(text.slice(at + mark!.length), false)]
  return { n, pieces, blank: text.trim() === '' }
}))
</script>

<template>
  <div class="java" :class="{ lifting: focus.length > 0 }">
    <div v-for="l in lines" :key="l.n" class="line" :class="[tints[l.n], { focus: focus.includes(l.n) }]">
      <span v-if="!bare" class="no" :class="keys[l.n]">{{ l.n }}</span>
      <span class="text"><template v-for="(p, i) in l.pieces" :key="i"><mark v-if="p.mark" :class="[p.kind, { plain: !marked }]">{{ p.text }}</mark><span v-else :class="p.kind">{{ p.text }}</span></template><template v-if="l.blank">&nbsp;</template></span>
    </div>
  </div>
</template>

<style scoped>
.java { font-family: var(--mono); font-variant-ligatures: none; font-size: var(--fs-code, 24px); line-height: 1.5; color: var(--ink); }
.line { display: flex; align-items: baseline; margin: 0 -12px; padding: 0 12px; border-radius: 6px; }
.line.focus { background: #fff; }
.lifting .line:not(.focus) { opacity: 0.4; }
.line.in { background: var(--spec-in); }
.line.out { background: var(--spec-out); }
.no { flex: none; width: 2.2em; margin-right: 0.9em; padding-right: 0.5em; text-align: right; font-size: 0.8em; color: var(--muted); border-right: 4px solid transparent; user-select: none; }
.no.full { border-right-color: var(--branch-full); }
.no.partial { border-right-color: var(--branch-partial); }
.no.reject { border-right-color: var(--branch-reject); }
.text { white-space: pre; }
.kw { color: #6b4bb0; }
.num { color: #b4530f; }
.call { color: #0b6e8e; }
.anno { color: #6b4bb0; font-weight: 700; }
.const { color: #b4530f; }
.comment { color: var(--muted); font-style: italic; }
mark { background: #fbe3cf; box-shadow: 0 0 0 2px #e2711d; border-radius: 4px; }
mark.plain { background: none; box-shadow: none; }
</style>
