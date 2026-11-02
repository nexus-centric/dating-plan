// Diversity sim: npx tsx scripts/sim_diversity.ts  — 20 consecutive "Lên kèo" presses per setting
import { plan, Prefs } from '../src/planner'
const S: [string, Partial<Prefs>][] = [
  ['cafe 400-500k all', { combo: 'cafe', budget: 500e3, min: 400e3, districts: [] }],
  ['cafe 200-300k Q1', { combo: 'cafe', budget: 300e3, min: 200e3, districts: ['Quận 1'] }],
  ['photobooth 400-500k PN', { combo: 'photobooth', budget: 500e3, min: 400e3, districts: ['Phú Nhuận'] }],
  ['choi 600-700k TB', { combo: 'choi', budget: 700e3, min: 600e3, districts: ['Tân Bình'] }],
  ['random 800-900k', { combo: 'random', budget: 900e3, min: 800e3, districts: [] }],
  ['deeptalk 400-500k Q3', { combo: 'deeptalk', budget: 500e3, min: 400e3, districts: ['Quận 3'] }],
  ['cafe 400-500k Tân Phú', { combo: 'cafe', budget: 500e3, min: 400e3, districts: ['Tân Phú'] }],
]
let tu = 0, tt = 0, tov = 0, tn = 0, trep = 0
for (const [name, q] of S) {
  const presses: string[][] = []; const sigs: string[][] = []
  for (let k = 0; k < 20; k++) { const r = plan({ moods: [], part: 'toi', dow: null, long: false, ...q } as Prefs); presses.push(r.plans.flatMap(p => p.slots.map(s => s.item.id))); sigs.push(r.plans.map(p => p.slots.map(s => s.item.id).join('|'))) }
  const all = presses.flat(), uniq = new Set(all).size
  let ov = 0; for (let k = 1; k < 20; k++) { const prev = new Set(presses[k - 1]); ov += presses[k].filter(x => prev.has(x)).length / Math.max(1, presses[k].length) }
  let rep = 0; for (let k = 1; k < 20; k++) { const win = new Set(sigs.slice(Math.max(0, k - 10), k).flat()); rep += sigs[k].filter(s => win.has(s)).length }
  tu += uniq; tt += all.length; tov += ov / 19; tn++; trep += rep
  console.log(`${name.padEnd(24)} unique ${uniq}/${all.length} (${Math.round(uniq / Math.max(1, all.length) * 100)}%)  overlap-with-previous-press ${Math.round(ov / 19 * 100)}%  full-plan repeats within 10 presses: ${rep}`)
}
console.log(`TOTAL unique ratio ${Math.round(tu / tt * 100)}%  avg consecutive overlap ${Math.round(tov / tn * 100)}%  repeats ${trep}`)
