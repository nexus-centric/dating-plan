// Range × combo simulation: npx tsx scripts/sim_ranges.ts > scripts/sim_ranges.txt
import { plan, COMBOS, RANGES, total, tierOf, catKey } from '../src/planner'
const RUNS = +(process.env.RUNS ?? 12)
const out: string[] = []; const log = (s: string) => { out.push(s); console.log(s) }
const combos = COMBOS.filter(c => c.id !== 'random')
for (const long of [false, true]) {
  log(`\n=== ${long ? '3 điểm (Buổi dài)' : '2 điểm'} · ${RUNS} lần chạy × 3 kèo ===`)
  const summary: string[] = []
  for (const r of RANGES) {
    log(`\n-- ${r.label} --\ncombo\tpart\tplans/run\tsure(Σmax≤max)\tinRange(sure & Σmax≥min)\tmaybe\tunknown\tover\tavg`)
    let viable = 0, viableR = 0; const kinds = new Set<string>(), cats = new Set<string>(); let rep = 0, repN = 0
    for (const c of [...combos, COMBOS.find(c => c.id === 'random')!]) {
      const part = c.part ?? 'toi'
      let n = 0, sure = 0, inR = 0, maybe = 0, unk = 0, over = 0, sum = 0
      for (let t = 0; t < RUNS; t++) {
        const res = plan({ budget: r.max, min: r.min, districts: [], combo: c.id, moods: [], long, part })
        const cs = res.plans.flatMap(p => p.slots.map(s => catKey(s.item))); if (cs.length) { rep += 1 - new Set(cs).size / cs.length; repN++ }
        for (const p of res.plans) {
          n++; const T = tierOf(p.slots.map(s => s.item), r.max), tt = total(p); sum += (tt.lo + tt.hi) / 2
          p.slots.forEach(s => { kinds.add(s.item.kind); cats.add(catKey(s.item)) })
          if (T === 0) { sure++; if (tt.hi >= r.min || r.min === 0) inR++ } else if (T === 1) maybe++; else if (T === 2) unk++; else over++
        }
      }
      const pc = (x: number) => n ? Math.round(x / n * 100) + '%' : '-'
      if (c.id !== 'random' && n && sure / n >= 0.8) viable++
      if (c.id !== 'random' && n && sure / n >= 0.8 && inR / n >= 0.5) viableR++
      log([c.id, part, (n / RUNS).toFixed(1), pc(sure), pc(inR), pc(maybe), pc(unk), pc(over), n ? Math.round(sum / n / 1000) + 'k' : '-'].join('\t'))
    }
    const line = `${r.label}: viable combos: ≥80% chắc chắn = ${viable}/${combos.length}; ≥80% chắc chắn AND ≥50% in-range (Σmax ≥ range min) = ${viableR} · distinct kinds ${kinds.size} · categories ${cats.size} · category repeat rate across the 3 plans ${Math.round(rep / Math.max(1, repN) * 100)}%`
    log(line); summary.push(line)
  }
  log('\nSUMMARY ' + (long ? '3-stop' : '2-stop')); summary.forEach(l => log(l))
}
import('fs').then(fs => fs.writeFileSync(new URL('./sim_ranges.txt', import.meta.url), out.join('\n') + '\n'))
