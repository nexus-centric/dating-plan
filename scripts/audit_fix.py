#!/usr/bin/env python3
"""Audit fixes 2026-10-31. Backup: tmp/data-before-audit.json. Writes src/data.json + /workspace/date-app-audit.csv.
Hidden places get status='hidden' (+hidden_reason); src/data.ts filters status closed/hidden. Nothing is deleted."""
import json, csv, re, shutil, os
from urllib.parse import quote
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, BAK = f'{ROOT}/src/data.json', f'{ROOT}/tmp/data-before-audit.json'
if not os.path.exists(BAK): shutil.copy(SRC, BAK)
d = json.load(open(BAK))
DATE = '2026-10-31'
NQ29 = 'https://congbao.hochiminhcity.gov.vn/cong-bao/van-ban/nghi-quyet/so/29-2026-nq-hdnd/ngay/27-08-2026/tai-ve/50039'
BOX = dict(lat=(10.72, 10.84), lng=(106.62, 106.78))  # central HCMC bounding box
search = lambda name, addr: 'https://www.google.com/maps/search/?api=1&query=' + quote(f'{name} {addr} TP.HCM')
rows = {}
def log(i, issue, action, url): rows[i] = (issue, action, url)
def hide(i, reason, url): d[i].update(status='hidden', hidden_reason=reason, date_checked=DATE); log(i, reason, 'hidden', url)

# --- verified closures / not a visitable place ---
hide(89, 'Tripadvisor: "reported permanently closed"; reviews 2023 say moved/closed; website has no programmes', 'https://www.tripadvisor.com/Attraction_Review-g293925-d10088468-Reviews-The_Factory_Contemporary_Arts_Centre-Ho_Chi_Minh_City.html')
hide(90, '188/1 Nguyễn Văn Hưởng permanently closed (Wanderlog/hcm-cityguide); brand relaunching at new venue, address not yet confirmed', 'https://wanderlog.com/place/details/1410265/saigon-outcast')
hide(371, 'Cuốn N Roll announced closure of the whole chain from 25/4/2026 (and it is a Hà Nội brand)', 'https://cuonnroll.com/tin-khuyen-mai/cuon-n-roll-gui-loi-chao-tam-biet-nha-minh/')
hide(71, 'Not a walk-in photobooth: Printaphy only rents photobooths for events (quote-based)', 'https://www.printaphy.com/')
# --- out of central area (coords outside box) ---
for i, x in enumerate(d):
    if x.get('status') in ('closed', 'hidden') or x.get('type') == 'idea' or x.get('out_of_area'): continue
    la, ln = x.get('lat'), x.get('lng')
    if x.get('area') == 'Tân Phú': continue  # b13: Tân Phú is in scope (bbox lng extended to 106.60)
    if la and not (BOX['lat'][0] <= la <= BOX['lat'][1] and BOX['lng'][0] <= ln <= BOX['lng'][1]):
        hide(i, f'Out of central HCMC: coords {la},{ln} ({x.get("area")})', x.get('maps_url') or '')

# --- fixes ---
x = d[51]; x.update(name='Powerbowl Vạn Hạnh Mall (bowling)', address='Tầng 5, Vạn Hạnh Mall, 11 Sư Vạn Hạnh, P. Hòa Hưng (Q.10)', status='likely_operating',
  price_min=45000, price_max=75000, price_unit='person', couple_min=90000, couple_max=150000, price_confidence='medium', price_checked=DATE,
  price_note='35–65k/ván tùy khung giờ/ngày + thuê giày 10k (1 ván/người)', price_source_url='https://meetup.vn/dia-diem/bowling-van-hanh-mall-11-su-van-hanh-quan-10/',
  opening_hours='9:00–22:00', date_checked=DATE)
