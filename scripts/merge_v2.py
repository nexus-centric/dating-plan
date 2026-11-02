# v2 (26/10/2026): research + web_additions + new_types + Bliss Home (address from public Google Maps place pages)
# -> data/merged_hcm.json, data/excluded_hcm.json, data/unresolved_bliss.json, src/data.json
import json,re,difflib,unicodedata,math,os,sys,collections
sys.path.insert(0,os.path.dirname(__file__)); from geo_util import district as pip, clean
D='/workspace/date-app/data/'; TODAY='2026-10-26'
research=json.load(open(D+'research_hcm.json')); web=json.load(open(D+'web_additions.json')); newt=json.load(open(D+'new_types_hcm.json'))
bliss=json.load(open(D+'bliss_home_places.json'))
GM=json.load(open(D+'raw_bliss/_gm_details.json'))
FWD=json.load(open(D+'raw_bliss/_forward_cache.json')) if os.path.exists(D+'raw_bliss/_forward_cache.json') else {}
def norm(s): s=unicodedata.normalize('NFD',s.lower()).replace('đ','d'); s=''.join(c for c in s if unicodedata.category(c)!='Mn'); return re.sub(r'[^a-z0-9]+',' ',s).strip()
def km(a,b,c,d):
  p=math.radians; x=math.sin(p(c-a)/2)**2+math.cos(p(a))*math.cos(p(c))*math.sin(p(d-b)/2)**2; return 2*6371*math.asin(math.sqrt(x))
LABEL={'Quận 2':'TP Thủ Đức (Q2 cũ)','Thủ Đức (cũ)':'TP Thủ Đức (Thủ Đức cũ)'}
KEEP={'Quận 1','Quận 3','Quận 4','Quận 5','Quận 6','Quận 7','Quận 8','Quận 10','Quận 11','Phú Nhuận','Bình Thạnh','Tân Bình','Tân Phú','Gò Vấp','Quận 2','Thủ Đức (cũ)'}
EXCL={'Quận 12','Củ Chi','Hóc Môn','Bình Chánh','Nhà Bè','Cần Giờ','Quận 9','Bình Tân'}
MOOD={'Homestay date':['lãng mạn','kỷ niệm','ngày mưa'],'Work date':['chill','ngày mưa'],'Shopping date':['chill','rẻ mà vui'],'Spa date':['chill','lãng mạn','ngày mưa'],'Tổ hợp game date':['năng động','ngày mưa','rẻ mà vui'],'Picnic date':['chill','rẻ mà vui','năng động'],'Check-in date':['chill','lãng mạn'],'Photobooth date':['rẻ mà vui','kỷ niệm','ngày mưa'],'Deep talk date':['chill','lãng mạn','đêm muộn'],'Fine Dining date':['lãng mạn','sang chảnh','kỷ niệm'],'Workshop date':['kỷ niệm','ngày mưa']}
def fnum(s): return float(s.replace(',','.')) if s else None
def inum(s): return int(re.sub(r'\D','',s)) if s and re.sub(r'\D','',s) else None
def price(pl):
  if not pl: return None,None
  m=re.match(r'([\d.]+)-([\d.]+)\s*(N)?\s*₫',pl)
  if not m: return None,f'Google Maps: {pl}'
  lo,hi=[int(x.replace('.','')) for x in m.groups()[:2]]
  if m.group(3): lo*=1000; hi*=1000
  return hi*2, f'Google Maps ghi {pl}/người → ước tính tối đa {hi*2:,}đ/2 người'.replace(',','.')
def hours_of(h):
  if not h: return None,None
  m=re.match(r'([^,]+),(.*?), Sao chép',h)
  if not m: return None,None
  day,t=m.groups(); t=t.strip()
  if re.search(r'Mở cửa cả ngày',t): return 'Mở cửa 24 giờ (Google Maps)',[0,1440]
  if 'Đóng cửa' in t and 'đến' not in t: return f'{day}: đóng cửa (Google Maps – kiểm tra ngày khác)',None
  mm=re.findall(r'(\d{1,2}):(\d{2}) đến (\d{1,2}):(\d{2})',t)
  if not mm: return f'{t} (Google Maps, {day})',None
  a=[(int(x[0])*60+int(x[1]),int(x[2])*60+int(x[3])) for x in mm]
  o,c=a[0][0],a[-1][1]
  if c<=o: c+=1440
  return ', '.join(f'{x[0]}:{x[1]}–{x[2]}:{x[3]}' for x in mm)+f' (giờ {day} theo Google Maps)',[o,c]
