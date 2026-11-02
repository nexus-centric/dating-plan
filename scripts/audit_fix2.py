#!/usr/bin/env python3
"""Audit pass 2 (2026-10-31): applies on top of audit_fix.py. Uses tmp/audit_maps.json (from scripts/audit_maps.cjs:
live Google Maps page per place) + targeted web checks. Updates src/data.json and /workspace/date-app-audit.csv.
Run: python3 scripts/audit_fix.py && node scripts/audit_maps.cjs (until cached) && python3 scripts/audit_fix2.py"""
import json, csv, re, os, unicodedata
from urllib.parse import quote
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, CSV, MAPS = f'{ROOT}/src/data.json', '/workspace/date-app-audit.csv', f'{ROOT}/tmp/audit_maps.json'
d = json.load(open(SRC)); m = json.load(open(MAPS)); DATE = '2026-10-31'
prev = {int(r['id']): r for r in csv.DictReader(open(CSV))}
AUTO = 'automated checks passed'
rows = {}
def log(i, issue, action, url): rows[i] = (issue, action, url)
def hide(i, reason, url): d[i].update(status='hidden', hidden_reason=reason, date_checked=DATE); log(i, reason, 'hidden', url)
search = lambda q: 'https://www.google.com/maps/search/?api=1&query=' + quote(q)

# Google Maps shows "Tạm thời đóng cửa" (re-checked by hand on the place page 2026-10-31)
for i in (15, 124, 126, 168, 234, 264, 278, 428):
    hide(i, 'Google Maps place page shows "Tạm thời đóng cửa" (temporarily closed) on 2026-10-31', m[str(i)]['url'])
# Maps link pointed to another business
d[3]['maps_url'] = search('Momento Rooftop Bar 105 Cô Giang Quận 1'); d[3]['maps_kind'] = 'search'
log(3, 'Maps cid resolved to "Mít Cocktail Bar" (30 Ngô Đức Kế); official site lists Momento at 8F 105 Cô Giang -> Maps link replaced', 'fixed', 'https://momentorooftop.com/happy-hour-momento-rooftop/')
d[419]['maps_url'] = search('Yuna Alaska Coffee Nguyễn Gia Trí Bình Thạnh'); d[419]['status'] = 'uncertain'
log(419, 'Maps search resolved to a different pet cafe; Google Maps cannot find Yuna at 58 Nguyễn Gia Trí (Foody listing only)', 'unverified', 'https://www.foody.vn/ho-chi-minh/yuna-alaska-coffee')
d[67]['status'] = 'uncertain'
log(67, '856 Sư Vạn Hạnh now shows "La Sams" café on Google Maps; PhotoYoyo only in 2025 listicles', 'unverified', 'https://hcm.inhat.vn/photobooth-quan-10/')
for i in (100, 101):
    log(i, 'Tour (no fixed venue); Maps link is a city-level search, operator/price not re-confirmed', 'unverified', (d[i].get('source_urls') or [''])[0])
# categories: Bliss list labels ("Fine Dining date", "Check-in date"...) were used as category -> use Google Maps category
for i, x in enumerate(d):
    r = m.get(str(i))
    if r and (x.get('category') or '').endswith(' date') and r.get('category'):
        old = x['category']; x['category'] = r['category'][0].lower() + r['category'][1:]
        note = f'category "{old}" (list label) -> "{x["category"]}" (Google Maps)'
        pv = prev.get(i, {})
        if i in rows: continue
        if pv.get('action') in ('unverified', 'hidden') or (pv.get('action') == 'fixed'): log(i, pv['issue'] + '; ' + note, pv['action'], pv['source_url'])
        else: log(i, note, 'fixed', r['url'])
d[290]['category'] = 'nhà hàng Ý (mì Ý, salad)'
log(290, 'category "Fine Dining date" wrong: Google Maps = Nhà hàng Phương Tây; name says mì Ý/salad', 'fixed', m['290']['url'])
d[24]['kind'] = 'restaurant'; log(24, 'kind was cafe; it is a steakhouse/grill (Maps: Cửa hàng thịt + grill)', 'fixed', m['24']['url'])
d[275]['kind'] = 'bar'; log(275, 'kind was cafe for a cocktail bar', 'fixed', m['275']['url'])
log(397, 'Google Maps re-check 2026-10-31: Landmark 81, open (Đang mở cửa), 720A Điện Biên Phủ', 'ok', 'https://www.google.com/maps/place/Landmark+81/')
# photo spot-check
for k in ('image', 'image_credit', 'image_source_url', 'image_kind'): d[165].pop(k, None)
log(165, 'Photo showed a street/GS25 store, not the studio -> removed (emoji placeholder)', 'fixed', m['165']['url'])

json.dump(d, open(SRC, 'w'), ensure_ascii=False, indent=1)
fold = lambda s: re.sub(r'[^a-z0-9 ]', ' ', unicodedata.normalize('NFD', (s or '').replace('đ', 'd').replace('Đ', 'd')).encode('ascii', 'ignore').decode().lower())
with open(CSV, 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['id', 'name', 'issue', 'action', 'source_url'])
    for i in sorted(prev):
        p = prev[i]
        if i in rows: issue, action, url = rows[i]
        elif p['issue'].startswith(AUTO) and str(i) in m and m[str(i)].get('name'):
            r = m[str(i)]; issue, action, url = f'Google Maps live check {DATE}: resolves to "{r["name"]}" ({r.get("category")}), {r.get("address") or ""}; not marked closed', 'ok', r['url']
        else: issue, action, url = p['issue'], p['action'], p['source_url']
        w.writerow([i, d[i]['name'], issue, action, url])
import collections; print(collections.Counter(r['action'] for r in csv.DictReader(open(CSV))))
