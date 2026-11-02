"""b13: add Maps-verified places in Phú Nhuận / Tân Bình / Tân Phú; un-hide verified Tân Phú items.
Inputs: data/b13/candidates.json (queolua JSON-LD), data/b13/verify.json (live Google Maps check),
data/b13/places.json (Maps place pages for activities). Appends only (ids stay stable). Idempotent."""
import json, re, shutil, os, io, unicodedata, urllib.request
from PIL import Image
D='src/data.json'; TODAY='2026-10-31'
if not os.path.exists('tmp/data-before-b13.json'): shutil.copy(D,'tmp/data-before-b13.json')
d=json.load(open(D)); C=json.load(open('data/b13/candidates.json')); V=json.load(open('data/b13/verify.json')); P=json.load(open('data/b13/places.json'))
have={x['name'] for x in d}
def norm(s): s=unicodedata.normalize('NFD',s or '').lower(); s=''.join(c for c in s if unicodedata.category(c)!='Mn').replace('đ','d'); return re.findall(r'[a-z0-9]+',s)
def same(a,b):
    A,B=set(norm(a)),set(norm(b)); return bool(A and B) and len(A&B)/min(len(A),len(B))>=0.5
def num(r): return float(r.replace(',','.')) if r else None
log=[]
# 1) un-hide Tân Phú items hidden only because of bbox/district
for i in (215,258,271,273):
    v=V.get(f'unhide:{i}') or {}
    if v.get('name') and not v.get('perm_closed') and not v.get('temp_closed') and d[i]['status']=='hidden':
        d[i]['status']='likely_operating'; d[i]['date_checked']=TODAY; d[i].pop('hidden_reason',None)
        d[i]['note']=(d[i].get('note') or '')+f' | b13 {TODAY}: Tân Phú vào phạm vi; Google Maps vẫn hoạt động ({v["address"]}).'
        log.append(('unhide',i,d[i]['name']))
MOOD={'restaurant':['hẹn hò','ăn no'],'streetfood':['bình dân','ăn vặt'],'cafe':['chill'],'dessert':['ngọt ngào','ăn vặt']}
CAT={'restaurant':'nhà hàng','streetfood':'quán ăn','cafe':'cafe','dessert':'tráng miệng'}
UNIT={'cafe':'drink','dessert':'person'}
def photo(url,slug):
    out=f'public/images/b13-{slug}.webp'
    if os.path.exists(out): return '/'+out[7:]
    try:
        b=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read()
        im=Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((800,800)); im.save(out,'WEBP',quality=78); return '/'+out[7:]
    except Exception as e: return None
def slug(s): return '-'.join(norm(s))[:50]
def add(it):
    if it['name'] in have: return
    have.add(it['name']); d.append(it); log.append(('add',it['area'],it['kind'],it['name']))
for c in C:
    v=V.get(c['key']) or {}
    if not v.get('name') or v.get('perm_closed') or v.get('temp_closed') or not same(c['name'],v['name']): log.append(('skip',c['name'],v.get('name'))); continue
    k=c['kind']; pmin,pmax=c['pmin'],c['pmax']; addr=(v['address'] or '').replace('Địa chỉ: ','') or c['addr']
    it=dict(type='food',name=c['name'],kind=k,category=CAT[k],google_category=v.get('category'),district=c['area'],area=c['area'],address=addr,
        lat=c['lat'],lng=c['lng'],maps_url=v['url'],maps_kind='search',rating=num(v.get('rating')) or c['rating'],reviews=c['reviews'],
        price_min=pmin,price_max=pmax,price_unit=UNIT.get(k,'person'),couple_min=pmin*2 if pmin else None,couple_max=pmax*2,price_per_couple_vnd=None,
        price_note=f"queolua.vn: {'%dk–%dk'%(pmin//1000,pmax//1000) if pmin else 'dưới %dk'%(pmax//1000)}/người",
        price_source_url=c['key'],price_confidence='medium',price_method='queolua_jsonld',price_checked=TODAY,
        opening_hours=None,hours=None,mood_tags=MOOD[k],source='b13',source_urls=[c['key'],v['url']],out_of_area=False,status='likely_operating',
        date_checked=TODAY,added=TODAY,lists=[],website=None,discovered_via='queolua.vn ward listing + Google Maps verify',
        description_vi=f"{c.get('sub') or CAT[k]} ở {c['area']}; điểm {c['rating']}/5 ({c['reviews']} đánh giá, queolua.vn).",
        note=f"Google Maps {TODAY}: '{v['name']}' đang hoạt động, rating {v.get('rating')}. Số đánh giá từ queolua.vn (Maps chế độ hạn chế).")
    if c.get('image'):
        im=photo(c['image'],slug(c['name']))
        if im: it.update(image=im,image_credit='Ảnh: Google Maps (qua queolua.vn)',image_source_url=c['key'],image_kind='photo')
    add(it)
