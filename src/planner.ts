import { Item, items, inDistrict, ratingScore, Kind } from './data'
export type Combo = 'cafe' | 'choi' | 'workshop' | 'checkin' | 'spa' | 'photobooth' | 'finedining' | 'game' | 'deeptalk'
  | 'anvat' | 'cafephoto' | 'chedem' | 'baotang' | 'phim' | 'song' | 'boardgame' | 'karaoke' | 'thethao' | 'thucung' | 'xemkich' | 'random'
/** part = gợi ý buổi phù hợp (vd. bảo tàng đóng cửa ~17h) */
export const COMBOS: { id: Combo; label: string; part?: 'chieu' | 'toi' | 'dem' }[] = [
  { id: 'cafe', label: '🍜 Ăn + Cafe' }, { id: 'anvat', label: '🥢 Ăn vặt + Dạo phố' }, { id: 'chedem', label: '🍧 Chè/kem + Dạo đêm' },
  { id: 'phim', label: '🎬 Ăn + Xem phim' }, { id: 'choi', label: '🎳 Ăn + Đi chơi' }, { id: 'photobooth', label: '📸 Ăn + Photobooth' },
  { id: 'cafephoto', label: '☕ Cafe + Photobooth', part: 'chieu' }, { id: 'baotang', label: '🏛️ Bảo tàng + Cafe', part: 'chieu' },
  { id: 'song', label: '⛴️ Sông Sài Gòn + Ăn' }, { id: 'boardgame', label: '🎲 Ăn + Board game' }, { id: 'karaoke', label: '🎤 Ăn + Karaoke' },
  { id: 'thethao', label: '🏹 Vận động + Ăn' }, { id: 'thucung', label: '🐱 Cafe thú cưng + Ăn' }, { id: 'xemkich', label: '🎭 Ăn + Kịch / Nhạc sống', part: 'toi' }, { id: 'game', label: '🎮 Ăn + Game' }, { id: 'spa', label: '💆 Ăn + Spa' },
  { id: 'workshop', label: '🎨 Ăn + Workshop' }, { id: 'checkin', label: '🌃 Ăn + Check-in' }, { id: 'finedining', label: '🥂 Fine dining' },
  { id: 'deeptalk', label: '🕯️ Deep talk' }, { id: 'random', label: '🎲 Bất ngờ đi' }]

/* ---------- Budget ranges (cho 2 người, tối đa 1tr/buổi) ---------- */
export interface Range { id: string; min: number; max: number; label: string }
export const RANGES: Range[] = [
  { id: 'r0', min: 0, max: 200e3, label: 'Dưới 200k' }, { id: 'r2', min: 200e3, max: 300e3, label: '200–300k' },
  { id: 'r4', min: 400e3, max: 500e3, label: '400–500k' }, { id: 'r6', min: 600e3, max: 700e3, label: '600–700k' },
  { id: 'r8', min: 800e3, max: 900e3, label: '800–900k' }, { id: 'r9', min: 900e3, max: 1e6, label: '900k–1tr' }]
export const rangeOf = (budget: number, min?: number | null): Range => RANGES.find(r => r.max === budget && (min == null || r.min === min)) ?? RANGES.find(r => r.max >= budget) ?? RANGES[RANGES.length - 1]

/* ---------- Category → slot rules ----------
 * meal (bữa tối):      chỉ nhà hàng thật / phố ẩm thực (kind restaurant | streetfood). Bar, rooftop, cafe, dessert KHÔNG vào đây.
 * fine (fine dining):  nhà hàng thuộc list Fine Dining, hoặc mood "sang chảnh", hoặc giá ≥ 1tr/2 người.
 * sweet (sau bữa tối): cafe | dessert | bar (rooftop/cocktail).
 * night (sau fine):    bar/rooftop hoặc show (phòng trà, kịch).
 * deeptalk:            quán trong list Deep talk, hoặc cafe/bar có mood chill/lãng mạn.
 * choi:                game | show | cinema | sight | experience.  checkin: sight + rooftop bar.
 * photobooth | spa | game | workshop: theo kind. Homestay, shopping chỉ để khám phá, không vào planner tối. */
