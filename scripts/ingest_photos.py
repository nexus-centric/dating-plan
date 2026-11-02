import json,re,io,sys,glob,urllib.request
from PIL import Image
d=json.load(open('src/data.json'))
ok=fail=0
for f in sorted(glob.glob('data/photo_batches/result_*.json')):
    for r in json.load(open(f)):
        if r.get('status')!='ok' or not r.get('image_url'): continue
        i=r['idx']; x=d[i]
        if r['name']!=x['name']: print('mismatch',i); continue
        if (x.get('image') or '').startswith('/images/gm-'): continue
        url=re.sub(r'=w\d+[^/]*$','=w900-h700-k-no',r['image_url'])
        slug=re.sub(r'[^a-z0-9]+','-',x['name'].lower()).strip('-')[:60] or 'p'
        slug=f'{slug}-{i}'
        try:
            data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read()
            im=Image.open(io.BytesIO(data)).convert('RGB'); im.thumbnail((900,900))
            path=f'public/images/gm-{slug}.webp'; im.save(path,'WEBP',quality=78)
            x.update(image='/images/gm-'+slug+'.webp',image_kind='photo',image_credit='Google Maps',image_source_url=r.get('place_url')); ok+=1
        except Exception as e: fail+=1; print('fail',i,e)
json.dump(d,open('src/data.json','w'),ensure_ascii=False,indent=1)
json.dump({str(i):{k:x.get(k) for k in ('image','image_kind','image_credit','image_source_url')} for i,x in enumerate(d) if x.get('image')},open('data/images_map.json','w'),ensure_ascii=False,indent=1)
print('ok',ok,'fail',fail,'total photos',sum(1 for x in d if x.get('image_kind')=='photo'))
