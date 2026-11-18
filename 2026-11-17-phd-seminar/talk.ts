// What identifies the talk. The title slide, the frame's section bar and footer, the overview
// and the summary read it from here. The headmatter of slides.md and slides-web.md cannot
// import it, so their `title` has to be changed by hand.
export const talk = {
  titleLines: ['Formal Guarantees Meet', 'Practical Constraints'],
  subtitleLines: ['From Semantic Differencing to Test Generalization', 'for Regression Detection'],
  speaker: 'Johann Glock',
  supervisors: ['Prof. Martin Pinzger', 'Prof. Johann Eder'],
  event: 'SCCH PhD Seminar',
  date: '17 November 2026',
  day: '2026-11-17',
  // The parts in the section bar. A slide marks its part with `section` in its frontmatter.
  sections: ['Introduction', 'Background', 'PASDA', 'Teralizer', 'Conclusion'],
  // The research question, broken where the overview breaks it.
  questionLines: ['How can symbolic analysis support regression detection', 'without a complete proof?'],
}
