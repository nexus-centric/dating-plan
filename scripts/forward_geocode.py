# Forward-geocode addresses of research + web items via Nominatim (1 req/s). Accept only if the result falls in the stated district.
import json,time,urllib.request,urllib.parse,os,re,sys
sys.path.insert(0,os.path.dirname(__file__)); from geo_util import district
D='/workspace/date-app/data/'; cache=D+'raw_bliss/_forward_cache.json'
C=json.load(open(cache)) if os.path.exists(cache) else {}
items=json.load(open(D+'research_hcm.json'))+json.load(open(D+'web_additions.json'))+json.load(open(D+'new_types_hcm.json'))
def clean(a):
  a=re.sub(r'\(.*?\)','',a); a=re.sub(r'(Tầng|Lầu)[^,]*,','',a); a=re.sub(r'\bP\.\s?\d+,?','',a); a=re.sub(r'\bQ\.\s?(\d+)',r'Quận \1',a)
  return a.strip(' ,')+', Hồ Chí Minh'
for it in items:
  if not it.get('address') or it.get('out_of_area'): continue
  q=clean(it['address'])
  if q in C: continue
  u='https://nominatim.openstreetmap.org/search?format=jsonv2&limit=1&countrycodes=vn&q='+urllib.parse.quote(q)
  try: C[q]=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'hcm-date-app-demo/0.1 (personal, low volume)'})))
  except Exception as e: print(e); C[q]=[]
  json.dump(C,open(cache,'w'),ensure_ascii=False); time.sleep(1.1)
print('done',len(C))