def clean_addr(a):
  a=re.sub(r'^Địa chỉ:\s*','',a).strip(); a=re.sub(r',?\s*Việt Nam\s*$','',a); a=re.sub(r',\s*Hồ Chí Minh(\s*\d{5,6})?\s*$','',a); a=re.sub(r',\s*Thành phố Hồ Chí Minh.*$','',a)
  return a.strip(' ,')
def kind_of(cat,gcat='',lst=''):
  c=(cat+' '+(gcat or '')).lower(); L=lst or ''
  if L=='Photobooth date' or re.search(r'photobooth|buồng chụp|studio nhiếp|phòng ảnh|chụp ảnh film|ảnh thẻ',c): return 'photobooth'
  if L=='Spa date' or re.search(r'\bspa\b|massage|xông hơi',c): return 'spa'
  if re.search(r'công viên',(gcat or '').lower()): return 'sight'
  if L=='Homestay date' or re.search(r'khách sạn|lưu trú|homestay',c): return 'homestay'
  if L=='Workshop date' or re.search(r'workshop|lớp nấu|lớp học|cửa hàng bán nến',c): return 'workshop'
  if L=='Tổ hợp game date' or re.search(r'escape|boardgame|board game|karaoke|bowling|trượt băng|bắn cung|pickleball|leo núi|thể thao|trò chơi|game|bi-a|billiard',c): return 'game'
  if re.search(r'thú cưng|tarot',c): return 'experience'
  if re.search(r'kịch|nhạc sống|phòng trà|biểu diễn|nhà hát',c): return 'show'
  if re.search(r'rạp chiếu|phim',c): return 'cinema'
  if re.search(r'rooftop|\bbar\b|quán bar|hộp đêm|quán bia|wine|cocktail|pub',c): return 'bar'
  if re.search(r'dessert|tiệm bánh|bánh ngọt|kem|chè',c): return 'dessert'
  if re.search(r'cà phê|cafe|café|coffee|giải khát|trà sữa|tea',c): return 'cafe'
  if re.search(r'chợ đêm|street food|chợ ẩm thực',c): return 'streetfood'
  if re.search(r'nhà hàng|quán ăn|steak|bít tết|bistro|món nướng|lẩu|du thuyền nhà hàng|ẩm thực',c): return 'restaurant'
  if L=='Shopping date' or re.search(r'cửa hàng|trung tâm mua sắm|shop',c): return 'shopping'
  if re.search(r'tour|đạp xe|tarot|thú cưng|cat cafe',c): return 'experience'
  if L in('Picnic date','Check-in date') or re.search(r'đi dạo|phố|sông|ngắm|bảo tàng|nghệ thuật|công viên|sách|di tích|triển lãm|thuyền',c): return 'sight'
  return 'other'
stats=collections.Counter(); excluded=[]; unresolved=[]; dropped_closed=[]; dup_log=[]
# ---- 1. Bliss rows
recs=[]
for lst,v in bliss.items():
  raw=json.load(open(D+f'raw_bliss/{lst}.json')); pool=list(raw)
  for p in v['places']:
    stats['bliss_rows']+=1
    m=next((r for r in pool if norm(GM.get(r.get('cid'),{}).get('name') or '')==norm(p['name'])),None) or next((r for r in pool if r['name']==p['name']),None)  # place-page title (h1) first
    if not m:  # names on the list page vs place page differ slightly -> fuzzy match (difflib, normalized)
      sc=[(difflib.SequenceMatcher(None,norm(p['name']),norm(r['name'])).ratio() + (0.3 if norm(p['name']).startswith(norm(r['name'])) or norm(r['name']).startswith(norm(p['name'])) else 0),r) for r in pool]
      sc.sort(key=lambda x:-x[0])
      if sc and sc[0][0]>=0.6: m=sc[0][1]; stats['fuzzy_name_match']+=1
    if m: pool.remove(m)
    g=GM.get(m['cid'],{}) if m and m.get('cid') else {}
    cat=p['category'] or ''
    if 'vĩnh viễn' in cat or g.get('perm_closed'):
      stats['perm_closed_dropped']+=1; dropped_closed.append({'name':p['name'],'list':lst,'reason':'Đóng cửa vĩnh viễn (Google Maps)'}); continue
    if not p['rating'] and re.match(r'^\d',p['name']) and not g.get('category'):
      stats['not_a_place']+=1; unresolved.append({'name':p['name'],'list':lst,'reason':'Chỉ là một địa chỉ/điểm ghim, không phải địa điểm có tên'}); continue
    lat,lng=(m['lat'],m['lng']) if m else (None,None); cid=m.get('cid') if m else None
    hit=None
    for r in recs:
      if (cid and r['cid']==cid) or (norm(r['name'])==norm(p['name']) and (lat is None or r['lat'] is None or km(lat,lng,r['lat'],r['lng'])<0.15)): hit=r;break
    if hit:
      stats['dup_within_bliss']+=1; dup_log.append({'name':p['name'],'merged_into':hit['name'],'why':'trùng trong các list Bliss'})
      if lst not in hit['lists']: hit['lists'].append(lst); hit['source_urls'].append(v['url'])
      continue
    recs.append({'name':p['name'],'lists':[lst],'bcat':cat,'gcat':g.get('category') or ('' if 'Tạm thời' in cat else cat),'rating':fnum(p['rating']),'reviews':inum(p['reviews']),'pl':p['price_level'],
      'lat':lat,'lng':lng,'cid':cid,'temp':('Tạm thời' in cat) or bool(g.get('temp_closed')),'source_urls':[v['url']],'g':g})
