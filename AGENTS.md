# AGENTS.md

Slide decks of talks, one folder per talk. The repository is public, so material that must stay private until its event, or that belongs to a partner, does not go here.

## Layout

- A talk's folder is named by its day and a short name, such as `2026-11-17-phd-seminar`. The website uses the same name as the talk's address, and the talk's tag carries it too.
- A folder holds everything its deck needs: `slides.md`, components, layouts, styles, pictures, and its own `package.json` and lockfile. Start a new talk as a copy of the folder it builds on, because a given talk then keeps building as it did, whatever a later deck changes or upgrades.
- A folder's `AGENTS.md` holds the commands and rules of that deck.

## After a talk

- Change a given talk's folder only to correct errors, because it records what was shown.
- Export the PDF for the website with `pnpm pdf:web`, tag the commit it comes from with the folder's name, and add the talk to the table in `README.md`.

## Commits

Follow `skill://commit-policy`.
