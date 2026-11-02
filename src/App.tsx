import { useEffect, useMemo, useRef, useState } from 'react'
import { flushSync } from 'react-dom'
import { Item, items, MOODS, DISTRICTS, districtCount, inDistrict, isUncertain, fmt, fmtCount, mapsUrl, look, byRating, coupleRange, fmtRange, UNIT } from './data'
import { COMBOS, Combo, Plan, Prefs, PlanResult, Tier, TIER_LABEL, PARTS, DOW, RANGES, rangeOf, plan, districtFit, swapCandidates, relink, total, tierOf, remember } from './planner'
import { Entry, Meta, decodePlan, sharePlan, loadDiary, saveDiary, newEntry, entryPlan, addPhoto, getPhoto, delPhoto, nextDate, fmtDate, itemIdx } from './store'

function useFavs() {
  const [favs, setFavs] = useState<string[]>(() => { try { return JSON.parse(localStorage.getItem('favs') || '[]') } catch { return [] } })
  useEffect(() => localStorage.setItem('favs', JSON.stringify(favs)), [favs])
  const toggle = (id: string) => setFavs(f => f.includes(id) ? f.filter(x => x !== id) : [...f, id])
  return { favs, toggle }
}
type Favs = ReturnType<typeof useFavs>

const reduced = () => typeof matchMedia !== 'undefined' && matchMedia('(prefers-reduced-motion: reduce)').matches
/** Scroll-reveal: watches .card / [data-reveal] elements added under root; fades+rises them in once, staggered per batch. */
function useReveal(root: React.RefObject<HTMLElement>) {
  useEffect(() => {
    const el = root.current; if (!el || reduced() || !('IntersectionObserver' in window)) return
    const io = new IntersectionObserver(es => {
      let i = 0
      for (const e of es) if (e.isIntersecting) { const t = e.target as HTMLElement; t.style.transitionDelay = `${Math.min(i++, 6) * 60}ms`; t.classList.add('in'); io.unobserve(t) }
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 })
    const seen = new WeakSet<Element>()
    const scan = () => el.querySelectorAll('.card, [data-reveal]').forEach(c => { if (seen.has(c) || c.closest('.card') !== c && c.parentElement?.closest('.card')) return; seen.add(c); c.classList.add('rv'); io.observe(c) })
    scan(); const mo = new MutationObserver(scan); mo.observe(el, { childList: true, subtree: true })
    return () => { io.disconnect(); mo.disconnect() }
  }, [root])
}
/** Scroll direction + scrolled flag (rAF-throttled). */
function useScrollState() {
  const [st, setSt] = useState({ scrolled: false, hidden: false })
  useEffect(() => {
    let last = scrollY, tick = false
    const on = () => { if (tick) return; tick = true; requestAnimationFrame(() => { const y = scrollY, d = y - last; tick = false
      setSt(s => { const n = { scrolled: y > 8, hidden: Math.abs(d) < 6 ? s.hidden : d > 0 && y > 120 }; return n.scrolled === s.scrolled && n.hidden === s.hidden ? s : n })
      if (Math.abs(d) >= 6) last = y }) }
    addEventListener('scroll', on, { passive: true }); return () => removeEventListener('scroll', on)
  }, [])
  return st
}

function Chip({ on, onClick, children, mint }: { on: boolean; onClick: () => void; children: React.ReactNode; mint?: boolean }) {
  return <button type="button" aria-pressed={on} onClick={onClick} className={`chip ${on ? 'chip-on' : 'chip-off'} ${mint ? 'mint' : ''}`}>{children}</button>
}
const tog = (arr: string[], v: string) => arr.includes(v) ? arr.filter(x => x !== v) : [...arr, v]

