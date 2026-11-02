import raw from './data.json'
export type Kind = 'restaurant' | 'streetfood' | 'cafe' | 'bar' | 'dessert' | 'photobooth' | 'spa' | 'homestay' | 'workshop' | 'game' | 'show' | 'cinema' | 'shopping' | 'experience' | 'sight' | 'idea' | 'other'
export interface Item {
  id: string; name: string; type: 'food' | 'activity' | 'idea'; category: string; district: string | null; address: string | null
  price_per_couple_vnd: number | null; price_note: string | null; opening_hours: string | null; mood_tags: string[]
  description_vi: string; source_urls: string[]; source: string; out_of_area: boolean; status: string; date_checked: string
  rating: number | null; reviews: number | null; lat: number | null; lng: number | null; lists: string[]
  maps_url: string | null; website: string | null; google_category: string | null
  area: string | null      // normalized district (old district names; TP Thủ Đức split Q2/Thủ Đức cũ)
  kind: Kind               // derived at build time (data/build_merge) – drives planner slots
  hours: [number, number] | null // [open, close] minutes from 00:00 when parseable (close may exceed 1440)
  image?: string; image_credit?: string; image_source_url?: string; image_kind?: 'photo' | 'logo'
  price_min?: number | null; price_max?: number | null; price_unit?: string | null
  couple_min?: number | null; couple_max?: number | null
  price_source_url?: string | null; price_confidence?: 'high' | 'medium' | 'low' | null; price_checked?: string | null
  maps_kind?: 'direct' | 'search'
}
// status 'closed' = a recent source reports the place stopped operating -> hidden everywhere
export const items: Item[] = (raw as unknown as Omit<Item, 'id'>[]).filter(x => x && typeof x === 'object')
  .map((x, i) => ({ ...x, name: String(x.name ?? ''), category: x.category ?? 'Khác', description_vi: x.description_vi ?? '', mood_tags: Array.isArray(x.mood_tags) ? x.mood_tags : [], lists: Array.isArray(x.lists) ? x.lists : [], source_urls: Array.isArray(x.source_urls) ? x.source_urls.filter(Boolean) : [], id: `${i}-${x.name}` }))
  .filter(x => x.name && x.status !== 'closed' && x.status !== 'hidden')
export const MOODS = ['lãng mạn', 'chill', 'năng động', 'ngày mưa', 'kỷ niệm', 'rẻ mà vui', 'sang chảnh', 'đêm muộn']
// District filter options derived from data (sorted by number of places)
const counts = new Map<string, number>()
items.forEach(i => { if (i.area && !i.out_of_area && i.type !== 'idea') counts.set(i.area, (counts.get(i.area) ?? 0) + 1) })
export const DISTRICTS = [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0], 'vi')).map(e => e[0])
export const districtCount = (d: string) => counts.get(d) ?? 0
export const inDistrict = (it: Item, ds: string[]) => !ds.length || (it.area != null && ds.includes(it.area))
export const isUncertain = (it: Item) => it.status === 'uncertain'
export const fmt = (v: number) => v >= 1e6 ? `${(v / 1e6).toLocaleString('vi-VN', { maximumFractionDigits: 1 })}tr` : `${Math.round(v / 1000)}k`
/** couple estimate as [lo, hi] (either may be null) */
export const coupleRange = (it: Item): [number | null, number | null] => it.couple_min != null || it.couple_max != null ? [it.couple_min ?? null, it.couple_max ?? null] : it.price_per_couple_vnd != null ? [it.price_per_couple_vnd, it.price_per_couple_vnd] : [null, null]
export const fmtRange = (lo: number | null, hi: number | null) => lo != null && hi != null ? (lo === hi ? `~${fmt(lo)}` : lo === 0 ? `≤${fmt(hi)}` : `~${fmt(lo)}–${fmt(hi)}`) : lo != null ? `từ ${fmt(lo)}` : hi != null ? `≤${fmt(hi)}` : ''
export const UNIT: Record<string, string> = { person: '/người', drink: '/ly', dish: '/món', session: '/lượt', ticket: '/vé', couple: '/2 người', hour: '/giờ', room: '/phòng', free: '' }
export const mapsUrl = (it: Item) => it.maps_url ?? ('https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent([it.name, it.address ?? it.district ?? 'TP.HCM'].join(' ')))
/** rating score that doesn't over-reward 5.0 with 3 reviews (Bayesian average, prior 4.3 @ 30 reviews) */
export const ratingScore = (it: Item) => it.rating == null ? 0 : (it.rating * (it.reviews ?? 0) + 4.3 * 30) / ((it.reviews ?? 0) + 30)
export const byRating = (a: Item, b: Item) => ratingScore(b) - ratingScore(a)
export const fmtCount = (n: number) => n >= 1000 ? `${(n / 1000).toLocaleString('vi-VN', { maximumFractionDigits: 1 })}k` : String(n)
const EMO: Record<Kind, [string, string]> = {
  restaurant: ['🍽️', 'bg-orange-200'], streetfood: ['🍢', 'bg-yellow-200'], cafe: ['☕', 'bg-amber-200'],
  bar: ['🍸', 'bg-indigo-300'], dessert: ['🍰', 'bg-pink-200'], photobooth: ['📸', 'bg-rose-200'],
  spa: ['💆', 'bg-emerald-100'], homestay: ['🏡', 'bg-orange-100'], workshop: ['🎨', 'bg-teal-200'],
  game: ['🎮', 'bg-lime-200'], show: ['🎭', 'bg-violet-300'], cinema: ['🎬', 'bg-slate-300'],
  shopping: ['🛍️', 'bg-pink-200'], experience: ['✨', 'bg-amber-100'], sight: ['🌃', 'bg-violet-300'],
  idea: ['💡', 'bg-yellow-100'], other: ['💞', 'bg-pink-200'],
}
export const look = (it: Item) => { const m = it.out_of_area ? ['🏕️', 'bg-emerald-200'] : EMO[it.kind] ?? EMO.other; return { emoji: m[0], grad: m[1] } }
