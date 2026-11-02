#!/usr/bin/env python3
"""b13 step 1: pick candidates from queolua (food/cafe/dessert) + gm_discover (activities). Writes data/b13/candidates.json + verify_todo.json"""
import json, re, unicodedata, collections
d = json.load(open('src/data.json'))
fold = lambda s: re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFD', (s or '').replace('đ', 'd').replace('Đ', 'd')).encode('ascii', 'ignore').decode().lower())
have = {fold(x['name']) for x in d}
# old district <- new (2025) ward names; Tân Phú checked first because "Tân Sơn Nhì" contains "Tân Sơn"
WARD = [('Tân Phú', ['Tân Phú', 'Tân Sơn Nhì', 'Tây Thạnh', 'Phú Thọ Hòa', 'Phú Thạnh', 'Hiệp Tân', 'Tân Thới Hòa']),
        ('Phú Nhuận', ['Phú Nhuận', 'Cầu Kiệu', 'Đức Nhuận']),
        ('Tân Bình', ['Tân Bình', 'Tân Sơn Hòa', 'Tân Sơn Nhất', 'Bảy Hiền', 'Tân Hòa', 'Tân Sơn'])]
def area_of(a):
    a = re.sub(r'^Địa chỉ:\s*', '', a or '')
    for D, ws in WARD:
        if any(re.search(r'(?<!\w)' + w + r'(?!\w)', a) for w in ws): return D
BOX = lambda la, ln: la and 10.72 <= la <= 10.84 and 106.60 <= ln <= 106.78
def money(s): return [int(x.replace('.', '')) for x in re.findall(r'(\d[\d.]*)\s*đ', s or '')]
Q = json.load(open('data/b13/queolua.json'))
cands = []
CAT = {'nha-hang': 'restaurant', 'quan-an': 'restaurant', 'quan-ca-phe': 'cafe', 'tiem-banh': 'dessert'}
cat_of = {u: v['cat'] for v in Q['lists'].values() for u in v['urls']}
for u, p in Q['places'].items():
    L = p.get('ld') or {}
    if not L.get('name') or fold(L['name']) in have: continue
    if re.search(r'mang đi|giao hàng|online|takeaway|sỉ|đại lý|chay|tạp hóa', L['name'], re.I): continue
    ar = area_of((L.get('address') or {}).get('streetAddress'))
    g = L.get('geo') or {}; R = L.get('aggregateRating') or {}
    pr = money(L.get('priceRange'))
    if len(pr) == 1 and re.match(r'Dưới', L.get('priceRange') or ''): pr = [None, pr[0]]   # 'Dưới 100.000đ' = upper bound only
    if not ar or not BOX(g.get('latitude'), g.get('longitude')) or len(pr) < 2 or pr[1] > 500000: continue
    if (R.get('ratingValue') or 0) < 4.3 or (R.get('reviewCount') or 0) < 40: continue
    summ = p.get('summary', ''); m = re.search(r'Quẹo tóm tắt\s+(.+?) ở ', summ); sub = (m.group(1) if m else '').split(',')[0].strip()
    kind = CAT[cat_of[u]]
    if kind == 'restaurant' and pr[1] <= 100000: kind = 'streetfood'
    if re.search(r'chè|kem|tráng miệng|bánh flan|sữa chua', sub + ' ' + L['name'], re.I): kind = 'dessert'
    cands.append(dict(src='queolua', key=u, name=L['name'], area=ar, kind=kind, sub=sub, addr=L['address']['streetAddress'], lat=g['latitude'], lng=g['longitude'],
                      rating=R.get('ratingValue'), reviews=R.get('reviewCount'), pmin=pr[0], pmax=pr[1], image=L.get('image'), hours=L.get('openingHoursSpecification')))
score = lambda c: (c['rating'] * c['reviews'] + 4.3 * 30) / (c['reviews'] + 30)
CAP = {'restaurant': 12, 'streetfood': 5, 'cafe': 8, 'dessert': 5}
pick = []
for D in ('Phú Nhuận', 'Tân Bình', 'Tân Phú'):
    n = collections.Counter()
    for c in sorted([c for c in cands if c['area'] == D], key=lambda c: -score(c)):
        if n[c['kind']] < CAP[c['kind']]: n[c['kind']] += 1; pick.append(c)
json.dump(pick, open('data/b13/candidates.json', 'w'), ensure_ascii=False, indent=1)
json.dump([{'key': c['key'], 'q': f"{c['name']} {c['addr']}"} for c in pick], open('data/b13/verify_todo.json', 'w'), ensure_ascii=False, indent=1)
print(len(cands), 'pool;', collections.Counter((c['area'], c['kind']) for c in pick))
