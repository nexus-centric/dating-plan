# Builds data/merged_hcm.json + data/excluded_bliss.json from research_hcm.json, bliss_home_places.json (+raw coords), web_additions.json
import json,re,unicodedata,math,os,sys,collections,re as _re
sys.path.insert(0,os.path.dirname(__file__)); from geo_util import district as pip
D='/workspace/date-app/data/'
research=json.load(open(D+'research_hcm.json')); bliss=json.load(open(D+'bliss_home_places.json')); web=json.load(open(D+'web_additions.json'))
REV=json.load(open(D+'raw_bliss/_reverse_cache.json'))
FWD=json.load(open(D+'raw_bliss/_forward_cache.json')) if os.path.exists(D+'raw_bliss/_forward_cache.json') else {}
def norm(s): s=unicodedata.normalize('NFD',s.lower()).replace('đ','d'); s=''.join(c for c in s if unicodedata.category(c)!='Mn'); return re.sub(r'[^a-z0-9]+',' ',s).strip()
def km(a,b,c,d):
  R=6371;p=math.radians; x=math.sin(p(c-a)/2)**2+math.cos(p(a))*math.cos(p(c))*math.sin(p(d-b)/2)**2; return 2*R*math.asin(math.sqrt(x))
KEEP={'Quận 1','Quận 3','Quận 4','Quận 5','Quận 6','Quận 7','Quận 8','Quận 10','Quận 11','Phú Nhuận','Bình Thạnh','Tân Bình','Tân Phú','Gò Vấp','Quận 2'}
DNORM={'Quận 2':'TP Thủ Đức (Q2 cũ)'}
MOOD={'Homestay date':['lãng mạn','kỷ niệm','ngày mưa'],'Work date':['chill','ngày mưa'],'Shopping date':['chill','rẻ mà vui'],'Spa date':['chill','lãng mạn','ngày mưa'],'Tổ hợp game date':['năng động','ngày mưa','rẻ mà vui'],'Picnic date':['chill','rẻ mà vui','năng động'],'Check-in date':['chill','lãng mạn'],'Photobooth date':['rẻ mà vui','kỷ niệm','ngày mưa'],'Deep talk date':['chill','lãng mạn','đêm muộn'],'Fine Dining date':['lãng mạn','sang chảnh','kỷ niệm'],'Workshop date':['kỷ niệm','ngày mưa']}
FOODCAT=re.compile(r'cà phê|Món ăn|Nhà hàng|Quán bar|Quầy giải khát|Quán ăn|Thịt nướng|Bít tết|Tiệm bánh|Hộp đêm|Quán bia|rang cà phê',re.I)
def price(pl):
  if not pl: return None,None
  m=re.match(r'([\d.]+)-([\d.]+)\s*(N)?\s*₫',pl)
  if not m: return None,f'Google Maps: {pl}'
  lo,hi=[int(x.replace('.','')) for x in m.groups()[:2]]
  if m.group(3): lo*=1000; hi*=1000
  return hi*2, f'Google Maps ghi {pl}/người → ước tính tối đa {hi*2:,}đ/2 người'.replace(',','.')
stats=collections.Counter(); excluded=[]; dropped=[]
# 1. collect bliss rows with coords
recs={}  # key -> rec
for lst,v in bliss.items():
  raw=json.load(open(D+f'raw_bliss/{lst}.json')); pool=list(raw)
  for p in v['places']:
    stats['bliss_rows']+=1
    m=next((r for r in pool if r['name']==p['name']),None)
    if m: pool.remove(m)
    cat=p['category'] or ''
    if 'vĩnh viễn' in cat: stats['closed_dropped']+=1; dropped.append({'name':p['name'],'list':lst,'reason':'Bị đóng vĩnh viễn (Google Maps)'}); continue
    if not p['rating'] and re.match(r'^\d',p['name']): stats['not_a_place']+=1; dropped.append({'name':p['name'],'list':lst,'reason':'Chỉ là địa chỉ, không phải địa điểm'}); continue
    lat,lng=(m['lat'],m['lng']) if m else (None,None)
    # dedupe: same normalized name and within 150 m (or no coords)
    key=None
    for k,r in recs.items():
      if norm(r['name'])==norm(p['name']) and (lat is None or r['lat'] is None or km(lat,lng,r['lat'],r['lng'])<0.15): key=k;break
    if key:
      stats['dup_bliss']+=1; r=recs[key]
      if lst not in r['lists']: r['lists'].append(lst); r['source_urls'].append(v['url'])
      continue
    recs[len(recs)]={'name':p['name'],'lists':[lst],'gcat':cat,'rating':float(p['rating'].replace(',','.')) if p['rating'] else None,
      'reviews':int(p['reviews'].replace('.','')) if p['reviews'] else None,'pl':p['price_level'],'lat':lat,'lng':lng,'cid':m['cid'] if m else None,
      'temp_closed':'Tạm thời' in cat,'source_urls':[v['url']]}
