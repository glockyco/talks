// Copies the last build step of each slide with `shot: <name>` in its frontmatter from
// out/slides/ (written by `pnpm png`) to public/shots/<name>.png, where the Questions slide
// shows them. Slidev's own parser numbers the slides, with the files that slides.md imports,
// in the order of the export.
import { copyFileSync, mkdirSync, readdirSync } from 'node:fs'
import { load } from '@slidev/parser/fs'

const root = process.cwd()
const { slides } = await load({ roots: [root], userRoot: root }, `${root}/slides.md`)
const renders = readdirSync('out/slides').sort()
mkdirSync('public/shots', { recursive: true })
for (const [i, slide] of slides.entries()) {
  const name = slide.frontmatter.shot
  if (!name) continue
  const prefix = `${String(i + 1).padStart(3, '0')}-`
  const steps = renders.filter(file => file.startsWith(prefix))
  if (steps.length === 0) throw new Error(`No render for the slide "${slide.frontmatter.title}". Run pnpm png first.`)
  copyFileSync(`out/slides/${steps.at(-1)}`, `public/shots/${name}.png`)
  console.log(`${name}.png from ${steps.at(-1)}`)
}
