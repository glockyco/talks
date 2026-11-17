# PhD seminar, 17 November 2026

The 20-minute talk about my PhD thesis topic for the SCCH PhD seminar, as a Slidev deck.
`slides.md` is the deck, and `../AGENTS.md` holds the rules for the repository.

## Commands

```bash
pnpm install   # once per clone
pnpm dev       # live preview and presenter view on http://localhost:3030
pnpm png       # one PNG per slide and build step in out/slides/
pnpm shots     # after pnpm png: refresh the key-slide images of the Questions slide
pnpm pdf       # out/slides.pdf, the backup for presenting, one page per build step
pnpm pdf:web   # out/slides-web.pdf, the PDF for the website: from the title slide to Papers
```

## Rules

- Build slides in the frame `layouts/bars.vue`. Give each slide `title`, `section` and
  `message` in its frontmatter. The message is the slide's one statement and stands
  under the title. `messageAt` holds it back until that click. `sources` adds one line
  of citations above the footer bar: authors and year, grouped by what they support,
  all from the thesis bibliography.
- The title slide uses `layouts/cover.vue`, which has the frame's fonts and logos and no
  bars, and reads its text from `talk.ts`. The deck shows it before the talk starts and
  again after About This Talk, where the talk begins. Give the second copy a `title`,
  because `scripts/shots.mjs` counts slides by their `title` lines.
- A `section` that the bar does not list marks nothing in the bar. Give About This Talk
  `section: Before the talk`, because the talk starts after it, and put backup slides
  after Questions with `section: Backup`.
- Show `components/Overview.vue` before each part with that part as `active`, because
  the audience needs a pause and a signal when the topic changes.
- Try options for a slide in a file named `*-drafts.md` with the deck's headmatter, and
  delete the file once the chosen option is in `slides.md`, because two copies of a
  slide drift apart.
- Use only the size and color variables of `.frame` in `styles/index.css`, because one
  type scale across all slides is what keeps them consistent.
- Keep the text of a panel to three lines, and the message to one concrete fact or
  reason, because the audience should listen and look, not read. Panel text wraps into
  lines of even length. Reword a text whose last line holds one or two words.
- State what is on the slide. Do not let a tool "say", "know" or "see" something, do not
  build a contrast into a sentence ("while ... only", "yet"), do not join two halves
  with "and ... also", do not list three things for rhythm, and give a count where one
  exists, because such sentences read as machine-written.
- Let the message say what the slide means for regression detection, not how a tool
  works: "detects the regression that the developer test misses", not "fails for
  amounts from 51 to 60".
- Show Java with the `JavaCode` component, not with Markdown code blocks, because slides
  mark single tokens and hold marks back until a click.
- Use the fonts the deck bundles (Inter and JetBrains Mono). A system font differs
  between machines and shifts the layout.
- Name the branches of the loan example "full approval", "partial approval" and
  "rejection", and its versions v1 and v2, in code, plots, maps and text alike.
- Say "symbolic analysis" for the technique, "path condition" and "symbolic output" for
  the two parts of a method summary, and "generalized test" for what Teralizer produces.
- Write verdicts as EQ, NEQ, MAYBE_EQ, MAYBE_NEQ and UNKNOWN, in the colors that
  `styles/index.css` defines for them. Orange also marks where v2 differs from v1.
- Before the PASDA part, show one verdict for the method as a whole. Verdicts per path
  belong to the PASDA part, which introduces the partition level, and the two questions
  to the solver appear only on the Best-Effort Classification slide.
- Name a role in the process picture, not a product ("solver", "PBT"), and name the
  product (Z3, jqwik) where a slide shows its output or code.
- Start a label inside a picture in lowercase (axis, lane, legend, box, caption), and
  keep the spelling of names and verdicts. Panel heads are set in capitals by
  `.card-head`: wrap a version, unit or name in `<span class="keep">` so that it keeps
  its case. Messages and panel text are sentences with a period, and labels have none.
- Give one thing one word and one mark on every slide, and write pairs in the same form
  ("proven" and "not proven"), because a listener takes a second word for a second
  thing. Before showing a new slide, compare its terms, marks and capitalization with
  the settled slides.
- Write ranges with "to" ("51 to 60"), units with a space ("1 h") and percent without.
  Set concepts in the text font and code identifiers and values in the code font.
- Trace every number and claim on a slide to the thesis tables or macros, or to a
  recorded run, and name the source in a comment beside the data. Put the comment
  before the slide's content, because Slidev reads a comment at the end of a slide as
  its speaker note, and the decks have no speaker notes.
  Check a claim about a tool by running the tool or reading its source. Take code
  examples from the running example or the Java standard library.
- Name the baselines PRV, ARDiff and DSE on every result comparison, because the
  comparison is the evidence.
- The Questions slide shows renders of four key slides from `public/shots/`. Run
  `pnpm shots` after changing one of them. A missing image makes the export draw an
  error overlay over every slide, which shows as dark renders.
- Before showing a changed slide, render every build step with `pnpm png`, have an agent
  that did not build the slide audit the PNGs against the full flaw taxonomy of
  [SlideAudit](https://pmc.ncbi.nlm.nih.gov/articles/PMC13227769/) (Figure 2), then
  look at them yourself. The builder of a slide misses defects in its own renders.
- Edit the Markdown and the components directly. The dev server's MCP endpoint stays off
  (`mcp: false` in the headmatter).
- Ask before changing the frame, the type scale, the loan map or the result bars,
  because they were chosen in review.
