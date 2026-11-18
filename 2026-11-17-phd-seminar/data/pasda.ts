// PASDA's evaluation on the 141 pairs of the ARDiff benchmark (73 equivalent, 68 not), at
// six timeouts per pair. From Tables 4.5 to 4.7 of the thesis
// (tab:program-level-classifications-1 to -3).
export const PAIRS = 141

type Result = {
  label: string
  // Pairs each tool proves EQ or NEQ.
  proven: { PASDA: number, PRV: number, ARDiff: number, DSE: number }
  // PASDA's best-effort verdicts on the pairs it cannot prove, correct and wrong.
  maybeEq: { correct: number, wrong: number }
  maybeNeq: { correct: number, wrong: number }
}

export const results: Record<10 | 30 | 90 | 300 | 900 | 3600, Result> = {
  10: { label: '10 s', proven: { PASDA: 86, PRV: 82, ARDiff: 78, DSE: 51 }, maybeEq: { correct: 28, wrong: 10 }, maybeNeq: { correct: 4, wrong: 2 } },
  30: { label: '30 s', proven: { PASDA: 91, PRV: 87, ARDiff: 83, DSE: 51 }, maybeEq: { correct: 28, wrong: 9 }, maybeNeq: { correct: 4, wrong: 2 } },
  90: { label: '90 s', proven: { PASDA: 95, PRV: 89, ARDiff: 83, DSE: 51 }, maybeEq: { correct: 23, wrong: 8 }, maybeNeq: { correct: 5, wrong: 3 } },
  300: { label: '300 s', proven: { PASDA: 99, PRV: 93, ARDiff: 84, DSE: 51 }, maybeEq: { correct: 19, wrong: 7 }, maybeNeq: { correct: 5, wrong: 4 } },
  900: { label: '900 s', proven: { PASDA: 102, PRV: 93, ARDiff: 85, DSE: 51 }, maybeEq: { correct: 20, wrong: 7 }, maybeNeq: { correct: 5, wrong: 1 } },
  3600: { label: '1 h', proven: { PASDA: 104, PRV: 95, ARDiff: 86, DSE: 51 }, maybeEq: { correct: 19, wrong: 8 }, maybeNeq: { correct: 4, wrong: 1 } },
}

// The best-effort verdicts of a timeout, correct or not.
export const maybeCount = (r: Result) => r.maybeEq.correct + r.maybeEq.wrong + r.maybeNeq.correct + r.maybeNeq.wrong