const k = (i: Item, ...ks: Kind[]) => ks.includes(i.kind)
export const pools = {
  meal: (i: Item) => k(i, 'restaurant', 'streetfood'),
  fine: (i: Item) => k(i, 'restaurant') && (i.lists.includes('Fine Dining date') || i.mood_tags.includes('sang chảnh') || (i.price_per_couple_vnd ?? 0) >= 1e6),
  sweet: (i: Item) => k(i, 'cafe', 'dessert', 'bar'),
  night: (i: Item) => k(i, 'bar', 'show'),
  deeptalk: (i: Item) => i.lists.includes('Deep talk date') || (k(i, 'cafe', 'bar') && i.mood_tags.some(m => m === 'chill' || m === 'lãng mạn')),
  choi: (i: Item) => k(i, 'game', 'show', 'cinema', 'sight', 'experience'),
  checkin: (i: Item) => k(i, 'sight') || (k(i, 'bar') && /rooftop/i.test(i.category + ' ' + i.name)),
  workshop: (i: Item) => k(i, 'workshop'),
  photobooth: (i: Item) => k(i, 'photobooth'),
  spa: (i: Item) => k(i, 'spa'),
  game: (i: Item) => k(i, 'game'),
  cheapmeal: (i: Item) => k(i, 'restaurant', 'streetfood') && (priceRange(i)?.[1] ?? Infinity) <= 300e3,
  walk: (i: Item) => k(i, 'sight') && (priceRange(i)?.[1] ?? Infinity) <= 60e3,
  dessertp: (i: Item) => k(i, 'dessert') || (k(i, 'streetfood', 'cafe') && /chè|kem|tráng miệng|dessert/i.test(i.category + ' ' + i.name)),
  cafe: (i: Item) => k(i, 'cafe'),
  museum: (i: Item) => k(i, 'sight') && /bảo tàng|triển lãm|nghệ thuật|art|museum|dinh /i.test(i.category + ' ' + i.name),
  cinema: (i: Item) => k(i, 'cinema'),
  river: (i: Item) => k(i, 'sight') && /water ?bus|bạch đằng|bờ sông|ba son|sông|thủ thiêm/i.test(i.category + ' ' + i.name),
  boardgame: (i: Item) => /board ?game|cờ bàn/i.test(i.category + ' ' + i.name),
  karaoke: (i: Item) => /karaoke/i.test(i.category + ' ' + i.name),
  pet: (i: Item) => /thú cưng|cat cafe|cafe mèo|pet/i.test(i.category + ' ' + i.name),
  stage: (i: Item) => k(i, 'show') && /kịch|phòng trà|nhạc sống|acoustic|jazz/i.test(i.category + ' ' + i.name),
  sport: (i: Item) => k(i, 'game') && /bowling|bida|billiard|bắn cung|leo núi|climb|patin|pickleball|escape|thoát hiểm|trượt băng|jump/i.test(i.category + ' ' + i.name),
}
export type PoolKey = keyof typeof pools
const LABEL: Record<PoolKey, string> = { meal: 'Ăn tối', fine: 'Fine dining', sweet: 'Cafe / tráng miệng / bar', night: 'Bar / nhạc sống', deeptalk: 'Deep talk', choi: 'Đi chơi', checkin: 'Check-in', workshop: 'Workshop', photobooth: 'Photobooth', spa: 'Spa / thư giãn', game: 'Game',
  cheapmeal: 'Ăn bình dân / ăn vặt', walk: 'Dạo phố (miễn phí)', dessertp: 'Chè / kem', cafe: 'Cafe', museum: 'Bảo tàng / triển lãm', cinema: 'Xem phim', river: 'Sông Sài Gòn', boardgame: 'Board game', karaoke: 'Karaoke', sport: 'Vận động', pet: 'Cafe thú cưng', stage: 'Kịch / nhạc sống' }
/** typical minutes spent at each kind of stop (used to chain slot times) */
const DUR: Record<PoolKey, number> = { meal: 90, fine: 120, sweet: 75, night: 90, deeptalk: 90, choi: 90, checkin: 60, workshop: 120, photobooth: 45, spa: 90, game: 90,
  cheapmeal: 60, walk: 60, dessertp: 45, cafe: 75, museum: 90, cinema: 135, river: 75, boardgame: 120, karaoke: 120, sport: 90, pet: 75, stage: 120 }
