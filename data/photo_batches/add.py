import json,sys,os
B=json.load(open('batch_01.json'));N={p['idx']:p['name'] for p in B}
f='result_01.json'
R=json.load(open(f)) if os.path.exists(f) else []
def add(idx,status,url=None,pu=None,note=None):
    R[:]=[r for r in R if r['idx']!=idx]
    r=dict(idx=idx,name=N[idx],status=status,image_url=url,contributor=None,place_url=pu or f"https://www.google.com/maps?cid={C[idx]}")
    if note:r['note']=note
    R.append(r)
C={p['idx']:p['maps_url'].split('cid=')[-1] for p in B}
def save(): json.dump(sorted(R,key=lambda r:r['idx']),open(f,'w'),ensure_ascii=False,indent=1)