# 2. map
out=[]; names=collections.Counter(norm(r['name']) for r in recs.values())
for r in recs.values():
  d=pip(r['lat'],r['lng']) if r['lat'] else None
  if d is None: excluded.append({'name':r['name'],'lists':r['lists'],'reason':'ngoài TP.HCM hoặc không có toạ độ','lat':r['lat'],'lng':r['lng']}); stats['excl_outside']+=1; continue
  if d not in KEEP: excluded.append({'name':r['name'],'lists':r['lists'],'district':d,'reason':f'ngoài khu trung tâm ({d})','lat':r['lat'],'lng':r['lng']}); stats['excl_'+d]+=1; continue
  rv=REV.get(f"{r['lat']:.6f},{r['lng']:.6f}",{}); a=rv.get('address',{})
  street=' '.join(x for x in [a.get('house_number'),a.get('road')] if x)
  dn=DNORM.get(d,d)
  addr=', '.join(x for x in [street,a.get('suburb') or a.get('quarter'),dn] if x)
  lst=r['lists'][0]; gc=r['gcat'] if not r['temp_closed'] else ''
  typ='food' if (lst in('Fine Dining date','Deep talk date') or (lst in('Work date','Check-in date') and FOODCAT.search(gc or 'cà phê'))) else 'activity'
  if lst=='Check-in date' and re.search(r'Công viên|Cửa hàng',gc): typ='activity'
  pc,pn=price(r['pl'])
  name=r['name']
  if names[norm(name)]>1: name=f"{name} ({dn})"
  cid_url=f"https://maps.google.com/?cid={r['cid']}" if r['cid'] else None
  desc=(f"{gc} · " if gc else '')+f"Có trong list “{' / '.join(r['lists'])}” của Bliss Home."
  if r['temp_closed']: desc+=' Google Maps ghi “Tạm thời đóng cửa”.'
  out.append({'name':name,'type':typ,'category':lst,'district':dn,'address':('Gần '+addr+' (vị trí ước tính từ toạ độ Google Maps, OSM)') if street else (dn+' (từ toạ độ Google Maps)'),
    'price_per_couple_vnd':pc,'price_note':pn,'opening_hours':None,'mood_tags':MOOD[lst],'description_vi':desc,
    'source_urls':r['source_urls']+([cid_url] if cid_url else []),'source':'bliss_home','out_of_area':False,
    'status':'uncertain' if r['temp_closed'] else 'likely_operating','date_checked':'2026-10-25',
    'rating':r['rating'],'reviews':r['reviews'],'lat':round(r['lat'],6),'lng':round(r['lng'],6),'lists':r['lists'],'google_category':r['gcat'],'maps_url':cid_url,'address_approx':bool(street)})
  stats['kept_bliss']+=1
# 3. research items: keep, enrich, dedupe bliss into them
def similar(a,b):
  A,B=norm(a),norm(b); return A==B or (len(A)>6 and len(B)>6 and (A in B or B in A))
base=[]
for it in research+web:
  it=dict(it); it.setdefault('rating',None); it.setdefault('reviews',None); it.setdefault('lists',[]); it.setdefault('maps_url',None)
  it.setdefault('lat',None); it.setdefault('lng',None)
  if it.get('address') and not it.get('out_of_area'):
    from geo_util import clean
    res=FWD.get(clean(it['address'])) or []
    if res:
      la,ln=float(res[0]['lat']),float(res[0]['lon']); pd=pip(la,ln)
      want=it.get('district') or ''
      if pd and (DNORM.get(pd,pd).split(' ')[0] in want or pd in want or (pd=='Quận 2' and 'Thảo Điền' in want)): it['lat'],it['lng']=round(la,6),round(ln,6)
  base.append(it)
final=[]
for b in out:
  hit=next((x for x in base if similar(x['name'],b['name'])),None)
  if hit:
    stats['dup_vs_existing']+=1
    hit['rating']=hit['rating'] or b['rating']; hit['reviews']=hit['reviews'] or b['reviews']; hit['lists']=sorted(set(hit['lists']+b['lists']))
    hit['source_urls']=hit['source_urls']+[u for u in b['source_urls'] if u not in hit['source_urls']]
    if hit['lat'] is None: hit['lat'],hit['lng']=b['lat'],b['lng']
    hit['maps_url']=hit['maps_url'] or b['maps_url']
    continue
  final.append(b)
merged=base+final
for it in merged:
  dd=it.get('district') or ''
  m=_re.search(r'Quận \d+|Bình Thạnh|Phú Nhuận|Tân Bình|Tân Phú|Gò Vấp|Thảo Điền|Thủ Đức',dd)
  it['district_norm']=None if not m or it.get('out_of_area') else ('TP Thủ Đức (Q2 cũ)' if m.group(0) in('Thảo Điền','Thủ Đức') else m.group(0))
json.dump(merged,open(D+'merged_hcm.json','w'),ensure_ascii=False,indent=1)
json.dump({'excluded_out_of_area':excluded,'dropped':dropped},open(D+'excluded_bliss.json','w'),ensure_ascii=False,indent=1)
json.dump(merged,open('/workspace/date-app/src/data.json','w'),ensure_ascii=False)
print(dict(stats)); print('merged',len(merged),'research',len(research),'web',len(web),'bliss kept new',len(final))
print(collections.Counter(i['district_norm'] for i in merged).most_common())
print('no coords',sum(1 for i in merged if i['lat'] is None and i['type']!='idea' and not i['out_of_area']))
