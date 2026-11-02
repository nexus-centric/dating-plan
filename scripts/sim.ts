// Planner simulation: npx tsx scripts/sim.ts
import { plan, COMBOS, total, tierOf } from '../src/planner'
const budgets = [200000, 300000, 500000, 1000000, 2000000]
const RUNS = +(process.env.RUNS ?? 30)
const long = process.env.LONG === '1'
console.log(`combo\tbudget\tplans/run\tsure(Σmax≤B)\tmaybe(Σmin≤B)\tunknown\tover\temptyRuns\tminSure${long ? '\t[3 stops]' : ''}`)
for (const c of COMBOS) for (const b of budgets) {
  let n = 0, sure = 0, maybe = 0, unk = 0, over = 0, empty = 0, ms: number | null = null
  for (let t = 0; t < RUNS; t++) {
    const r = plan({ budget: b, districts: [], combo: c.id, moods: [], long }); if (!r.plans.length) empty++; ms = r.minSure ?? ms
    for (const p of r.plans) { n++; const T = tierOf(p.slots.map(s => s.item), b); total(p); if (T === 0) sure++; else if (T === 1) maybe++; else if (T === 2) unk++; else over++ }
  }
  const pc = (x: number) => n ? Math.round(x / n * 100) + '%' : '-'
  console.log([c.id, b / 1000 + 'k', (n / RUNS).toFixed(1), pc(sure), pc(maybe), pc(unk), pc(over), empty, ms ? ms / 1000 + 'k' : ''].join('\t'))
}
for (const d of [['Quận 4'], ['Quận 5'], ['Gò Vấp']]) {
  const r = plan({ budget: 500000, districts: d, combo: 'cafe', moods: [] })
  console.log(d, r.plans.length, r.plans.map(p => p.slots.map(s => s.item.area).join('>')).join(' | '), r.empty ? JSON.stringify(r.empty) : '')
}
