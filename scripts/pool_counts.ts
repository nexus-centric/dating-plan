import { items } from '/workspace/date-app/src/data'
import { pools } from '/workspace/date-app/src/planner'
for (const d of ['Phú Nhuận','Tân Bình','Tân Phú','Quận 1']) console.log(d, Object.fromEntries(['meal','sweet','photobooth','choi','cafe','game','spa','workshop','dessertp'].map(k=>[k, items.filter(i=>i.area===d&&!i.out_of_area&&(pools as any)[k](i)).length])))