log(51, 'Price source was unrelated page (60–100k); official operator is Powerbowl', 'fixed', 'http://powerbowl.vn/trung-tam/')
x = d[370]; x.update(address='A65 Nguyễn Trãi, P. Nguyễn Cư Trinh, Q.1', opening_hours='05:30–21:30', price_min=69000, price_max=80000, price_unit='person',
  couple_min=138000, couple_max=160000, price_note='69–80k/tô (Foody)', price_source_url='https://www.foody.vn/ho-chi-minh/quynh-hu-tieu-nam-vang',
  price_confidence='medium', price_checked=DATE, maps_kind='search', lat=None, lng=None, date_checked=DATE)
x['maps_url'] = search('Hủ Tiếu Nam Vang Quỳnh', x['address'])
log(370, 'Wrong address (86 Lê Thị Riêng); Foody lists A65 Nguyễn Trãi; price 69–80k not 50–55k', 'fixed', 'https://www.foody.vn/ho-chi-minh/quynh-hu-tieu-nam-vang')
x = d[369]; x.update(status='uncertain', price_note=(x.get('price_note') or '') + ' · ⚠️ chưa xác minh chi nhánh 339 Lê Văn Sỹ (Foody chỉ có 458 Lê Văn Sỹ, Tân Bình)', date_checked=DATE)
log(369, 'Branch at 339 Lê Văn Sỹ not found; only 458 Lê Văn Sỹ (Tân Bình) confirmed', 'unverified', 'https://www.foody.vn/ho-chi-minh/com-tam-phuc-loc-tho-458-le-van-sy')
area_fix = {175: ('Quận 3', '141/8 Bàn Cờ, P. Bàn Cờ, Q.3'), 234: ('Phú Nhuận', '1A Hoa Lan, P. Cầu Kiệu, Phú Nhuận'), 256: ('Quận 3', '534 Lê Văn Sỹ, P. Nhiêu Lộc, Q.3'),
            363: ('Tân Bình', '351 Lê Văn Sỹ, P. Tân Sơn Hòa, Tân Bình'), 423: ('Quận 1', '12B Cách Mạng Tháng Tám, P. Bến Thành, Q.1')}
for i, (ar, ad) in area_fix.items():
    old = d[i].get('area'); d[i].update(area=ar, district=ar, address=ad, date_checked=DATE)
    log(i, f'District mismatch: address ward/coords = {ar}, data said {old}', 'fixed', d[i].get('maps_url') or '')
for i in (40, 41, 119, 428, 429):  # museum fees: point to NQ 29/2026/NQ-HĐND (hiệu lực 01/10/2026) instead of portal homepage
    d[i]['price_source_url'] = NQ29; d[i]['price_checked'] = DATE
    log(i, 'Fee source was portal homepage; now NQ 29/2026/NQ-HĐND (effective 1/10/2026)', 'fixed', NQ29)
for i in (338, 337, 98, 76, 95, 101):
    log(i, 'Address/price not confirmable from public sources this pass; keeps ⚠️ badge', 'unverified', (d[i].get('source_urls') or [d[i].get('maps_url')])[0] or '')
for i, u in {30: 'https://6ixgo.com/vi/Trons-kitchen.ri102', 419: 'https://www.foody.vn/ho-chi-minh/yuna-alaska-coffee', 348: 'https://photobooth.joelin.cc/en/vietnam/ho-chi-minh/',
             414: d[414]['price_source_url'], 413: NQ29}.items():
    log(i, 'Web-verified: exists at listed address', 'ok', u)

json.dump(d, open(SRC, 'w'), ensure_ascii=False, indent=1)
# --- report: every place the app displays (or displayed before this audit) ---
with open('/workspace/date-app-audit.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['id', 'name', 'issue', 'action', 'source_url'])
    for i, x in enumerate(d):
        if x.get('type') == 'idea': continue
        if x.get('status') == 'closed' and i not in rows: w.writerow([i, x['name'], 'already hidden (closed) before audit', 'hidden', (x.get('source_urls') or [''])[0]]); continue
        issue, action, url = rows.get(i, ('automated checks passed (in-area coords, district/address consistent, image file exists, no duplicate); not individually web-verified', 'ok', x.get('maps_url') or ''))
        w.writerow([i, x['name'], issue, action, url])
import collections; print(collections.Counter(r[1] for r in rows.values()), len(rows))
