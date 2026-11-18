# AGENTS.md

Slide decks of talks, one folder per talk. The repository is public, so material that must stay private until its event, or that belongs to a partner, does not go here.

## Layout

- A talk's folder is named by its day and a short name, such as `2026-11-17-phd-seminar`. The website uses the same name as the talk's address, and the talk's tag carries it too.
- A folder holds everything its deck needs: `slides.md`, components, layouts, styles, pictures, and its own `package.json` and lockfile. Start a new talk as a copy of the folder it builds on, because a given talk then keeps building as it did, whatever a later deck changes or upgrades.
- The rules below hold for every talk. A folder's `AGENTS.md` holds its commands and the rules of its own content.

## Slides

- Keep the message under a slide's title to one concrete fact or reason, and the text of a panel to three lines, because the audience should listen and look, not read. Panel text wraps into lines of even length. Reword a text whose last line holds one or two words.
- Let the message say what the slide means for the talk's question, not how a tool works.
- State what is on the slide. Do not let a tool "say", "know" or "see" something, do not build a contrast into a sentence ("while ... only", "yet"), do not join two halves with "and ... also", do not list three things for rhythm, and give a count where one exists, because such sentences read as machine-written.
- Give one thing one word and one mark on every slide, and write pairs in the same form ("proven" and "not proven"), because a listener takes a second word for a second thing. Before showing a new slide, compare its terms, marks and capitalization with the settled slides.
- Start a label inside a picture in lowercase (axis, lane, legend, box, caption), and keep the spelling of names. Messages and panel text are sentences with a period, and labels have none.
- Write ranges with "to" ("51 to 60"), units with a space ("1 h") and percent without. Set concepts in the text font and code identifiers and values in the code font.
- Take every size and color from the variables in the folder's `styles/index.css`, because one type scale across all slides keeps them consistent and lets one change reach every slide. Only the layouts and single display sizes, such as a large number, set their own.
- Use the fonts the deck bundles. A system font differs between machines and shifts the layout.
- Trace every number and claim on a slide to the thesis or paper it comes from, or to a recorded run, and name the source in a comment before the slide's content. Slidev reads a comment at the end of a slide as its speaker note, and the decks have no speaker notes. Put the scripts and outputs of a run into the folder's `evidence/`, because a source only on one machine cannot be checked.
- Check a claim about a tool by running the tool or reading its source.

## Working on a deck

- Try options for a slide in a file named `*-drafts.md` with the deck's headmatter, and delete the file once the chosen option is in the deck, because two copies of a slide drift apart.
- Before showing a changed slide, render every build step with `pnpm png`, have an agent that did not build the slide audit the PNGs against the full flaw taxonomy of [SlideAudit](https://pmc.ncbi.nlm.nih.gov/articles/PMC13227769/) (Figure 2), then look at them yourself. The builder of a slide misses defects in its own renders.
- After a change that should not show, compare every build step with the renders from before it, pixel by pixel.
- Edit the Markdown and the components directly. The dev server's MCP endpoint stays off (`mcp: false` in the headmatter).

## After a talk

- Export the PDF for the website with `pnpm pdf:web`, tag the commit it comes from with the folder's name, and add the talk to the table in `README.md`. The tag keeps what was shown, so the folder can be corrected and cleaned up afterwards.

## Commits

Follow `skill://commit-policy`.