const GAP = 15 // travel between stops
type R = Exclude<Combo, 'random'>
/** 2-stop recipes (unchanged order) + optional "Buổi dài" 3-stop recipes */
const RECIPES: Record<R, PoolKey[]> = {
  cafe: ['meal', 'sweet'], choi: ['meal', 'choi'], photobooth: ['meal', 'photobooth'], game: ['meal', 'game'], spa: ['spa', 'meal'],
  workshop: ['workshop', 'meal'], checkin: ['meal', 'checkin'], finedining: ['fine', 'night'], deeptalk: ['meal', 'deeptalk'],
  anvat: ['cheapmeal', 'walk'], cafephoto: ['cafe', 'photobooth'], chedem: ['dessertp', 'walk'], baotang: ['museum', 'cafe'], phim: ['meal', 'cinema'],
  song: ['river', 'meal'], boardgame: ['meal', 'boardgame'], karaoke: ['meal', 'karaoke'], thethao: ['sport', 'meal'], thucung: ['pet', 'meal'], xemkich: ['meal', 'stage'],
}
const LONG: Record<R, PoolKey[]> = {
  cafe: ['photobooth', 'meal', 'sweet'], choi: ['choi', 'meal', 'sweet'], photobooth: ['photobooth', 'meal', 'sweet'], game: ['game', 'meal', 'sweet'],
  spa: ['spa', 'meal', 'sweet'], workshop: ['workshop', 'meal', 'sweet'], checkin: ['meal', 'checkin', 'sweet'], finedining: ['checkin', 'fine', 'night'],
  deeptalk: ['choi', 'meal', 'deeptalk'],
  anvat: ['cheapmeal', 'walk', 'dessertp'], cafephoto: ['cafe', 'photobooth', 'cheapmeal'], chedem: ['cheapmeal', 'dessertp', 'walk'], baotang: ['museum', 'cafe', 'meal'],
  phim: ['meal', 'cinema', 'dessertp'], song: ['river', 'meal', 'sweet'], boardgame: ['meal', 'boardgame', 'dessertp'], karaoke: ['meal', 'karaoke', 'dessertp'], thethao: ['sport', 'meal', 'sweet'], thucung: ['pet', 'meal', 'dessertp'], xemkich: ['meal', 'stage', 'dessertp'],
}
const RANDOM_POOL: R[] = ['cafe', 'choi', 'photobooth', 'game', 'checkin', 'deeptalk', 'anvat', 'chedem', 'phim', 'boardgame', 'karaoke', 'thethao', 'song', 'thucung', 'xemkich']

/* ---------- Date part / time ---------- */
export type Part = 'chieu' | 'toi' | 'dem'
export const PARTS: { id: Part; label: string; start: number }[] = [
  { id: 'chieu', label: '☀️ Chiều (~14:00)', start: 14 * 60 }, { id: 'toi', label: '🌆 Tối (~18:00)', start: 18 * 60 }, { id: 'dem', label: '🌙 Đêm (~20:30)', start: 20 * 60 + 30 }]