out=[]
for r in recs:
  g=r['g']; addr=clean_addr(g['address']) if g.get('address') else None
  if r['lat'] is None or not addr:
    stats['unresolved']+=1; unresolved.append({'name':r['name'],'lists':r['lists'],'reason':'Không lấy được địa chỉ từ trang Google Maps công khai' if r['lat'] is not None else 'Không có toạ độ/cid','maps_url':f"https://maps.google.com/?cid={r['cid']}" if r['cid'] else None}); continue
  d=pip(r['lat'],r['lng'])
  if d is None:
    stats['excl:ngoài TP.HCM (cũ)']+=1; excluded.append({'name':r['name'],'lists':r['lists'],'address':addr,'district':None,'reason':'Ngoài TP.HCM cũ (vd. Bình Dương/Đồng Nai)','lat':r['lat'],'lng':r['lng']}); continue
  if d not in KEEP:
    stats[f'excl:{d}']+=1; excluded.append({'name':r['name'],'lists':r['lists'],'address':addr,'district':d,'reason':f'Ngoài khu trung tâm ({d})','lat':r['lat'],'lng':r['lng']}); continue
  area=LABEL.get(d,d); lst=r['lists'][0]
  kind=kind_of('',r['gcat'],lst)
  if lst in('Work date','Deep talk date') and kind=='other': kind='cafe'
  typ='food' if kind in('restaurant','cafe','bar','dessert','streetfood') else 'activity'
  pc,pn=price(r['pl']); oh,hrs=hours_of(g.get('hours'))
  cid_url=f"https://maps.google.com/?cid={r['cid']}" if r['cid'] else None
  desc=(f"{r['gcat']} · " if r['gcat'] else '')+f"Trong list “{' / '.join(r['lists'])}” của Bliss Home."
  if r['temp']: desc+=' Google Maps ghi “Tạm thời đóng cửa” – kiểm tra trước khi đi.'
  out.append({'name':r['name'],'type':typ,'category':lst,'district':area,'address':f'{addr} ({area})','price_per_couple_vnd':pc,'price_note':pn,
    'opening_hours':oh,'mood_tags':MOOD[lst],'description_vi':desc,'source_urls':r['source_urls']+([cid_url] if cid_url else []),'source':'bliss_home','out_of_area':False,
    'status':'uncertain' if r['temp'] else 'likely_operating','date_checked':TODAY,'rating':r['rating'],'reviews':r['reviews'],'lat':round(r['lat'],6),'lng':round(r['lng'],6),
    'lists':r['lists'],'google_category':r['gcat'] or None,'maps_url':cid_url,'website':g.get('website'),'area':area,'kind':kind,'hours':hrs})
  if r['temp']: stats['temp_closed_flagged']+=1
# ---- 2. base items
AREA_RE=re.compile(r'Quận \d+|Bình Thạnh|Phú Nhuận|Tân Bình|Tân Phú|Gò Vấp|Thảo Điền|Thủ Đức')
def base_area(it):
  m=AREA_RE.search(it.get('district') or '')
  if not m or it.get('out_of_area'): return None
  return 'TP Thủ Đức (Q2 cũ)' if m.group(0) in('Thảo Điền','Thủ Đức') else m.group(0)