const CONF: Record<string, [string, string]> = { high: ['✓ menu chính thức', 'text-mint-600'], medium: ['review/Maps', 'text-sky-600'], low: ['nguồn cũ/chưa chắc', 'text-amber-600'] }
function Price({ it }: { it: Item }) {
  const [lo, hi] = coupleRange(it)
  const per = it.price_min != null || it.price_max != null ? `${fmtRange(it.price_min ?? null, it.price_max ?? null)}${UNIT[it.price_unit ?? ''] ?? ''}` : ''
  const conf = it.price_confidence ? CONF[it.price_confidence] : null
  if (it.price_unit === 'free' || (lo === 0 && hi === 0)) return <span className="text-mint-700"><b>Miễn phí</b>{it.price_note ? ` · ${it.price_note}` : ''}</span>
  if (lo == null && hi == null) return <span className="text-amber-700"><b>Chưa rõ giá</b>{per && ` · ${per}`}{it.price_note ? ` · ${it.price_note}` : ''}</span>
  return <span className="inline-flex flex-wrap gap-x-1 max-w-full"><span className="text-mint-700 font-semibold">{fmtRange(lo, hi)}/2 người</span>
    {per && <span className="text-slate-600">({per})</span>}
    {conf && (it.price_source_url ? <a href={it.price_source_url} target="_blank" rel="noreferrer" className={`underline decoration-dotted ${conf[1]}`} title={`${it.price_note ?? ''} — kiểm tra ${it.price_checked ?? ''}`}>{conf[0]}</a> : <span className={conf[1]}>{conf[0]}</span>)}</span>
}
function Stars({ it }: { it: Item }) {
  if (it.rating == null) return <span className="text-[11px] text-slate-400">Chưa có đánh giá</span>
  const full = Math.round(it.rating)
  return <span className="text-xs inline-flex items-center gap-1" title={`${it.rating} / 5 trên Google Maps`}>
    <span className="text-amber-500 tracking-tighter">{'★'.repeat(full)}<span className="text-slate-300">{'★'.repeat(5 - full)}</span></span>
    <b>{it.rating.toLocaleString('vi-VN', { minimumFractionDigits: 1 })}</b>{it.reviews != null && <span className="text-slate-600">({fmtCount(it.reviews)} đánh giá)</span>}</span>
}
function Badges({ it }: { it: Item }) {
  return <>{isUncertain(it) && <span className="text-[11px] px-2 py-0.5 rounded-full bg-amber-100 text-amber-800">⚠️ cần kiểm tra lại</span>}
    {it.source === 'user' && <span className="text-[11px] px-2 py-0.5 rounded-full bg-mint-100 text-mint-700">💌 từ bạn</span>}
    {it.source === 'bliss_home' && <span className="text-[11px] px-2 py-0.5 rounded-full bg-blush-100 text-blush-700">💗 Bliss Home</span>}
    {it.source === 'social' && <span className="text-[11px] px-2 py-0.5 rounded-full bg-mint-100 text-mint-700">📱 TikTok/FB</span>}</>
}
function Links({ it }: { it: Item }) {
  return <div className="flex flex-wrap gap-2 text-xs">
    {it.type !== 'idea' && <a className="btn bg-mint-100 text-mint-800 !px-3 !py-1" href={mapsUrl(it)} target="_blank" rel="noreferrer">{it.maps_kind === 'direct' ? '📍 Mở Google Maps' : '🔎 Tìm trên Google Maps'}</a>}
    {it.source_urls?.map((u, i) => <a key={u} className="btn bg-slate-100 text-slate-600 !px-3 !py-1" href={u} target="_blank" rel="noreferrer">🔗 Nguồn {i + 1}</a>)}
  </div>
}
function Thumb({ it, h = 'h-28', credit = true }: { it: Item; h?: string; credit?: boolean }) {
  const l = look(it)
  if (!it.image) return <div className={`w-full ${h} rounded-2xl ${l.grad} grid place-items-center text-5xl`}>{l.emoji}</div>
  return <Img it={it} h={h} credit={credit} bg={l.grad} />
}
function Img({ it, h, credit, bg }: { it: Item; h: string; credit: boolean; bg: string }) {
  const logo = it.image_kind === 'logo'; const [ok, setOk] = useState(false); const ref = useRef<HTMLImageElement>(null)
  useEffect(() => { if (ref.current?.complete && ref.current.naturalWidth) setOk(true) }, [])
  return <div className={`relative w-full ${h} rounded-2xl overflow-hidden ${logo ? bg : ok ? 'bg-slate-100' : (it.id.length % 2 ? 'bg-blush-100' : 'bg-mint-100') + ' skeleton'}`}>
    <img ref={ref} onLoad={() => setOk(true)} src={it.image!.startsWith('/') ? import.meta.env.BASE_URL + it.image!.slice(1) : it.image} alt={it.name} loading="lazy" decoding="async" className={`img-fade ${ok ? 'opacity-100' : 'opacity-0'} ${logo ? 'w-full h-full object-contain p-2 mix-blend-multiply' : 'w-full h-full object-cover'}`} />
    {credit && it.image_credit && <a href={it.image_source_url} target="_blank" rel="noreferrer" className="absolute bottom-1 right-1 text-[9px] leading-none px-1.5 py-0.5 rounded bg-black/45 text-white">{it.image_credit}</a>}
  </div>
}
function Heart({ it, f }: { it: Item; f: Favs }) {
  const on = f.favs.includes(it.id)
  return <button aria-label="Yêu thích" onClick={() => f.toggle(it.id)} className={`text-xl transition ${on ? 'wiggle' : 'opacity-60 hover:opacity-100 hover:scale-110'}`}>{on ? '❤️' : '🤍'}</button>
}
function ItemCard({ it, f }: { it: Item; f: Favs }) {
  return <div className="card card-hover p-3 flex flex-col gap-2 min-w-0 [overflow-wrap:anywhere]">
    <Thumb it={it} />
    <div className="flex items-start justify-between gap-2"><h3 className="font-bold leading-snug">{it.name ?? 'Chưa rõ tên'}</h3><Heart it={it} f={f} /></div>
    <div className="flex flex-wrap gap-1 text-[11px]"><span className="sticker bg-mint-50 text-mint-800">{it.category}</span>
      {it.area && <span className="px-2 py-0.5 rounded-full bg-slate-100">{it.area}</span>}<Badges it={it} /></div>
    {it.type !== 'idea' && <Stars it={it} />}
    {it.address && <div className="text-xs text-slate-600">📍 {it.address}</div>}
    <p className="text-sm text-slate-600">{it.description_vi}</p>
    {it.type !== 'idea' && <div className="text-xs"><Price it={it} /></div>}
    {it.opening_hours && <div className="text-xs text-slate-600">🕒 {it.opening_hours}</div>}
    <div className="flex flex-wrap gap-1">{(it.mood_tags ?? []).map(m => <span key={m} className="text-[11px] text-mint-600">#{m}</span>)}</div>
    <div className="mt-auto"><Links it={it} /></div>
  </div>
}

const tierCls: Record<Tier, string> = { 0: 'bg-mint-100 text-mint-800', 1: 'bg-amber-100 text-amber-800', 2: 'bg-slate-100 text-slate-700', 3: 'bg-blush-100 text-blush-700' }
const roundUp = (v: number) => Math.ceil(v / 50000) * 50000
function useToast() { const [msg, setMsg] = useState(''); useEffect(() => { if (!msg) return; const t = setTimeout(() => setMsg(''), 2600); return () => clearTimeout(t) }, [msg]); return { msg, show: setMsg } }
function Toast({ msg }: { msg: string }) { return msg ? <div className="fixed z-50 left-1/2 -translate-x-1/2 bottom-24 sm:bottom-8 px-4 py-2 rounded-full bg-slate-900/90 text-white text-sm shadow-lg animate-pop">{msg}</div> : null }

function PlanCard({ pl, title, budget, min, f, onSwap, actions, delay = 0 }: { pl: Plan; title: string; budget?: number; min?: number; f: Favs; onSwap?: (si: number) => void; actions?: React.ReactNode; delay?: number }) {
  const t = total(pl); const tier = budget ? tierOf(pl.slots.map(s => s.item), budget) : null
  return <div className={`card p-5 sm:p-7 ${delay % 160 ? 'mint-shadow' : ''}`} style={{ animationDelay: `${delay}ms` }}>
    <div className="win-bar -mx-5 sm:-mx-7 -mt-5 sm:-mt-7 mb-5 px-5 sm:px-7 py-3 flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-blush-400" /><span className="w-2.5 h-2.5 rounded-full bg-mint-400" /><span className="w-2.5 h-2.5 rounded-full bg-slate-300" /><span className="ml-3 text-[11px] text-slate-600 truncate">hen-ho-sai-gon · {title}</span></div>
    <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
      <h3 className="font-semibold text-lg"><span className="eyebrow block mb-0.5">Kèo hẹn hò</span>{title}</h3>
      {tier != null && <span className={`text-[11px] font-semibold px-2.5 py-1 rounded-full ${tierCls[tier]}`}>{TIER_LABEL[tier]}</span>}</div>
    <div className="text-sm mb-3">💸 Ước tính: <b className={tier === 3 ? 'text-blush-600' : 'text-mint-700'}>{t.unknown === t.slots ? 'chưa rõ giá' : fmtRange(t.lo, t.hi)}</b>{t.unknown > 0 && t.unknown < t.slots && <span className="text-amber-700"> + {t.unknown} chỗ chưa rõ giá</span>}{budget ? <span className="text-slate-600"> / ngân sách {min != null ? rangeOf(budget, min).label : fmt(budget)}</span> : null}{budget && min != null && t.unknown === 0 && t.hi < min ? <span className="text-slate-600"> · rẻ hơn khoảng đã chọn</span> : null}</div>
    <ol className="relative border-l-2 border-solid border-blush-100 ml-2 space-y-4">
      {pl.slots.map((s, si) => <li key={si} className="pl-5 relative">
        <span className="absolute -left-[9px] top-1 w-4 h-4 rounded-full bg-white border-2 border-blush-500 ring-4 ring-white" />
        <div className="text-xs font-semibold text-blush-700 tabular-nums">{s.time} · {s.label}{si > 0 && <span className="font-normal text-slate-600"> · {s.km != null ? `cách điểm trước ~${s.km.toLocaleString('vi-VN', { maximumFractionDigits: 1 })} km` : (s.item.area === pl.slots[si - 1].item.area ? 'cùng quận' : 'quận kề bên')}</span>}</div>
        <div className="flex gap-3 mt-1"><div className="w-20 shrink-0"><Thumb it={s.item} h="h-20" credit={false} /></div>
          <div className="min-w-0 flex-1 space-y-1"><div className="flex justify-between gap-2"><b>{s.item.name}</b><Heart it={s.item} f={f} /></div>
            <div className="flex flex-wrap gap-1 text-[11px]">{s.item.area && <span className="px-2 py-0.5 rounded-full bg-slate-100">{s.item.area}</span>}<Badges it={s.item} />
              {s.closed === true && <span className="px-2 py-0.5 rounded-full bg-blush-100 text-blush-700">⏰ có thể đóng cửa lúc {s.time}</span>}
              {s.closed == null && s.item.type !== 'idea' && <span className="px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">🕒 chưa rõ giờ mở</span>}</div>
            <Stars it={s.item} />
            <div className="text-xs"><Price it={s.item} /></div>
            {s.item.opening_hours && <div className="text-xs text-slate-600">🕒 {s.item.opening_hours}</div>}
            <div className="flex flex-wrap gap-2 items-center">{onSwap && <button onClick={() => onSwap(si)} className="btn bg-mint-100 text-mint-700 !px-3 !py-1 text-xs">🔄 Đổi gợi ý</button>}<Links it={s.item} /></div></div></div>
      </li>)}</ol>
    {actions && <div className="flex flex-wrap gap-2 mt-4 pt-3 border-t border-blush-100">{actions}</div>}
  </div>
}
function PlanActions({ pl, meta, diary, toast }: { pl: Plan; meta: Meta; diary: Diary; toast: (m: string) => void }) {
  const saved = diary.has(pl)
  return <>
    <button className="btn btn-pop btn-primary" onClick={async () => { const r = await sharePlan(pl, meta); toast(r === 'copied' ? '📋 Đã chép kèo + link, dán gửi người ấy nhé!' : r === 'shared' ? '💌 Đã chia sẻ' : 'Không chia sẻ được 😢') }}>📤 Chia sẻ</button>
    <button disabled={saved} className={`btn ${saved ? 'bg-mint-100 text-mint-700' : 'bg-mint-100 text-mint-700'}`} onClick={() => { diary.add(pl, meta); toast('📔 Đã lưu kèo vào Nhật ký') }}>{saved ? '✓ Đã lưu' : '📌 Lưu kèo'}</button></>
}

function useDiary() {
  const [list, setList] = useState<Entry[]>(loadDiary)
  useEffect(() => saveDiary(list), [list])
  const sig = (pl: Plan) => pl.slots.map(s => itemIdx(s.item)).join('.')
  return {
    list, has: (pl: Plan) => list.some(e => e.s.split('~').map(x => x.split('.')[0]).join('.') === sig(pl)),
    add: (pl: Plan, m: Meta) => setList(l => [newEntry(pl, m), ...l]),
    update: (id: string, patch: Partial<Entry>) => setList(l => l.map(e => e.id === id ? { ...e, ...patch } : e)),
    remove: (id: string) => setList(l => { l.find(e => e.id === id)?.photos.forEach(delPhoto); return l.filter(e => e.id !== id) }),
  }
}
type Diary = ReturnType<typeof useDiary>

function Planner({ f, diary, toast }: { f: Favs; diary: Diary; toast: (m: string) => void }) {
  const [p, setP] = useState<Prefs>({ budget: 500000, min: 400000, districts: [], combo: 'cafe', moods: [], part: 'toi', dow: null, long: false })
  const [res, setRes] = useState<(PlanResult & { p: Prefs }) | null>(null)
  const run = (q: Prefs) => { setP(q); setRes({ ...plan(q), p: q }) }
  const counts = useMemo(() => Object.fromEntries(DISTRICTS.map(d => [d, districtFit(p, d)])), [p.combo, p.part, p.dow, p.long])
  const swap = (pi: number, si: number) => setRes(r => {
    if (!r) return r
    const used = new Set(r.plans.flatMap(pl => pl.slots.map(s => s.item.id)))
    const c = swapCandidates(r.plans[pi], si, r.p, used); if (!c.length) { toast('Hết lựa chọn phù hợp gần đó rồi 😅'); return r }
    const pick = c[Math.floor(Math.random() * Math.min(6, c.length))]; remember([pick.id])
    return { ...r, plans: r.plans.map((pl, i) => i !== pi ? pl : relink({ ...pl, slots: pl.slots.map((s, j) => j === si ? { ...s, item: pick } : s) }, r.p)) }
  })
  const meta = (q: Prefs): Meta => ({ combo: q.combo, budget: q.budget, min: q.min, date: nextDate(q.dow ?? null) })
  const rl = (q: Prefs) => q.min != null ? rangeOf(q.budget, q.min).label : fmt(q.budget)
  const today = new Date().getDay()
  return <div id="planner" className="scroll-mt-20 grid grid-cols-[minmax(0,1fr)] lg:grid-cols-[minmax(340px,400px)_minmax(0,1fr)] gap-6 lg:gap-8">
    <section className="card p-6 space-y-7 h-fit lg:sticky lg:top-24">
      <div data-testid="ranges"><h2 className="font-semibold text-[15px] mb-2.5">💸 Ngân sách (cho 2 người, tối đa 1tr/buổi)</h2>
        <div className="grid grid-cols-3 gap-1.5 sm:gap-2 [&>button]:!px-1 [&>button]:max-[379px]:!text-[12px]">{RANGES.map(r => <Chip key={r.id} on={p.budget === r.max && p.min === r.min} onClick={() => setP({ ...p, budget: r.max, min: r.min })}>{r.label}</Chip>)}</div>
        <p className="text-xs text-slate-600 mt-1">Ưu tiên kèo có tổng giá <b>nằm trong khoảng</b> đã chọn — khoảng cao hơn sẽ gợi ý chỗ xịn hơn.</p></div>
      <div><h2 className="font-semibold text-[15px] mb-2.5">🕒 Khi nào?</h2>
        <div className="flex flex-wrap gap-2">{PARTS.map(x => <Chip key={x.id} on={p.part === x.id} onClick={() => setP({ ...p, part: x.id })}>{x.label}</Chip>)}</div>
        <div className="flex flex-wrap gap-1.5 mt-2">{[null, 1, 2, 3, 4, 5, 6, 0].map(d => <Chip key={String(d)} on={p.dow === d} onClick={() => setP({ ...p, dow: d })}>{d == null ? 'Ngày bất kỳ' : DOW[d] + (d === today ? ' (nay)' : '')}</Chip>)}</div>
        <label className="mt-3 flex items-center gap-2 text-sm cursor-pointer"><input type="checkbox" className="accent-blush-500 w-4 h-4" checked={!!p.long} onChange={e => setP({ ...p, long: e.target.checked })} /><span><b>Buổi dài</b> · 3 điểm (vd. photobooth → ăn tối → cafe)</span></label></div>
      <div><h2 className="font-semibold text-[15px] mb-2.5">✨ Combo</h2>
        <div className="flex flex-wrap gap-2">{COMBOS.map(c => <Chip key={c.id} on={p.combo === c.id} onClick={() => setP({ ...p, combo: c.id as Combo, part: c.part ?? p.part })}>{c.label}</Chip>)}</div></div>
      <div><h2 className="font-semibold text-[15px] mb-2.5">📍 Khu vực</h2>
        <div className="flex flex-wrap gap-2">{DISTRICTS.map(d => <Chip mint key={d} on={p.districts.includes(d)} onClick={() => setP({ ...p, districts: tog(p.districts, d) })}>{d} <span className={counts[d] ? 'opacity-60' : 'opacity-40 line-through'}>{counts[d]}</span></Chip>)}</div>
        <p className="text-xs text-slate-600 mt-1">Số bên cạnh = chỗ hợp điểm đầu của combo vào giờ đã chọn. Các điểm liền nhau luôn cùng quận hoặc quận kề.</p></div>
      <div><h2 className="font-semibold text-[15px] mb-2.5">💗 Mood</h2>
        <div className="flex flex-wrap gap-2">{MOODS.map(m => <Chip mint key={m} on={p.moods.includes(m)} onClick={() => setP({ ...p, moods: tog(p.moods, m) })}>{m}</Chip>)}</div></div>
      <button onClick={() => run(p)} className="btn btn-pop btn-primary w-full !py-3 text-base">Lên kèo hẹn hò 💞</button>
    </section>
    <section className="space-y-4" id="results">
      {!res && <div className="card p-10 text-center text-slate-600"><div className="eyebrow mb-3">Bắt đầu</div><div className="text-5xl mb-4">💌</div>Chọn ngân sách, giờ, combo rồi bấm <b>Lên kèo</b> nhé!</div>}
      {res && res.empty && <div className="card p-5 space-y-3 border-amber-200 animate-pop" data-testid="empty">
        <div className="text-3xl">🧭</div>
        <p><b>{res.empty.district.join(', ')}</b> hiện chỉ có <b>{res.empty.count}</b> địa điểm phù hợp cho chặng “{res.empty.slot}” vào giờ này, nên chưa ghép được kèo.</p>
        {res.empty.neighbourCount > res.empty.count && <button className="btn btn-pop btn-primary" onClick={() => run({ ...res.p, districts: res.empty!.neighbours })}>🗺️ Mở rộng sang quận lân cận ({res.empty.neighbourCount} chỗ)</button>}
        <button className="btn bg-slate-100 ml-2" onClick={() => run({ ...res.p, districts: [] })}>Mọi khu trung tâm</button></div>}
      {res && !res.plans.length && !res.empty && <div className="card p-5 space-y-2" data-testid="empty"><div className="text-3xl">🌙</div><p>Giờ này hầu hết chỗ cho combo này đã đóng cửa hoặc chưa mở. Thử buổi khác nhé!</p>
        <div className="flex flex-wrap gap-2">{PARTS.filter(x => x.id !== res.p.part).map(x => <button key={x.id} className="btn bg-mint-100 text-mint-700" onClick={() => run({ ...res.p, part: x.id })}>{x.label}</button>)}</div></div>}
      {res && res.best != null && res.best > 0 && <div className="card p-4 space-y-2 bg-amber-50/80 animate-pop" data-testid="budget-hint">
        <p className="text-sm">💡 Với <b>{rl(res.p)}</b>, {COMBOS.find(c => c.id === res.p.combo)?.label} {res.best === 3 ? 'đang vượt ngân sách' : 'chưa có kèo chắc chắn vừa túi'}{res.best === 1 ? ' — dưới đây là kèo vừa túi nếu gọi món tiết kiệm' : res.best === 2 ? ' — dưới đây có điểm chưa rõ giá, hỏi giá trước nhé' : ''}.
          {res.minSure && <> Cần khoảng <b>{fmt(res.minSure)}</b> để chắc chắn đủ.</>}</p>
        <div className="flex flex-wrap gap-2">{res.minSure && res.minSure <= 1e6 && (() => { const r = rangeOf(roundUp(res.minSure!)); return <button className="btn bg-white border border-amber-200" onClick={() => run({ ...res.p, budget: r.max, min: r.min })}>Dùng khoảng {r.label}</button> })()}
          {res.altCombos.slice(0, 4).map(c => <button key={c} className="btn bg-white border border-blush-200" onClick={() => run({ ...res.p, combo: c })}>Thử {COMBOS.find(x => x.id === c)?.label} (vừa {rl(res.p)})</button>)}</div></div>}
      {res?.plans.map((pl, pi) => <PlanCard key={pi} pl={pl} title={`Kế hoạch ${pi + 1}${pl.slots.length > 2 ? ' · Buổi dài' : ''}`} budget={res.p.budget} min={res.p.min} f={f} delay={pi * 80} onSwap={si => swap(pi, si)}
        actions={<PlanActions pl={pl} meta={meta(res.p)} diary={diary} toast={toast} />} />)}
      {res && res.plans.length > 0 && <p className="text-xs text-slate-600">✅ chắc chắn = tổng giá cao nhất ≤ mức trên của khoảng · 🟡 có thể = tổng giá thấp nhất ≤ mức trên của khoảng. Giá ước tính cho 2 người từ nguồn công khai (kiểm tra 26/10/2026), có thể đã đổi. Giờ mở cửa: chỗ đã biết giờ luôn được kiểm tra; chỗ “chưa rõ giờ” nên gọi trước.</p>}
    </section></div>
}

function SharedPlan({ data, f, diary, toast, onClose }: { data: { plan: Plan; meta: Meta }; f: Favs; diary: Diary; toast: (m: string) => void; onClose: () => void }) {
  return <div className="space-y-3 mb-6"><div className="flex items-center justify-between"><h2 className="font-bold">💌 Kèo được chia sẻ {data.meta.date && <span className="font-normal text-slate-600">· {fmtDate(data.meta.date)}</span>}</h2><button className="btn bg-slate-100" onClick={onClose}>Đóng</button></div>
    <PlanCard pl={relink(data.plan)} title="Kèo của tụi mình" budget={data.meta.budget} min={data.meta.min} f={f} actions={<PlanActions pl={data.plan} meta={data.meta} diary={diary} toast={toast} />} /></div>
}

function Photo({ k, onDel }: { k: string; onDel: () => void }) {
  const [src, setSrc] = useState<string>(); useEffect(() => { getPhoto(k).then(setSrc) }, [k])
  return <div className="relative w-24 h-24 rounded-xl overflow-hidden bg-slate-100">{src && <img src={src} className="w-full h-full object-cover" alt="" />}
    <button onClick={onDel} aria-label="Xoá ảnh" className="absolute top-1 right-1 w-6 h-6 rounded-full bg-black/50 text-white text-xs">✕</button></div>
}
function DiaryEntry({ e, diary, f, toast }: { e: Entry; diary: Diary; f: Favs; toast: (m: string) => void }) {
  const pl = entryPlan(e); const [open, setOpen] = useState(false); const [busy, setBusy] = useState(false)
  if (!pl) return null
  const t = total(pl)
  return <div className={`card p-4 space-y-3 ${e.done ? 'ring-2 ring-mint-200' : ''}`}>
    <div className="flex items-start justify-between gap-2"><div><div className="text-xs text-slate-600">{e.done ? '💖 Đã đi' : '📌 Sắp đi'} · <input type="date" value={e.date} onChange={x => diary.update(e.id, { date: x.target.value })} className="bg-transparent underline decoration-dotted" /></div>
      <h3 className="font-bold">{pl.slots.map(s => s.item.name).join(' → ')}</h3>
      <div className="text-xs text-slate-600">{pl.slots.map(s => s.time).join(' · ')} · 💸 {t.unknown === t.slots ? 'chưa rõ giá' : fmtRange(t.lo, t.hi)}</div></div>
      <button onClick={() => diary.update(e.id, { done: !e.done })} className={`btn shrink-0 ${e.done ? 'bg-mint-500 text-white' : 'bg-mint-50 text-mint-700 border border-mint-200'}`}>{e.done ? '✓ Đã đi' : 'Đánh dấu đã đi'}</button></div>
    <textarea value={e.note} onChange={x => diary.update(e.id, { note: x.target.value.slice(0, 280) })} rows={2} placeholder="Ghi chú ngắn: hôm đó thế nào? 💭" className="w-full rounded-2xl border border-blush-100 bg-white/70 p-3 text-sm outline-none focus:ring-2 ring-blush-200" />
    <div className="flex flex-wrap gap-2 items-center">{e.photos.map(k => <Photo key={k} k={k} onDel={() => { delPhoto(k); diary.update(e.id, { photos: e.photos.filter(x => x !== k) }) }} />)}
      <label className="w-24 h-24 rounded-xl border-2 border-dashed border-blush-200 grid place-items-center text-xs text-blush-500 cursor-pointer text-center">{busy ? 'Đang lưu…' : <>📷<br />Thêm ảnh</>}
        <input type="file" accept="image/*" multiple className="hidden" onChange={async x => { const fs = [...(x.target.files ?? [])]; if (!fs.length) return; setBusy(true); try { const ks = await Promise.all(fs.slice(0, 6).map(addPhoto)); diary.update(e.id, { photos: [...e.photos, ...ks] }) } catch { toast('Không lưu được ảnh 😢') } setBusy(false); x.target.value = '' }} /></label></div>
    <div className="flex flex-wrap gap-2 text-xs"><button className="btn bg-slate-100 !py-1" onClick={() => setOpen(!open)}>{open ? 'Thu gọn' : 'Xem chi tiết'}</button>
      <button className="btn bg-mint-100 text-mint-700 !py-1" onClick={async () => { const r = await sharePlan(pl, { combo: e.combo, budget: e.budget, min: e.min, date: e.date }); if (r === 'copied') toast('📋 Đã chép kèo + link') }}>📤 Chia sẻ</button>
      <button className="btn bg-blush-50 text-blush-600 !py-1 ml-auto" onClick={() => { if (confirm('Xoá kèo này khỏi nhật ký?')) diary.remove(e.id) }}>Xoá</button></div>
    {open && <PlanCard pl={relink(pl)} title="Chi tiết kèo" budget={e.budget} min={e.min} f={f} />}
  </div>
}
function Mine({ f, diary, toast }: { f: Favs; diary: Diary; toast: (m: string) => void }) {
  const [view, setView] = useState<'diary' | 'fav'>('diary')
  const up = diary.list.filter(e => !e.done).sort((a, b) => a.date.localeCompare(b.date)), done = diary.list.filter(e => e.done).sort((a, b) => b.date.localeCompare(a.date))
  return <div className="space-y-4">
    <div className="flex gap-2"><Chip on={view === 'diary'} onClick={() => setView('diary')}>📔 Nhật ký ({diary.list.length})</Chip><Chip on={view === 'fav'} onClick={() => setView('fav')}>❤️ Yêu thích ({f.favs.length})</Chip></div>
    {view === 'fav' ? <Browse f={f} onlyFavs /> : <>
      {!diary.list.length && <div className="card p-8 text-center text-slate-600"><div className="text-5xl mb-2">📔</div>Chưa có kèo nào. Lên kèo rồi bấm <b>📌 Lưu kèo</b> để lưu lại nhé!</div>}
      {up.length > 0 && <><h2 className="font-bold">📌 Sắp tới</h2><div className="grid grid-cols-[minmax(0,1fr)] lg:grid-cols-2 gap-4">{up.map(e => <DiaryEntry key={e.id} e={e} diary={diary} f={f} toast={toast} />)}</div></>}
      {done.length > 0 && <><h2 className="font-bold">💖 Kỷ niệm đã đi</h2><div className="grid grid-cols-[minmax(0,1fr)] lg:grid-cols-2 gap-4">{done.map(e => <DiaryEntry key={e.id} e={e} diary={diary} f={f} toast={toast} />)}</div></>}
      <p className="text-xs text-slate-600">Nhật ký và ảnh chỉ lưu trên máy này (localStorage + IndexedDB), không gửi đi đâu.</p></>}
  </div>
}

const COST = [['free', '🆓 Miễn phí', (v: number) => v === 0], ['lt200', '💵 Dưới 200k', (v: number) => v > 0 && v < 2e5], ['gt200', '💎 Trên 200k', (v: number) => v >= 2e5]] as const
function AtHome({ f }: { f: Favs }) {
  const all = useMemo(() => items.filter(i => i.type === 'idea'), [])
  const [moods, setMoods] = useState<string[]>([]); const [cost, setCost] = useState(''); const [pick, setPick] = useState<Item | null>(null)
  const costOf = (i: Item) => { const r = coupleRange(i); return i.price_unit === 'free' ? 0 : r[1] ?? r[0] }
  const hasCost = all.some(i => costOf(i) != null)
  const list = all.filter(i => (!moods.length || i.mood_tags.some(m => moods.includes(m))) && (!cost || (() => { const v = costOf(i); const c = COST.find(x => x[0] === cost)!; return v != null && c[2](v) })()))
  const moodsAvail = MOODS.filter(m => all.some(i => i.mood_tags.includes(m)))
  return <div className="space-y-4">
    <div><h2 className="text-xl font-bold">🏠 Date tại nhà / sáng tạo</h2><p className="text-sm text-slate-600">Không cần ra đường vẫn ngọt ngào</p></div>
    <div className="card p-4 space-y-3">
      <div className="flex flex-wrap gap-2">{moodsAvail.map(m => <Chip key={m} on={moods.includes(m)} onClick={() => setMoods(tog(moods, m))}>#{m} <span className="opacity-50">{all.filter(i => i.mood_tags.includes(m)).length}</span></Chip>)}</div>
      {hasCost ? <div className="flex flex-wrap gap-2">{COST.map(([id, l]) => <Chip key={id} on={cost === id} onClick={() => setCost(cost === id ? '' : id)}>{l}</Chip>)}</div>
        : <p className="text-xs text-slate-600">Các ý tưởng tại nhà chưa có dữ liệu chi phí nên chỉ lọc theo mood (đa số gần như miễn phí).</p>}
      <button className="btn btn-pop btn-primary w-full sm:w-auto" onClick={() => { const src = list.length ? list : all; let x = src[Math.floor(Math.random() * src.length)]; if (src.length > 1) while (x === pick) x = src[Math.floor(Math.random() * src.length)]; setPick(x) }}>🎲 Gợi ý ngẫu nhiên</button></div>
    {pick && <div className="card p-4 ring-2 ring-blush-300 animate-pop"><div className="text-xs font-bold text-blush-600 mb-2">✨ Tối nay thử cái này nha</div><div className="max-w-sm"><ItemCard it={pick} f={f} /></div></div>}
    <p className="text-sm text-slate-600">{list.length} ý tưởng</p>
    <div className="grid grid-cols-[minmax(0,1fr)] md:grid-cols-2 xl:grid-cols-3 gap-4 lg:gap-5">{list.map(i => <ItemCard key={i.id} it={i} f={f} />)}</div>
  </div>
}

const fold = (t: unknown) => String(t ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'd').toLowerCase()
const hay = new Map<string, { name: string; all: string }>()
const haystack = (i: Item): { name: string; all: string } => { let h = hay.get(i.id); if (!h) { h = { name: fold(i.name), all: fold([i.name, i.address, i.district, i.area, i.category, i.google_category, i.description_vi, ...(i.mood_tags || [])].filter(Boolean).join(' ')) }; hay.set(i.id, h) } return h }
const KIND_LABEL: Record<string, string> = { restaurant: 'Nhà hàng', cafe: 'Cà phê', photobooth: 'Photobooth / studio ảnh', workshop: 'Workshop', sight: 'Tham quan', game: 'Game / giải trí', bar: 'Bar / pub', shopping: 'Mua sắm', spa: 'Spa / massage', homestay: 'Homestay / khách sạn', show: 'Show / kịch', experience: 'Trải nghiệm', streetfood: 'Ăn vặt / đường phố', cinema: 'Rạp phim', dessert: 'Tráng miệng', other: 'Khác' }
const kindLabel = (k: string) => KIND_LABEL[k] ?? k
function Browse({ f, onlyFavs }: { f: Favs; onlyFavs?: boolean }) {
  const [q, setQ] = useState('')
  const [type, setType] = useState(''); const [cat, setCat] = useState(''); const [ds, setDs] = useState<string[]>([]); const [moods, setMoods] = useState<string[]>([])
  const base = useMemo(() => items.filter(i => !i.out_of_area && i.type !== 'idea').sort(byRating), [])
  const cats = useMemo(() => [...new Set(base.filter(i => !type || i.type === type).map(i => i.kind || 'other'))].sort((a, b) => kindLabel(a).localeCompare(kindLabel(b), 'vi')), [type, base])
  const filtered = (onlyFavs ? items.filter(i => f.favs.includes(i.id)) : base.filter(i => (!type || i.type === type) && (!cat || (i.kind || 'other') === cat) && inDistrict(i, ds) && (!moods.length || (i.mood_tags ?? []).some(m => moods.includes(m)))))
  const words = fold(q.trim()).split(/\s+/).filter(Boolean)
  const list = !words.length ? filtered : filtered.filter(i => { const h = haystack(i); return words.every(w => h.all.includes(w)) })
    .map(i => { const h = haystack(i); const w = words.join(' '); return [i, h.name.startsWith(w) ? 0 : h.name.includes(w) ? 1 : words.every(x => h.name.includes(x)) ? 2 : 3] as const })
    .sort((a, b) => a[1] - b[1]).map(x => x[0])
  return <div className="space-y-4">
    {!onlyFavs && <div className="card p-4 space-y-3">
      <div className="relative"><span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">🔍</span>
        <input type="text" inputMode="search" enterKeyHint="search" value={q} onChange={e => setQ(e.target.value)} placeholder="Tìm quán, địa chỉ, quận, mood… (vd: lau, bui vien, rooftop)" aria-label="Tìm địa điểm"
          className="w-full rounded-full border border-slate-200 bg-white pl-10 pr-10 py-3 outline-none focus:border-blush-300 focus:ring-4 focus:ring-blush-100 transition" />
        {q && <button onClick={() => setQ('')} aria-label="Xóa tìm kiếm" className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">✕</button>}</div>
      <div className="flex flex-wrap gap-2">{[['', 'Tất cả'], ['food', '🍽️ Ăn uống'], ['activity', '🎡 Đi chơi']].map(([v, l]) => <Chip key={v} on={type === v} onClick={() => { setType(v); setCat('') }}>{l}</Chip>)}
        <select value={cat} onChange={e => setCat(e.target.value)} className="chip chip-off"><option value="">Mọi loại hình</option>{cats.map(c => <option key={c} value={c}>{kindLabel(c)}</option>)}</select></div>
      <div className="flex flex-wrap gap-2">{DISTRICTS.map(d => <Chip mint key={d} on={ds.includes(d)} onClick={() => setDs(tog(ds, d))}>{d} <span className="opacity-50">{districtCount(d)}</span></Chip>)}</div>
      <div className="flex flex-wrap gap-2">{MOODS.map(m => <Chip mint key={m} on={moods.includes(m)} onClick={() => setMoods(tog(moods, m))}>#{m}</Chip>)}</div>
    </div>}
    <p className="text-sm text-slate-600">{list.length} địa điểm · {words.length ? `kết quả cho “${q.trim()}”` : "sắp xếp theo đánh giá (★ có tính số lượt review)"}</p>
    {!onlyFavs && words.length > 0 && !list.length && <div className="card p-8 text-center text-slate-600">Không tìm thấy “{q.trim()}”. Thử bỏ bớt bộ lọc quận/mood hoặc gõ ngắn hơn nhé.</div>}
    {onlyFavs && !list.length && <div className="card p-8 text-center text-slate-600">Chưa có mục yêu thích nào. Bấm 🤍 để lưu nhé!</div>}
    <CardGrid list={list} f={f} reset={`${q}|${type}|${cat}|${ds.join()}|${moods.join()}`} />
  </div>
}
const PAGE = 24
/** Renders cards incrementally (PAGE at a time) — rendering all ~400 frosted cards at once exhausted GPU memory on phones (tab crash). */
function CardGrid({ list, f, reset }: { list: Item[]; f: Favs; reset?: string }) {
  const [n, setN] = useState(PAGE); const more = useRef<HTMLButtonElement>(null)
  useEffect(() => setN(PAGE), [reset])
  useEffect(() => {
    const el = more.current; if (!el || !('IntersectionObserver' in window)) return
    const io = new IntersectionObserver(es => { if (es.some(e => e.isIntersecting)) setN(x => x + PAGE) }, { rootMargin: '600px 0px' })
    io.observe(el); return () => io.disconnect()
  }, [n, list.length])
  return <>
    <div className="grid grid-cols-[minmax(0,1fr)] md:grid-cols-2 xl:grid-cols-3 gap-4 lg:gap-5">{list.slice(0, n).map(i => <ItemCard key={i.id} it={i} f={f} />)}</div>
    {n < list.length && <div className="text-center"><button ref={more} type="button" onClick={() => setN(x => x + PAGE)} className="btn bg-white border border-blush-200 text-blush-700">Xem thêm ({list.length - n} địa điểm)</button></div>}
  </>
}
function Section({ title, sub, list, f }: { title: string; sub: string; list: Item[]; f: Favs }) {
  return <div className="space-y-4"><div><h2 className="text-xl font-bold">{title}</h2><p className="text-sm text-slate-600">{sub}</p></div>
    <CardGrid list={list} f={f} /></div>
}

/** DSH-style soft cloud background: a few solid-colour blobs, blurred via CSS filter (solid fills only). */
function Clouds() {
  return <div aria-hidden className="clouds">
    <span className="blob b1" /><span className="blob b2" /><span className="blob b3" />
    <span className="blob b4" /><span className="blob b5 hidden lg:block" />
  </div>
}
const TABS = [['plan', '💞', 'Lên kèo'], ['browse', '🗺️', 'Khám phá'], ['trip', '🏕️', 'Đi xa'], ['mine', '📔', 'Nhật ký']] as const
export default function App() {
  const f = useFavs(); const diary = useDiary(); const { msg, show } = useToast()
  const [tab, setTab] = useState<string>('plan')
  const [shared, setShared] = useState(() => decodePlan(location.hash))
  useEffect(() => { const h = () => { const d = decodePlan(location.hash); if (d) { setShared(d); setTab('plan') } }; addEventListener('hashchange', h); return () => removeEventListener('hashchange', h) }, [])
  const mainRef = useRef<HTMLElement>(null); useReveal(mainRef); const sc = useScrollState()
  const go = (id: string) => { if (id === tab) return; const run = () => { flushSync(() => setTab(id)); window.scrollTo(0, 0) }
    const d = document as Document & { startViewTransition?: (cb: () => void) => unknown }
    if (d.startViewTransition && !reduced()) d.startViewTransition(run); else run() }
  return <div className="pb-24 sm:pb-8 relative isolate"><Clouds />
    <header className={`sticky top-0 z-20 transition-[background-color,border-color,box-shadow] duration-300 border-b ${sc.scrolled ? 'bg-white/65 backdrop-blur-xl border-white/70 shadow-[0_1px_12px_-6px_rgba(30,35,44,.12)]' : 'bg-transparent border-transparent'}`}>
      <div className={`max-w-6xl mx-auto px-5 flex transition-[padding] duration-300 ${sc.scrolled ? 'py-2' : 'py-3 sm:py-4'} items-center justify-between gap-4`}>
        <h1 className="font-semibold text-lg tracking-tight flex items-center gap-2"><span className="w-2 h-2 rounded-full bg-blush-500" /><span>Hẹn Hò <span className="text-mint-700">Sài Gòn</span></span></h1>
        <nav className="hidden sm:flex gap-1 p-1 rounded-full bg-white/40 backdrop-blur-md border border-white/70">{TABS.map(([id, e, l]) => <Chip key={id} on={tab === id} onClick={() => go(id)}>{e} {l}{id === 'mine' && diary.list.length ? ` (${diary.list.length})` : ''}</Chip>)}</nav>
      </div></header>
    <main ref={mainRef} className="max-w-6xl mx-auto px-5 py-8 sm:py-12"><div key={tab} className="tab-in">
      {tab === 'plan' && <>{shared && <SharedPlan data={shared} f={f} diary={diary} toast={show} onClose={() => { setShared(null); history.replaceState(null, '', location.pathname) }} />}
        <section className="text-center pt-6 pb-10 sm:pt-14 sm:pb-16 max-w-3xl mx-auto">
          <div className="eyebrow mb-5 inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/50 backdrop-blur border border-white/70">✦ Lên kèo tối nay</div>
          <h2 className="text-[34px] leading-[1.15] sm:text-5xl sm:leading-[1.12] font-medium tracking-tight"><span className="text-blush-700">Hẹn hò</span> <span className="text-mint-800">Sài Gòn</span></h2>
          <p className="mt-5 text-[15px] sm:text-base text-slate-600 max-w-xl mx-auto leading-relaxed">Tối nay đi đâu? Chọn ngân sách, giờ và combo — mình ghép kèo 2–3 điểm gần nhau ở trung tâm Sài Gòn cho hai bạn ✨</p>
          <button type="button" onClick={() => document.getElementById('planner')?.scrollIntoView({ block: 'start' })} className="btn mt-7 bg-white text-[var(--ink)] !px-5 !py-2.5 shadow-[0_1px_3px_rgba(0,0,0,.08)] hover:shadow-[0_6px_20px_-8px_rgba(179,54,79,.45)] border border-white">💞 Bắt đầu lên kèo</button>
        </section><Planner f={f} diary={diary} toast={show} /></>}
      {tab === 'browse' && <Browse f={f} />}
      {/* TODO: bật lại tab Tại nhà sau — {tab === 'ideas' && <AtHome f={f} />} */}
      {tab === 'trip' && <Section f={f} title="🏕️ Chuyến đi xa" sub="Ngoài khu trung tâm — không nằm trong gợi ý tối nay" list={items.filter(i => i.out_of_area)} />}
      {tab === 'mine' && <Mine f={f} diary={diary} toast={show} />}
    </div></main>
    <Toast msg={msg} />
    <nav aria-label="Điều hướng" className={`sm:hidden fixed bottom-0 inset-x-0 z-20 transition-transform duration-300 ${sc.hidden ? 'translate-y-full' : ''}`}><div className="bg-white/70 backdrop-blur-xl border-t border-[rgba(30,35,44,.08)] grid grid-cols-4 gap-1 px-2 pt-1.5 pb-[max(.375rem,env(safe-area-inset-bottom))]">
      {TABS.map(([id, e, l]) => <button key={id} onClick={() => go(id)} className={`py-1.5 flex flex-col items-center text-[11px] rounded-2xl transition-all active:scale-90 ${tab === id ? 'bg-mint-50 text-mint-800 font-semibold' : 'text-slate-600'}`}><span className={`text-xl transition ${tab === id ? 'scale-110' : ''}`}>{e}</span>{l}</button>)}
    </div></nav></div>
}
