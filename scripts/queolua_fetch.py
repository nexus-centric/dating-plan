#!/usr/bin/env python3
"""b13: list places per new ward (2025) x category from queolua.vn (Google-Maps-derived rating/price/geo/photo), cache details.
Out: data/b13/queolua.json"""
import json, re, os, time, urllib.request
OUT = 'data/b13/queolua.json'
WARDS = {'Phú Nhuận': ['phuong-phu-nhuan', 'phuong-duc-nhuan', 'phuong-cau-kieu'],
         'Tân Bình': ['phuong-tan-son-hoa', 'phuong-tan-son-nhat', 'phuong-tan-hoa', 'phuong-bay-hien', 'phuong-tan-binh', 'phuong-tan-son'],
         'Tân Phú': ['phuong-tan-phu', 'phuong-tay-thanh', 'phuong-tan-son-nhi', 'phuong-phu-tho-hoa', 'phuong-phu-thanh']}
CATS = ['nha-hang', 'quan-ca-phe', 'tiem-banh', 'quan-an']
cache = json.load(open(OUT)) if os.path.exists(OUT) else {'lists': {}, 'places': {}}
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=25).read().decode('utf8', 'ignore')
def lds(h): return [json.loads(m) for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)]
for dist, ws in WARDS.items():
    for w in ws:
        for c in CATS:
            k = f'{c}/{w}'
            if k in cache['lists']: continue
            try:
                h = get(f'https://queolua.vn/danh-muc/{c}/tp-ho-chi-minh/{w}')
                L = next((x for x in lds(h) if x.get('@type') == 'ItemList'), {'itemListElement': []})
                cache['lists'][k] = {'district': dist, 'cat': c, 'urls': [e['url'] for e in L['itemListElement']]}
            except Exception as e: cache['lists'][k] = {'district': dist, 'cat': c, 'urls': [], 'error': str(e)[:80]}
            json.dump(cache, open(OUT, 'w'), ensure_ascii=False, indent=1); time.sleep(0.5)
urls = {u: v['district'] for v in cache['lists'].values() for u in v['urls']}
print('lists', len(cache['lists']), 'places', len(urls))
for u, dist in urls.items():
    if u in cache['places']: continue
    try:
        h = get(u); R = next((x for x in lds(h) if x.get('@type') not in ('BreadcrumbList', 'ItemList') and 'name' in x and '@graph' not in x), None)
        summ = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h[h.find('Quẹo tóm tắt'):h.find('Quẹo tóm tắt') + 600])) if 'Quẹo tóm tắt' in h else ''
        cache['places'][u] = {'district_hint': dist, 'ld': R, 'summary': summ[:400]}
    except Exception as e: cache['places'][u] = {'error': str(e)[:80]}
    if len(cache['places']) % 20 == 0: json.dump(cache, open(OUT, 'w'), ensure_ascii=False, indent=1)
    time.sleep(0.4)
json.dump(cache, open(OUT, 'w'), ensure_ascii=False, indent=1); print('done', len(cache['places']))
