"""Enrichment pass (2026-10-26): structured prices, maps_url, images, new ideas.
Input : data/merged_hcm.json (from merge_v2.py) + data/price_research.py + data/images_progress.json + data/new_ideas_2026_10.json
Output: src/data.json, data/enrich_progress.json (coverage report)"""
import json, re, urllib.parse, collections
D='/workspace/date-app/data/'; TODAY='2026-10-26'
base=json.load(open(D+'merged_hcm.json'))
ns={}; exec(open(D+'price_research.py').read(), ns); R,E,CHAIN,FREE=ns['R'],ns['E'],ns['CHAIN'],ns['FREE_NOTE']
imgs=json.load(open(D+'images_progress.json'))
new=json.load(open(D+'new_ideas_2026_10.json'))
FIELDS=['price_min','price_max','price_unit','couple_min','couple_max','price_source_url','price_confidence']
def chain(name):
    last=None
    for pre,rec in CHAIN:
        rec=rec or last; last=rec
        if name.startswith(pre): return rec
def setp(it,rec,note=None,method=''):
    for f in FIELDS: it[f]=rec.get(f)
    if note is not None: it['price_note']=note
    elif rec.get('price_note'): it['price_note']=rec['price_note']
    it['price_checked']=TODAY; it['price_method']=method
    cm,cx=it['couple_min'],it['couple_max']
    it['price_per_couple_vnd']=cx if cx is not None else cm   # planner budget uses the upper estimate
    if rec.get('status_override'): it['status']=rec['status_override']
MAPS=re.compile(r'Google Maps ghi ([\d.]+)\s*-\s*([\d.]+)\s*(N)?\s*₫')
def num(s,n): v=int(s.replace('.','')); return v*1000 if n else v
for it in base: it.pop('price_per_couple_vnd_old',None)
items=[]
for it in base:
    it=dict(it); nm=it['name']
    for f in FIELDS+['price_checked','price_method']: it.setdefault(f,None)
    if it['type']=='idea' or it.get('out_of_area'):
        items.append(it); continue
    rec=R.get(nm) or next((v for k,v in R.items() if nm.startswith(k) or k.startswith(nm)),None) or chain(nm)
    note=it.get('price_note') or ''
    m=MAPS.search(note)
    if rec: setp(it,rec,method='web_research_2026-10-26')
    elif nm in E:
        mn,mx,u,cm,cx,conf=E[nm]; setp(it,dict(price_min=mn,price_max=mx,price_unit=u,couple_min=cm,couple_max=cx,price_source_url=(it['source_urls'] or [None])[0],price_confidence=conf),note=note,method='earlier_research_structured')
    elif m:
        a,b=m.group(1),m.group(2); n=bool(m.group(3))
        lo=num(a,n) if not (a=='1' and not n) else None; hi=num(b,n)
        if a=='1': lo=None
        setp(it,dict(price_min=lo,price_max=hi,price_unit='person',couple_min=(2*lo if lo else None),couple_max=2*hi,price_source_url=it.get('maps_url'),price_confidence='medium'),
             note=f'Khoảng giá Google Maps: {"≤"+format(hi,",").replace(",",".") if lo is None else format(lo,",").replace(",",".")+"–"+format(hi,",").replace(",",".")}đ/người',method='google_maps_price_range (Bliss Home scrape)')
    elif nm in FREE or ('Shopping date' in it.get('lists',[]) and 'orkshop' not in nm):
        setp(it,dict(price_min=0,price_max=0,price_unit='free',couple_min=0,couple_max=0,price_source_url=it.get('maps_url'),price_confidence='medium'),
             note=FREE.get(nm,'Vào xem miễn phí; mua sắm tuỳ ý'),method='free_entry')
    else:
        it['price_per_couple_vnd']=None
    items.append(it)
# new ideas
for n in new:
    it={'type':'activity','district':None,'address':None,'price_per_couple_vnd':None,'price_note':None,'opening_hours':None,'mood_tags':[],'source':'web','out_of_area':False,'status':'likely_operating','date_checked':TODAY,
        'rating':None,'reviews':None,'lists':[],'maps_url':None,'lat':None,'lng':None,'website':None,'google_category':None,'hours':None,'area':None,'kind':'other'}
    it.update({k:v for k,v in n.items() if k!='price'}); it['added']=TODAY
    for f in FIELDS+['price_checked','price_method']: it.setdefault(f,None)
    if n.get('price'):
        mn,mx,u,cm,cx,url,conf,note=n['price']; setp(it,dict(price_min=mn,price_max=mx,price_unit=u,couple_min=cm,couple_max=cx,price_source_url=url,price_confidence=conf),note=note,method='web_research_2026-10-26')
    items.append(it)
# maps + images
for it in items:
    if it['type']=='idea': continue
    mu=it.get('maps_url') or ''
    if re.search(r'cid=\d+|/maps/place/|place_id|goo\.gl',mu): it['maps_kind']='direct'
    else:
        q=' '.join(x for x in [it['name'].split(' (')[0], it.get('address') or it.get('district') or '', 'TP.HCM'] if x)
        it['maps_url']='https://www.google.com/maps/search/?api=1&query='+urllib.parse.quote(q); it['maps_kind']='search'
    im=imgs.get(it['name'])
    if im and im.get('ok'):
        it['image']=im['image']; it['image_credit']='Ảnh: Facebook của quán' if 'facebook.com' in im['image_source_url'] else im['image_credit']; it['image_source_url']=im['image_source_url']; it['image_kind']=im.get('image_kind','photo')
json.dump(items,open('/workspace/date-app/src/data.json','w'),ensure_ascii=False)
# coverage
loc=[i for i in items if i['type']!='idea' and not i.get('out_of_area')]
rep={'generated':TODAY,'located_items':len(loc),
 'price_any':sum(i['couple_min'] is not None or i['couple_max'] is not None or i['price_min'] is not None or i['price_max'] is not None for i in loc),
 'price_couple_estimate':sum(i['price_per_couple_vnd'] is not None for i in loc),
 'by_confidence':collections.Counter(i['price_confidence'] or 'none' for i in loc),
 'by_type':{t:{'total':sum(i['type']==t for i in loc),'priced':sum(i['type']==t and i['price_per_couple_vnd'] is not None for i in loc)} for t in ['food','activity']},
 'by_source':{s:{'total':sum(i['source']==s for i in loc),'priced':sum(i['source']==s and i['price_per_couple_vnd'] is not None for i in loc)} for s in ['user','web','bliss_home']},
 'by_method':collections.Counter(i['price_method'] or 'none' for i in loc),
 'maps':collections.Counter(i.get('maps_kind') for i in loc),
 'images':collections.Counter(i.get('image_kind','none') for i in loc),
 'new_items':len(new),
 'unpriced':[i['name'] for i in loc if i['price_per_couple_vnd'] is None]}
json.dump(rep,open(D+'enrich_progress.json','w'),ensure_ascii=False,indent=1)
print(json.dumps({k:v for k,v in rep.items() if k!='unpriced'},ensure_ascii=False,indent=1)); print(len(rep['unpriced']),'unpriced')
