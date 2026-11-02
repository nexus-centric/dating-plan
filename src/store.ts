import { get, set, del } from 'idb-keyval'
import { Item, items, mapsUrl, fmtRange } from './data'
import { Plan, PoolKey, slotLabel, total, distanceKm, Combo, COMBOS } from './planner'

/* ---------- share: plan <-> URL hash ---------- */
const byIdx = new Map(items.map(i => [i.id.split('-')[0], i] as const))
export const itemIdx = (i: Item) => i.id.split('-')[0]
export interface Meta { combo?: Combo; budget?: number; /** range lower bound (v6); old links have only budget */ min?: number; date?: string }
export function encodePlan(pl: Plan, m: Meta) {
  const q = new URLSearchParams()
  q.set('s', pl.slots.map(s => `${itemIdx(s.item)}.${s.key}.${s.time.replace(':', '')}`).join('~'))
  if (m.combo) q.set('c', m.combo); if (m.budget) q.set('b', String(m.budget)); if (m.min != null && m.budget) q.set('m', String(m.min)); if (m.date) q.set('d', m.date)
  return 'plan&' + q.toString()
}
export function decodePlan(hash: string): { plan: Plan; meta: Meta } | null {
  const h = hash.replace(/^#/, ''); if (!h.startsWith('plan&')) return null
  const q = new URLSearchParams(h.slice(5)); const s = q.get('s'); if (!s) return null
  const slots = s.split('~').map(x => { const [i, k, t] = x.split('.'); const item = byIdx.get(i); return item && k && t ? { item, key: k as PoolKey, time: `${t.slice(0, 2)}:${t.slice(2)}`, label: slotLabel(k as PoolKey) } : null })
  if (!slots.length || slots.some(x => !x)) return null
  const ok = slots as NonNullable<typeof slots[0]>[]
  return { plan: { slots: ok.map((x, i) => ({ ...x, km: i ? distanceKm(ok[i - 1].item, x.item) : undefined })) }, meta: { combo: (q.get('c') as Combo) || undefined, budget: +(q.get('b') ?? 0) || undefined, min: q.get('m') != null ? +q.get('m')! : undefined, date: q.get('d') ?? undefined } }
}
export const shareUrl = (pl: Plan, m: Meta) => `${location.origin}${location.pathname}#${encodePlan(pl, m)}`
export const fmtDate = (d?: string) => { if (!d) return ''; const x = new Date(d + 'T00:00:00'); return x.toLocaleDateString('vi-VN', { weekday: 'long', day: '2-digit', month: '2-digit' }) }
export function planText(pl: Plan, m: Meta) {
  const t = total(pl); const combo = COMBOS.find(c => c.id === m.combo)?.label
  const lines = [`💞 Kèo hẹn hò${combo ? ` · ${combo}` : ''}${m.date ? ` · ${fmtDate(m.date)}` : ''}`, '']
  pl.slots.forEach((s, i) => {
    lines.push(`${i + 1}. ${s.time} · ${s.label}: ${s.item.name}`)
    if (s.item.address) lines.push(`   📍 ${s.item.address}`)
    lines.push(`   🗺️ ${mapsUrl(s.item)}`)
  })
  const est = t.unknown === t.slots ? 'chưa rõ giá' : fmtRange(t.lo, t.hi) + (t.unknown ? ` + ${t.unknown} chỗ chưa rõ giá` : '')
  lines.push('', `💸 Ước tính cho 2 người: ${est}`, `👉 Xem kèo: ${shareUrl(pl, m)}`)
  return lines.join('\n')
}
export async function sharePlan(pl: Plan, m: Meta): Promise<'shared' | 'copied' | 'failed'> {
  const text = planText(pl, m), url = shareUrl(pl, m)
  if (navigator.share) { try { await navigator.share({ title: 'Kèo hẹn hò 💞', text, url }); return 'shared' } catch (e) { if ((e as Error).name === 'AbortError') return 'failed' } }
  try { await navigator.clipboard.writeText(text); return 'copied' } catch {
    const ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select()
    const ok = document.execCommand('copy'); ta.remove(); return ok ? 'copied' : 'failed'
  }
}

/* ---------- diary (localStorage) + photos (IndexedDB) ---------- */
export interface Entry { id: string; created: string; date: string; s: string; combo?: Combo; budget?: number; min?: number; done: boolean; note: string; photos: string[] }
const KEY = 'diary'
export const loadDiary = (): Entry[] => { try { return JSON.parse(localStorage.getItem(KEY) || '[]') } catch { return [] } }
export const saveDiary = (e: Entry[]) => localStorage.setItem(KEY, JSON.stringify(e))
export const entryPlan = (e: Entry) => decodePlan('plan&s=' + e.s)?.plan ?? null
export function newEntry(pl: Plan, m: Meta): Entry {
  const s = new URLSearchParams(encodePlan(pl, m).slice(5)).get('s')!
  return { id: Date.now().toString(36), created: new Date().toISOString(), date: m.date ?? new Date().toISOString().slice(0, 10), s, combo: m.combo, budget: m.budget, min: m.min, done: false, note: '', photos: [] }
}
export async function addPhoto(file: File): Promise<string> {
  const bmp = await createImageBitmap(file); const max = 1024, r = Math.min(1, max / Math.max(bmp.width, bmp.height))
  const c = document.createElement('canvas'); c.width = Math.round(bmp.width * r); c.height = Math.round(bmp.height * r)
  c.getContext('2d')!.drawImage(bmp, 0, 0, c.width, c.height)
  const key = 'photo-' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6)
  await set(key, c.toDataURL('image/jpeg', 0.75)); return key
}
export const getPhoto = (k: string) => get<string>(k)
export const delPhoto = (k: string) => del(k)
/** local date string yyyy-mm-dd for the next occurrence of a weekday (today if dow null/matches) */
export function nextDate(dow: number | null) {
  const d = new Date(); if (dow != null) d.setDate(d.getDate() + ((dow - d.getDay() + 7) % 7))
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}
