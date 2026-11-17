// Copies the last build step of the four key slides from out/slides/ (written by
// `pnpm png`) to public/shots/, where the Questions slide shows them. A slide is found
// by its title, so the copies stay right when slides move.
import { copyFileSync, mkdirSync, readFileSync, readdirSync } from 'node:fs'

const shots = {
  'Regression Detection': 'regression-detection',
  'Best-Effort Classification': 'best-effort-classification',
  'Test Generalization': 'test-generalization',
  'Summary': 'summary',
}
const titles = readFileSync('slides.md', 'utf8').split('\n')
  .filter(line => line.startsWith('title:'))
  .map(line => line.slice('title:'.length).trim())
const renders = readdirSync('out/slides').sort()
mkdirSync('public/shots', { recursive: true })
for (const [title, name] of Object.entries(shots)) {
  const slide = String(titles.indexOf(title) + 1).padStart(3, '0')
  const steps = renders.filter(file => file.startsWith(`${slide}-`))
  if (titles.indexOf(title) < 0 || steps.length === 0) throw new Error(`No render for the slide "${title}". Run pnpm png first.`)
  copyFileSync(`out/slides/${steps.at(-1)}`, `public/shots/${name}.png`)
  console.log(`${name}.png from ${steps.at(-1)}`)
}