# 2) activities: (maps name, kind, name, pmin, pmax, unit, src, conf, mood, desc)
A=[('Hiên Concept','workshop','Hiên Concept – workshop gốm',450000,450000,'person','https://artlive.vn/en/hien-concept-where-your-soul-and-heart-are-healed/','medium',['sáng tạo','chill'],'Workshop làm gốm/tô tượng cho cặp đôi.'),
 ('Tiệm Bia Bọt - Quán Rooftop Tân Bình','bar','Tiệm Bia Bọt – Rooftop Tân Bình',100000,200000,'person','https://queolua.vn/dia-diem/tiem-bia-bot-quan-rooftop-tan-binh','medium',['đêm muộn','chill'],'Quán bia rooftop nhìn phố Tân Bình.'),
 ('MA BAE - Tap&Bar','bar','MA BAE – Tap&Bar',80000,None,'drink','https://www.greensm.com/vn-vi/news/bar-tan-phu','low',['đêm muộn','chill'],'Tap bar bia thủ công ở Tân Phú; nghỉ thứ Ba (theo nguồn giá).'),
 ('Inside Xcape Room','game','Inside Xcape Room',169000,199000,'person','https://insidexcape.vn/bang-gia/','medium',['hồi hộp','ngày mưa'],'Escape room giải đố, giá theo người/giờ.'),
 ('Jinzo Escape Saigon','game','Jinzo Escape Saigon',169000,199000,'person','https://oceanlanternfestival.com/top-10-escape-room-sai-gon-cam-nang-trai-nghiem-hack-nao-dinh-cao/','low',['hồi hộp','ngày mưa'],'Escape room ở Đức Nhuận (Phú Nhuận).'),
 ('Spirit Escape cơ sở 2','game','Spirit Escape (cơ sở 2)',159000,199000,'person','https://oceanlanternfestival.com/top-10-escape-room-sai-gon-cam-nang-trai-nghiem-hack-nao-dinh-cao/','low',['hồi hộp','ngày mưa'],'Escape room chủ đề kinh dị/giải đố.'),
 ('PHOTO TIME - TẦNG 2 LOTTE MART TÂN BÌNH','photobooth','PHOTO TIME – Lotte Mart Tân Bình',70000,110000,'session','https://hcm.inhat.vn/photobooth-tphcm/','low',['vui vẻ','ngày mưa'],'Photobooth tầng 2 Lotte Mart Cộng Hòa.'),
 ('PHOTO TIME - AEON MALL TÂN PHÚ CELADON','photobooth','PHOTO TIME – AEON Mall Tân Phú',70000,110000,'session','https://hcm.inhat.vn/photobooth-tphcm/','low',['vui vẻ','ngày mưa'],'Photobooth trong AEON Mall Tân Phú Celadon.'),
 ('Photoism Phú Nhuận','photobooth','Photoism Phú Nhuận',70000,100000,'session','https://simpletech.vn/blogs/photobooth/7-dia-diem-chup-anh-photobooth-tai-sai-gon','low',['vui vẻ','ngày mưa'],'Photobooth Hàn Quốc trên Hoa Lan.'),
 ('GenZ Cinema Phan Xích Long','cinema','GenZ Cinema Phan Xích Long (phòng chiếu riêng)',None,None,'room',None,None,['chill','ngày mưa','đêm muộn'],'Phòng chiếu phim riêng (cùng chuỗi GENZ Cinema).')]
AREA={'Hiên':'Tân Bình','Tiệm Bia':'Tân Bình','MA BAE':'Tân Phú','PHOTO TIME - TẦNG':'Tân Bình','PHOTO TIME - AEON':'Tân Phú'}
genz=next(x for x in d if x['name'].startswith('GENZ Cinema Tân Bình'))
byname={p['name']:(u,p) for u,p in P.items() if p.get('name')}
for mn,k,nm,pmin,pmax,unit,src,conf,mood,desc in A:
    u,p=byname[mn]
    if p.get('perm_closed') or p.get('temp_closed'): log.append(('skip',nm,'closed')); continue
    m=re.search(r'!3d(-?[\d.]+)!4d(-?[\d.]+)',u); area=next((v for kk,v in AREA.items() if mn.startswith(kk)),'Phú Nhuận')
    it=dict(type='food' if k=='bar' else 'activity',name=nm,kind=k,category={'bar':'bar','game':'escape room','photobooth':'photobooth','workshop':'workshop','cinema':'rạp chiếu phim'}[k],
        google_category=p.get('category'),district=area,area=area,address=p['address'].replace('Địa chỉ: ',''),lat=float(m[1]),lng=float(m[2]),maps_url=u,maps_kind='direct',
        rating=num(p.get('rating')),reviews=None,price_min=pmin,price_max=pmax,price_unit=unit,
        couple_min=pmin*(1 if unit in('session','room') else 2) if pmin else None,couple_max=pmax*(1 if unit in('session','room') else 2) if pmax else None,price_per_couple_vnd=None,
        price_source_url=src,price_confidence=conf,price_method='web_source',price_checked=TODAY,opening_hours=None,hours=None,mood_tags=mood,source='b13',
        source_urls=[x for x in (src,u) if x],out_of_area=False,status='likely_operating',date_checked=TODAY,added=TODAY,lists=[],website=p.get('website'),
        discovered_via='Google Maps search (b13)',description_vi=desc,note=f'Google Maps {TODAY}: đang hoạt động. Số đánh giá: chưa xác minh (Maps chế độ hạn chế).')
    if k=='cinema':
        for f in ('price_min','price_max','price_unit','couple_min','couple_max','price_note','price_source_url','price_confidence','price_method','opening_hours','hours'): it[f]=genz.get(f)
        it['note']+=' Giá lấy theo chuỗi GENZ Cinema (nguồn chi nhánh Tân Bình) – unverified cho chi nhánh này.'; it['price_confidence']='low'
    add(it)
json.dump(d,open(D,'w'),ensure_ascii=False,indent=1)
json.dump(log,open('data/b13/add_log.json','w'),ensure_ascii=False,indent=1)
import collections; print(collections.Counter((l[0],)+((l[1],l[2]) if l[0]=='add' else ()) for l in log)); print([l for l in log if l[0]=='skip'])
