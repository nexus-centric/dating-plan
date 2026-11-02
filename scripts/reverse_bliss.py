import json,glob,time,urllib.request,urllib.parse,os
cache='/workspace/date-app/data/raw_bliss/_reverse_cache.json'
C=json.load(open(cache)) if os.path.exists(cache) else {}
for f in glob.glob('/workspace/date-app/data/raw_bliss/*date.json'):
  for p in json.load(open(f)):
    k=f"{p['lat']:.6f},{p['lng']:.6f}"
    if k in C: continue
    u="https://nominatim.openstreetmap.org/reverse?format=jsonv2&zoom=18&addressdetails=1&accept-language=vi&lat=%s&lon=%s"%(p['lat'],p['lng'])
    try: C[k]=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'hcm-date-app-demo/0.1 (personal, low volume)'})))
    except Exception as e: print(e)
    json.dump(C,open(cache,'w'),ensure_ascii=False); time.sleep(1.1)
print('done',len(C))