export const DOW = ['CN', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7'] // index = JS getDay()
export const toMin = (t: string) => { const [h, m] = t.split(':').map(Number); return h * 60 + m }
export const toHHMM = (m: number) => `${String(Math.floor(m / 60) % 24).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`
export function slotTimes(keys: PoolKey[], part: Part = 'toi') {
  let t = PARTS.find(x => x.id === part)!.start; const out: number[] = []
  for (const key of keys) { out.push(t); t += DUR[key] + GAP; t = Math.ceil(t / 15) * 15 }
  return out
}

/* ---------- Adjacency (quận cũ; TP Thủ Đức tách Q2 cũ / Thủ Đức cũ, Q9 cũ đã loại) ---------- */
export const ADJ_LIST: Record<string, string[]> = {
  'Quận 1': ['Quận 3', 'Quận 4', 'Quận 5', 'Bình Thạnh', 'Phú Nhuận', 'TP Thủ Đức (Q2 cũ)'],
  'Quận 3': ['Quận 1', 'Quận 10', 'Phú Nhuận', 'Tân Bình', 'Bình Thạnh'],
  'Quận 4': ['Quận 1', 'Quận 7', 'Quận 8', 'TP Thủ Đức (Q2 cũ)'],
  'Quận 5': ['Quận 1', 'Quận 6', 'Quận 8', 'Quận 10', 'Quận 11'],
  'Quận 6': ['Quận 5', 'Quận 8', 'Quận 11', 'Tân Phú'],
  'Quận 7': ['Quận 4', 'Quận 8', 'TP Thủ Đức (Q2 cũ)'],
  'Quận 8': ['Quận 4', 'Quận 5', 'Quận 6', 'Quận 7'],
  'Quận 10': ['Quận 3', 'Quận 5', 'Quận 11', 'Tân Bình'],
  'Quận 11': ['Quận 5', 'Quận 6', 'Quận 10', 'Tân Bình', 'Tân Phú'],
  'Phú Nhuận': ['Quận 1', 'Quận 3', 'Bình Thạnh', 'Tân Bình', 'Gò Vấp'],
  'Bình Thạnh': ['Quận 1', 'Quận 3', 'Phú Nhuận', 'Gò Vấp', 'TP Thủ Đức (Q2 cũ)', 'TP Thủ Đức (Thủ Đức cũ)'],
  'Tân Bình': ['Quận 3', 'Quận 10', 'Quận 11', 'Phú Nhuận', 'Tân Phú', 'Gò Vấp'],
  'Tân Phú': ['Tân Bình', 'Quận 11', 'Quận 6'],
  'Gò Vấp': ['Phú Nhuận', 'Tân Bình', 'Bình Thạnh'],
  'TP Thủ Đức (Q2 cũ)': ['Quận 1', 'Quận 4', 'Quận 7', 'Bình Thạnh', 'TP Thủ Đức (Thủ Đức cũ)'],
  'TP Thủ Đức (Thủ Đức cũ)': ['Bình Thạnh', 'TP Thủ Đức (Q2 cũ)'],
}
const ALIAS: Record<string, string> = { 'Thảo Điền (TP Thủ Đức)': 'TP Thủ Đức (Q2 cũ)' }
const norm = (a: string) => ALIAS[a] ?? a
export const near = (a0: string | null, b0: string | null) => {
  if (!a0 || !b0) return false; const a = norm(a0), b = norm(b0)
  return a === b || (ADJ_LIST[a]?.includes(b) ?? false) || (ADJ_LIST[b]?.includes(a) ?? false)
}
export const neighbours = (ds: string[]) => [...new Set(ds.flatMap(d => [d, ...(ADJ_LIST[norm(d)] ?? [])]))]
export function distanceKm(a: Item, b: Item): number | null {
  if (a.lat == null || a.lng == null || b.lat == null || b.lng == null) return null
  const R = 6371, r = Math.PI / 180, dLat = (b.lat - a.lat) * r, dLng = (b.lng - a.lng) * r
  const x = Math.sin(dLat / 2) ** 2 + Math.cos(a.lat * r) * Math.cos(b.lat * r) * Math.sin(dLng / 2) ** 2
  return 2 * R * Math.asin(Math.sqrt(x))
}

/* ---------- Opening hours: hard rule when known, soft when unknown ---------- */
const DAYNAME: Record<string, number> = { 'chủ nhật': 0, cn: 0, 'hai': 1, 'ba': 2, 'tư': 3, 'năm': 4, 'sáu': 5, 'bảy': 6 }
/** weekday closures parsed from free-text opening_hours (only a few clear patterns) */
export function closedOnDay(i: Item, dow: number | null): boolean {
  if (dow == null || !i.opening_hours) return false
  const s = i.opening_hours.toLowerCase()
  const m = s.match(/(?:đóng cửa|nghỉ)\s+(?:thứ\s+)?(chủ nhật|cn|hai|ba|tư|năm|sáu|bảy)/); if (m && DAYNAME[m[1]] === dow) return true
  if (/\bcn\s+nghỉ/.test(s) && dow === 0) return true
  const r = s.match(/^t([2-7])\s*[–-]\s*(cn|t[2-7])\b/)   // "T4–CN 10:00–19:00" → open only that range
  if (r && !/,|;/.test(s.split(/\d{2}:/)[0])) {
    const a = +r[1] - 1, b = r[2] === 'cn' ? 7 : +r[2].slice(1) - 1, d = dow === 0 ? 7 : dow
    if (!/cn\s+\d/.test(s) && (d < a || d > b)) return true
  }
  return false
}
/** true = known closed at that minute (or closes within 45'); false = open; null = unknown */
export function closedAt(i: Item, time: string | number, dow: number | null = null): boolean | null {
  if (closedOnDay(i, dow)) return true
  if (!i.hours) return null
  const t = typeof time === 'number' ? time : toMin(time), [o, c] = i.hours
  const ok = (x: number) => x >= o && x + 45 <= c
  return !(ok(t) || ok(t + 1440))
}

/* ---------- Prices ---------- */
/** couple price range [lo, hi] or null when unknown */
export function priceRange(i: Item): [number, number] | null {
  if (i.price_unit === 'free') return [0, 0]
  const lo = i.couple_min ?? i.price_per_couple_vnd ?? i.couple_max, hi = i.couple_max ?? i.price_per_couple_vnd ?? i.couple_min
  return lo == null || hi == null ? null : [lo, hi]
}
/** 0 = chắc chắn (Σmax ≤ budget) · 1 = có thể (Σmin ≤ budget) · 2 = có điểm chưa rõ giá · 3 = vượt ngân sách */
export type Tier = 0 | 1 | 2 | 3
export const TIER_LABEL: Record<Tier, string> = { 0: '✅ Chắc chắn trong ngân sách', 1: '🟡 Có thể vừa ngân sách', 2: '❔ Có điểm chưa rõ giá', 3: '⚠️ Vượt ngân sách' }
export function tierOf(its: Item[], budget: number): Tier {
  let lo = 0, hi = 0, unk = false
  for (const i of its) { const r = priceRange(i); if (!r) unk = true; else { lo += r[0]; hi += r[1] } }
  if (lo > budget) return 3
  if (unk) return 2
  return hi <= budget ? 0 : 1
}

export interface Prefs { budget: number; /** range lower bound (budget = upper bound) */ min?: number; districts: string[]; combo: Combo; moods: string[]; part?: Part; dow?: number | null; long?: boolean }
export interface Slot { time: string; label: string; key: PoolKey; item: Item; km?: number | null; closed?: boolean | null }
export interface Plan { slots: Slot[]; tier?: Tier; recipe?: R }
export interface PlanResult { plans: Plan[]; best: Tier | null; minSure: number | null; minMaybe: number | null; altCombos: Combo[]; empty?: { district: string[]; count: number; slot: string; neighbours: string[]; neighbourCount: number } | null }

/* ---------- Recent history: places/plans shown in the last presses get a penalty (sessionStorage, per tab) ---------- */
const HKEY = 'planner-recent-v1', MAX_IDS = 36, MAX_SIGS = 30
let hist: { ids: string[]; sigs: string[] } = (() => { try { const h = JSON.parse(sessionStorage.getItem(HKEY) || ''); if (Array.isArray(h?.ids) && Array.isArray(h?.sigs)) return h } catch { /* no storage */ } return { ids: [], sigs: [] } })()
const saveHist = () => { try { sessionStorage.setItem(HKEY, JSON.stringify(hist)) } catch { /* ignore */ } }
const sigOf = (its: Item[]) => its.map(i => i.id).join('|')
/** remember shown places (newest first) so the next press prefers fresh ones */
export function remember(ids: string[], sigs: string[] = []) {
  hist = { ids: [...ids, ...hist.ids.filter(x => !ids.includes(x))].slice(0, MAX_IDS), sigs: [...sigs, ...hist.sigs.filter(x => !sigs.includes(x))].slice(0, MAX_SIGS) }; saveHist()
}
export const resetHistory = () => { hist = { ids: [], sigs: [] }; saveHist() }
/** 0 if not shown recently; decays with age (≈ last 2 presses strongest) */
const recentPen = (id: string) => { const k = hist.ids.indexOf(id); return k < 0 ? 0 : k < 12 ? 4 : k < 24 ? 2.5 : 1.2 }
/** weighted random pick: lower score = more likely (softmax, temperature T) */
function pickWeighted<T>(xs: { c: T; v: number }[], T = 1.2): T {
  const m = Math.min(...xs.map(x => x.v)); const w = xs.map(x => Math.exp(-(x.v - m) / T)); let r = Math.random() * w.reduce((a, b) => a + b, 0)
  for (let k = 0; k < xs.length; k++) { r -= w[k]; if (r <= 0) return xs[k].c } return xs[xs.length - 1].c
}

const baseOk = (i: Item) => i.type !== 'idea' && !i.out_of_area
/** secondary score: lower is better (rating, mood, data quality, a bit of randomness) */
function sec(i: Item, p: Prefs, t: number) {
  let s = 0
  if (p.moods.length && !i.mood_tags.some(m => p.moods.includes(m))) s += 1.5
  if (closedAt(i, t, p.dow ?? null) == null) s += 0.6
  if (i.status === 'uncertain') s += 1
  s -= (ratingScore(i) - 4) * 2   // rating is a weight, not a hard sort
  s += recentPen(i.id)
  return s + Math.random() * 2
}
const link = (a: Item, b: Item) => { const d = distanceKm(a, b); return (d != null ? Math.max(0, d - 2) * 0.4 : 0.3) - (a.area === b.area ? 0.5 : 0) }

/** target total for the chosen range (midpoint); null = plain "≤ budget" mode */
const target = (p: Prefs) => p.min != null ? (p.min + p.budget) / 2 : null
/** penalty (score units) for a chain whose [lo,hi] sits away from the chosen range – so 800–900k gets nicer plans than 200–300k */
export function rangePenalty(lo: number, hi: number, p: Prefs) {
  const T = target(p); if (T == null) return 0
  const mid = (lo + hi) / 2, under = Math.max(0, (p.min ?? 0) - hi)          // whole plan cheaper than the range
  return Math.abs(mid - T) / 100e3 * 1.2 + under / 100e3 * 2
}
/** candidates for one slot: pool ∩ open-at-time ∩ (district | near previous) – top by score, the cheapest ones and the ones priced near the range share */
function slotCands(key: PoolKey, p: Prefs, t: number, exclude: Set<string>, first: boolean, m: number, nKeys = 2) {
  const list = items.filter(i => baseOk(i) && pools[key](i) && !exclude.has(i.id) && closedAt(i, t, p.dow ?? null) !== true && (!first || inDistrict(i, p.districts)))
  const scored = list.map(i => ({ i, s: sec(i, p, t), hi: priceRange(i)?.[1] ?? Infinity }))
  const top = [...scored].sort((a, b) => a.s - b.s).slice(0, m)
  const cheap = [...scored].sort((a, b) => a.hi - b.hi || a.s - b.s).slice(0, m)
  const T = target(p), share = T != null ? T / nKeys : null
  const fit = share == null ? [] : [...scored].filter(x => x.hi !== Infinity).sort((a, b) => Math.abs(a.hi - share) - Math.abs(b.hi - share) || a.s - b.s).slice(0, m)
  return [...new Set([...top, ...cheap, ...fit])]
}
interface Chain { its: Item[]; tier: Tier; score: number; hi: number; lo: number }
function chains(keys: PoolKey[], p: Prefs, times: number[], exclude: Set<string>, m = keys.length > 2 ? 12 : 24): Chain[] {
  const cs = keys.map((key, i) => slotCands(key, p, times[i], exclude, i === 0, m, keys.length))
  const out: Chain[] = []
  const rec = (idx: number, acc: typeof cs[0], sc: number) => {
    if (idx === keys.length) {
      const its = acc.map(x => x.i); const tier = tierOf(its, p.budget)
      let lo = 0, hi = 0; for (const x of its) { const r = priceRange(x); lo += r?.[0] ?? 0; hi += r?.[1] ?? 0 }
      out.push({ its, tier, score: tier * 100 + sc + rangePenalty(lo, hi, p), hi, lo }); return
    }
    for (const c of cs[idx]) {
      if (acc.some(a => a.i.id === c.i.id)) continue
      const prev = acc[acc.length - 1]?.i
      if (prev && !near(prev.area, c.i.area)) continue           // same / adjacent district (hard rule)
      rec(idx + 1, [...acc, c], sc + c.s + (prev ? link(prev, c.i) : 0))
    }
  }
  rec(0, [], 0)
  return out
}
const recipeKeys = (r: R, long?: boolean) => (long ? LONG : RECIPES)[r]
const toPlan = (c: Chain, keys: PoolKey[], times: number[], r: R, dow: number | null): Plan => ({
  tier: c.tier, recipe: r,
  slots: c.its.map((it, i) => ({ time: toHHMM(times[i]), label: LABEL[keys[i]], key: keys[i], item: it, km: i ? distanceKm(c.its[i - 1], it) : undefined, closed: closedAt(it, times[i], dow) })),
})

/** cheapest fully-priced chain for a recipe (Σmax and Σmin) – for "you need at least X" messages */
function minBudgets(r: R, p: Prefs) {
  const keys = recipeKeys(r, p.long), times = slotTimes(keys, p.part)
  const cs = chains(keys, { ...p, moods: [], budget: 0 }, times, new Set(), keys.length > 2 ? 14 : 40).filter(c => c.its.every(i => priceRange(i)))
  return { sure: cs.length ? Math.min(...cs.map(c => c.hi)) : null, maybe: cs.length ? Math.min(...cs.map(c => c.lo)) : null }
}

export function plan(p: Prefs, n = 3): PlanResult {
  const recs: R[] = p.combo === 'random' ? RANDOM_POOL : [p.combo]
  const dow = p.dow ?? null
  const per = recs.map(r => { const keys = recipeKeys(r, p.long), times = slotTimes(keys, p.part); return { r, keys, times, cs: chains(keys, p, times, new Set()).sort((a, b) => a.score - b.score) } })
  const used = new Set<string>(), usedCat = new Set<string>(), usedArea = new Set<string>(); const plans: Plan[] = []
  for (let k = 0; k < n; k++) {
    const sig = new Set(plans.map(pl => pl.slots.map(s => s.item.id).join('|')))
    // fresh stops first; if that would drop to a worse budget tier, allow re-using ONE stop (e.g. the only cheap dinner) with different other stops
    const fresh = per.map(x => ({ ...x, cs: x.cs.filter(c => !c.its.some(i => used.has(i.id))) })).filter(x => x.cs.length)
    const reuse = per.map(x => ({ ...x, cs: x.cs.filter(c => c.its.filter(i => used.has(i.id)).length <= 1 && !sig.has(c.its.map(i => i.id).join('|')) && !plans.some(pl => pl.slots.filter(s => c.its.includes(s.item)).length > 1)) })).filter(x => x.cs.length)
    const bt = (a: typeof fresh) => a.length ? Math.min(...a.map(x => x.cs[0].tier)) : 9
    const avail = bt(reuse) < bt(fresh) ? reuse : fresh
    if (!avail.length) break
    const bestTier = Math.min(...avail.map(x => x.cs[0].tier))
    const good = avail.filter(x => x.cs[0].tier === bestTier)
    const usedR = new Set(plans.map(pl => pl.recipe))                        // random: rotate combo types
    const goodR = good.filter(x => !usedR.has(x.r)); const g = (goodR.length ? goodR : good)[Math.floor(Math.random() * (goodR.length || good.length))]
    // diversity: avoid repeating a category (e.g. two "phở" dinners) or a place type across the 3 plans
    // …and spread districts when the user didn't pick one
    const div = (c: Chain) => c.its.reduce((a, it) => a + (usedCat.has(catKey(it)) ? 1.2 : 0) + (!p.districts.length && it.area && usedArea.has(it.area) ? 0.5 : 0) + (usedCat.has('k:' + it.kind) ? 0.3 : 0), 0)
    const tierCs = g.cs.filter(c => c.tier === bestTier); let freshSig = tierCs.filter(c => !hist.sigs.includes(sigOf(c.its)))
    // small pool (one district): rather than repeating a recent plan, allow the "có thể vừa ngân sách" tier (Σmin still ≤ budget)
    if (freshSig.length < 3 && bestTier === 0) freshSig = [...freshSig, ...g.cs.filter(c => c.tier === 1 && !hist.sigs.includes(sigOf(c.its)))]
    const pool = (freshSig.length ? freshSig : tierCs).slice(0, 40).map(c => ({ c, v: c.score + div(c) }))
    const c = pickWeighted(pool)
    c.its.forEach(i => { used.add(i.id); usedCat.add(catKey(i)); usedCat.add('k:' + i.kind); if (i.area) usedArea.add(i.area) }); plans.push(toPlan(c, g.keys, g.times, g.r, dow))
  }
  if (plans.length) remember(plans.flatMap(pl => pl.slots.map(s => s.item.id)), plans.map(pl => sigOf(pl.slots.map(s => s.item))))
  const best = plans.length ? Math.min(...plans.map(x => x.tier!)) as Tier : null
  let minSure: number | null = null, minMaybe: number | null = null, altCombos: Combo[] = []
  if (best == null || best > 0) {
    const mb = recs.map(r => minBudgets(r, p))
    const s = mb.map(x => x.sure).filter((x): x is number => x != null), m = mb.map(x => x.maybe).filter((x): x is number => x != null)
    minSure = s.length ? Math.min(...s) : null; minMaybe = m.length ? Math.min(...m) : null
    altCombos = (Object.keys(RECIPES) as R[]).filter(r => !recs.includes(r) && chains(recipeKeys(r, p.long), { ...p, moods: [] }, slotTimes(recipeKeys(r, p.long), p.part), new Set(), 14).some(c => c.tier === 0))
  }
  let empty: PlanResult['empty'] = null
  if (!plans.length && p.districts.length) {
    const key = recipeKeys(recs[0], p.long)[0], t = slotTimes(recipeKeys(recs[0], p.long), p.part)[0]
    const cnt = (ds: string[]) => items.filter(i => baseOk(i) && pools[key](i) && closedAt(i, t, dow) !== true && inDistrict(i, ds)).length
    const nb = neighbours(p.districts)
    empty = { district: p.districts, count: cnt(p.districts), slot: LABEL[key], neighbours: nb, neighbourCount: cnt(nb) }
  }
  return { plans, best, minSure, minMaybe, altCombos, empty }
}
/** category key used for diversity (cuisine / activity type) */
export const catKey = (i: Item) => (i.category || i.kind).toLowerCase().replace(/\s*\(.*\)/, '').trim()
/** back-compat */
export const makePlans = (p: Prefs, n = 3) => plan(p, n).plans

/** how many first-stop places a district has for this combo/time (for chip counts) */
export function districtFit(p: Prefs, d: string) {
  const recs: R[] = p.combo === 'random' ? RANDOM_POOL : [p.combo]
  return new Set(recs.flatMap(r => { const keys = recipeKeys(r, p.long), t = slotTimes(keys, p.part)[0]
    return items.filter(i => baseOk(i) && pools[keys[0]](i) && i.area === d && closedAt(i, t, p.dow ?? null) !== true).map(i => i.id) })).size
}

/** swap one slot keeping adjacency with neighbours, opening hours and – first of all – the budget */
export function swapCandidates(pl: Plan, si: number, p: Prefs, used: Set<string>) {
  const s = pl.slots[si], prev = pl.slots[si - 1]?.item, next = pl.slots[si + 1]?.item, t = toMin(s.time)
  const others = pl.slots.filter((_, j) => j !== si).map(x => x.item)
  return items.filter(i => baseOk(i) && pools[s.key](i) && !used.has(i.id) && closedAt(i, t, p.dow ?? null) !== true
    && (!prev || near(prev.area, i.area)) && (!next || near(next.area, i.area)) && (prev || next || inDistrict(i, p.districts)))
    .map(i => [tierOf([...others, i], p.budget) * 100 + swapRange([...others, i], p) + sec(i, p, t) + (prev ? link(prev, i) : 0) + (next ? link(i, next) : 0), i] as const)
    .sort((a, b) => a[0] - b[0]).map(x => x[1])
}
function swapRange(its: Item[], p: Prefs) { let lo = 0, hi = 0; for (const x of its) { const r = priceRange(x); lo += r?.[0] ?? 0; hi += r?.[1] ?? 0 } return rangePenalty(lo, hi, p) }
export function relink(pl: Plan, p?: Prefs): Plan {
  const slots = pl.slots.map((s, i) => ({ ...s, km: i ? distanceKm(pl.slots[i - 1].item, s.item) : undefined, closed: closedAt(s.item, s.time, p?.dow ?? null) }))
  return { ...pl, slots, tier: p ? tierOf(slots.map(s => s.item), p.budget) : pl.tier }
}
export function total(pl: Plan) {
  let lo = 0, hi = 0, unknown = 0
  for (const s of pl.slots) { const r = priceRange(s.item); if (!r) unknown++; else { lo += r[0]; hi += r[1] } }
  return { lo, hi, sum: hi, unknown, slots: pl.slots.length }
}
export const slotLabel = (k: PoolKey) => LABEL[k]
