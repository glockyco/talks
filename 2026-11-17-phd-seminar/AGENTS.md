# PhD seminar, 17 November 2026

The 20-minute talk about my PhD thesis topic for the SCCH PhD seminar, as a Slidev deck. `../AGENTS.md` holds the rules for every talk.

## Files

- `slides.md` holds the headmatter, the title slide and About This Talk, and imports `main.md` (second title slide to Papers) and `backup.md` (the backup slides). `slides-web.md` imports `main.md` alone for the website's PDF.
- `talk.ts` holds what identifies the talk: title, speaker, event, day, the parts of the section bar and the research question. The headmatter of `slides.md` and `slides-web.md` repeats the title, because it cannot import it.
- `data/` holds result data that several components draw, and `evidence/` the runs behind claims on the slides.

## Commands

```bash
pnpm install   # once per clone
pnpm dev       # live preview and presenter view on http://localhost:3030
pnpm png       # one PNG per slide and build step in out/slides/
pnpm shots     # after pnpm png: refresh the key-slide images of the Questions slide
pnpm pdf       # out/slides.pdf, the backup for presenting, one page per build step
pnpm pdf:web   # out/slides-web.pdf, the PDF for the website: main.md alone
```

## Rules

- Build slides in the frame `layouts/bars.vue`. Give each slide `title`, `section` and `message` in its frontmatter. The message stands under the title, and `messageAt` holds it back until that click. `sources` adds one line of citations above the footer bar: authors and year, grouped by what they support, all from the thesis bibliography.
- The title slide uses `layouts/cover.vue`, which has the frame's fonts and logos and no bars. The deck shows it before the talk starts and again after About This Talk, where the talk begins.
- A `section` that `talk.ts` does not list marks nothing in the section bar. About This Talk has `section: Before the talk`, because the talk starts after it, and backup slides come after Questions with `section: Backup`.
- Show `components/Overview.vue` before each part with that part as `active`, because the audience needs a pause and a signal when the topic changes.
- Show Java with the `JavaCode` component, not with Markdown code blocks, because slides mark single tokens and hold marks back until a click.
- Use the shared classes of `styles/index.css` before writing a slide's own style: `card` (with `compact` and `fill`), `card-head` (with `cited` and `cite`), `group-head`, `chip` (with `small` and `medium`), `key`, `fact`, `setup`, and `code` with `in` or `out`. Panel heads are set in capitals: wrap a version, unit or name in `<span class="keep">` so that it keeps its case.
- Name the branches of the loan example "full approval", "partial approval" and "rejection", and its versions v1 and v2, in code, plots, maps and text alike.
- Say "symbolic analysis" for the technique, "path condition" and "symbolic output" for the two parts of a method summary, and "generalized test" for what Teralizer produces.
- Write verdicts as EQ, NEQ, MAYBE_EQ, MAYBE_NEQ and UNKNOWN, in the colors that `styles/index.css` defines for them. Orange also marks where v2 differs from v1.
- Before the PASDA part, show one verdict for the method as a whole. Verdicts per path belong to the PASDA part, which introduces the partition level, and the two questions to the solver appear only on the Best-Effort Classification slide.
- Name a role in the process picture, not a product ("solver", "PBT"), and name the product (Z3, jqwik) where a slide shows its output or code.
- Name the baselines PRV, ARDiff and DSE on every result comparison, because the comparison is the evidence.
- Take code examples from the running example or the Java standard library.
- The Questions slide shows renders of the slides with `shot: <name>` in their frontmatter, from `public/shots/`. Run `pnpm shots` after changing one of them. A missing image makes the export draw an error overlay over every slide, which shows as dark renders.
- Ask before changing the frame, the type scale, the loan map or the result bars, because they were chosen in review.
