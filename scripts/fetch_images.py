"""Fetch one representative photo per place from its OWN public source (og:image of official website / FB page).
Downloads -> public/images/<slug>.webp (800px wide). Resumable: data/images_progress.json"""
import json, re, os, sys, io, unicodedata, html, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
ROOT='/workspace/date-app'; PROG=f'{ROOT}/data/images_progress.json'
prog=json.load(open(PROG)) if os.path.exists(PROG) else {}
items=json.load(open(f'{ROOT}/src/data.json'))
UA={'User-Agent':'Mozilla/5.0 (compatible; facebookexternalhit/1.1)','Accept-Language':'vi,en'}
def slug(s):
    s=unicodedata.normalize('NFKD',s.replace('đ','d').replace('Đ','D')).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')[:60]
def get(url,n=2_000_000):
    r=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=20); return r.geturl(), r.read(n)
SKIP=('m.me/','beacons.ai','linktr.ee','tiktok.com','instagram.com','s.shopee','campsite.bio','sites.google','framer.photos','giaodoan.vn')
def og(url):
    final,b=get(url); t=b.decode('utf-8','ignore')
    for pat in [r'<meta[^>]+property=["\']og:image(?::secure_url)?["\'][^>]+content=["\']([^"\']+)',r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image',r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)']:
        m=re.search(pat,t,re.I)
        if m: return urllib.parse.urljoin(final,html.unescape(m.group(1)))
def one(it):
    key=it['name']
    if key in prog and prog[key].get('ok') is not None: return
    w=it.get('website') or ''
    cands=[]
    if w and not any(s in w for s in SKIP): cands.append(w.split('?utm')[0])
    if not cands: prog[key]={'ok':False,'why':'no own website/FB'}; return
    for u in cands:
        try:
            img=og(u)
            if not img or img.endswith('.svg') or 'logo' in img.lower() and 'facebook' not in u: 
                if not img: continue
            _,b=get(img,8_000_000); im=Image.open(io.BytesIO(b)).convert('RGB')
            if im.width<300 or im.height<200: continue
            if im.width>800: im=im.resize((800,int(im.height*800/im.width)),Image.LANCZOS)
            fn=slug(key)+'.webp'; im.save(f'{ROOT}/public/images/{fn}','WEBP',quality=72,method=6)
            dom=urllib.parse.urlparse(u).netloc.replace('www.','')
            prog[key]={'ok':True,'image':f'/images/{fn}','image_source_url':u,'image_credit':f'Ảnh: {"Facebook " if "facebook" in dom else ""}{dom}'}; return
        except Exception as e: prog[key]={'ok':False,'why':str(e)[:120]}
    prog.setdefault(key,{'ok':False,'why':'no og:image'})
os.makedirs(f'{ROOT}/public/images',exist_ok=True)
todo=[i for i in items if i['type']!='idea']
with ThreadPoolExecutor(6) as ex: list(ex.map(one,todo))
json.dump(prog,open(PROG,'w'),ensure_ascii=False,indent=1)
print(sum(1 for v in prog.values() if v.get('ok')),'/',len(prog))