base=[]
for src,lst in(('research',research),('web_additions',web),('new_types',newt)):
  for it in lst:
    it=dict(it); it.update(rating=it.get('rating'),reviews=it.get('reviews'),lists=it.get('lists',[]),maps_url=it.get('maps_url'),lat=None,lng=None,website=None,google_category=None,hours=None)
    it['area']=base_area(it); it['kind']='idea' if it['type']=='idea' else kind_of(it['category'])
    if it['type']=='idea': it['district']=None
    if it.get('address') and not it.get('out_of_area'):
      res=FWD.get(clean(it['address'])) or []
      if res:
        la,ln=float(res[0]['lat']),float(res[0]['lon']); pd=pip(la,ln)
        if pd and it['area'] and LABEL.get(pd,pd)==it['area']: it['lat'],it['lng']=round(la,6),round(ln,6); stats['geocoded_nominatim']+=1
    oh=it.get('opening_hours') or ''
    mm=re.match(r'^(\d{1,2}):(\d{2})\s*[–-]\s*(\d{1,2}):(\d{2})',oh)
    if mm:
      o=int(mm[1])*60+int(mm[2]); c=int(mm[3])*60+int(mm[4]); c=c+1440 if c<=o else c; it['hours']=[o,c]
    it['_src']=src; base.append(it)
# ---- 3. dedupe bliss vs base
def similar(a,b):
  A,B=norm(a['name']),norm(b['name'])
  if A==B: return True
  if len(A)>5 and len(B)>5 and (A in B or B in A):
    if a.get('lat') and b.get('lat'): return km(a['lat'],a['lng'],b['lat'],b['lng'])<0.4
    return (a.get('area')==b.get('area'))
  return False
final=[]
for b in out:
  hit=next((x for x in base if x['type']!='idea' and similar(x,b)),None)
  if hit:
    stats['dup_vs_existing']+=1; dup_log.append({'name':b['name'],'merged_into':hit['name'],'why':'Bliss trùng với mục có sẵn'})
    for k in('rating','reviews','maps_url','website','google_category','hours'): hit[k]=hit[k] or b[k]
    hit['lists']=sorted(set(hit['lists']+b['lists'])); hit['source_urls']+= [u for u in b['source_urls'] if u not in hit['source_urls']]
    if hit['lat'] is None: hit['lat'],hit['lng']=b['lat'],b['lng']
    if not hit.get('opening_hours') and b['opening_hours']: hit['opening_hours']=b['opening_hours']
    continue
  # same name inside bliss output (chains) -> disambiguate
  final.append(b)
names=collections.Counter(norm(x['name']) for x in final)
for x in final:
  if names[norm(x['name'])]>1: x['name']=f"{x['name']} ({x['area']})"
merged=base+final
for x in merged: x.pop('_src',None)
json.dump(merged,open(D+'merged_hcm.json','w'),ensure_ascii=False,indent=1)
json.dump(merged,open('/workspace/date-app/src/data.json','w'),ensure_ascii=False)
json.dump({'generated':TODAY,'note':'Bliss Home places outside central HCMC (excluded: Q12, Củ Chi, Hóc Môn, Bình Chánh, Nhà Bè, Cần Giờ, Q9 cũ, Bình Tân, ngoài TP.HCM)','excluded':excluded,'dropped_permanently_closed':dropped_closed},open(D+'excluded_hcm.json','w'),ensure_ascii=False,indent=1)
json.dump({'generated':TODAY,'unresolved':unresolved},open(D+'unresolved_bliss.json','w'),ensure_ascii=False,indent=1)
json.dump(dup_log,open(D+'duplicates_merged.json','w'),ensure_ascii=False,indent=1)
src=collections.Counter(x['source'] for x in merged)
print(dict(stats)); print('total',len(merged),'by source',dict(src))
print('by area',collections.Counter(x['area'] for x in merged).most_common())
print('kinds',collections.Counter(x['kind'] for x in merged).most_common())
print('photobooth',sum(x['kind']=='photobooth' for x in merged),'ideas',sum(x['type']=='idea' for x in merged),'latlng',sum(x['lat'] is not None for x in merged),'rating',sum(x['rating'] is not None for x in merged))

# 2026-10-26: apply price/maps/image enrichment + new ideas on top of merged data -> src/data.json
import subprocess; subprocess.run(['python3','/workspace/date-app/scripts/enrich_v3.py'],check=True)
