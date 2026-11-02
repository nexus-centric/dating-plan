import json
G=json.load(open('/workspace/date-app/scripts/ref/gadm41_VNM_2.json'))
NAMES={'Quận1':'Quận 1','Quận2':'Quận 2','Quận3':'Quận 3','Quận4':'Quận 4','Quận5':'Quận 5','Quận6':'Quận 6','Quận7':'Quận 7','Quận8':'Quận 8','Quận9':'Quận 9','Quận10':'Quận 10','Quận11':'Quận 11','Quận12':'Quận 12','BìnhThạnh':'Bình Thạnh','PhúNhuận':'Phú Nhuận','TânBình':'Tân Bình','TânPhú':'Tân Phú','GòVấp':'Gò Vấp','BìnhTân':'Bình Tân','BìnhChánh':'Bình Chánh','CủChi':'Củ Chi','HócMôn':'Hóc Môn','NhàBè':'Nhà Bè','CầnGiờ':'Cần Giờ','ThủĐức':'Thủ Đức (cũ)'}
FE=[f for f in G['features'] if f['properties']['NAME_1']=='HồChíMinh']
def inring(x,y,r):
  c=False;j=len(r)-1
  for i in range(len(r)):
    xi,yi=r[i];xj,yj=r[j]
    if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/(yj-yi)+xi: c=not c
    j=i
  return c
def district(lat,lng):
  for f in FE:
    g=f['geometry']; polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
    for p in polys:
      if inring(lng,lat,p[0]) and not any(inring(lng,lat,h) for h in p[1:]): return NAMES.get(f['properties']['NAME_2'],f['properties']['NAME_2'])
  return None
import re
def clean(a):
  a=re.sub(r'\(.*?\)','',a); a=re.sub(r'(Tầng|Lầu)[^,]*,','',a); a=re.sub(r'\bP\.\s?\d+,?','',a); a=re.sub(r'\bQ\.\s?(\d+)',r'Quận \1',a)
  return a.strip(' ,')+', Hồ Chí Minh'
