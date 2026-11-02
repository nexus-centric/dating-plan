import json,io,urllib.request,re
from PIL import Image
d=json.load(open('src/data.json'))
def area_of(dist):
    for x in d:
        if x.get('district')==dist and x.get('area'): return x['area']
def dl(url,slug):
    url=re.sub(r'=w\d+[^/]*$','=w1200-h900-k-no',url)
    data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read()
    im=Image.open(io.BytesIO(data)).convert('RGB'); im.thumbnail((900,700))
    p=f'public/images/gm-{slug}.webp'; im.save(p,'WEBP',quality=78); print(slug,im.size); return '/images/gm-'+slug+'.webp'
C='Google Maps 27/10/2026: '
def upd(i,**kw):
    x=d[i]; note=kw.pop('addnote',None); img=kw.pop('img',None)
    if img:
        x.update(image=dl(img,f'{i}-b12'),image_kind='photo',image_credit='Google Maps',image_source_url=kw.get('maps_url',x.get('maps_url')))
    x.update(kw); x['date_checked']='2026-10-27'
    if note: x['note']=((x.get('note') or '')+' | '+C+note).strip(' |')
# Timeo
upd(79,address='29/23 Đoàn Thị Điểm, P. Cầu Kiệu, Phú Nhuận',district='Phú Nhuận',area=area_of('Phú Nhuận'),lat=10.799242,lng=106.6824689,
    maps_url='https://www.google.com/maps/place/Timeo+%7C+Tufting+Studio+%7C+HCMC/@10.799242,106.6824689,17z/data=!3m1!4b1!4m6!3m5!1s0x317529601acb4b33:0xfd6b3763eaf076e7!8m2!3d10.799242!4d106.6824689!16s%2Fg%2F11vx4trhft',
    maps_kind='direct',status='likely_operating',rating=5.0,reviews=244,opening_hours='T3–CN 10:00–19:00, nghỉ T2',
    img='https://lh3.googleusercontent.com/grass-cs/AABkmLeJlngQSkAu0pXFT8bdkMP31lkbw9L50NcbFVTr9bp4dQrrsfkfrxR30UkzgMbRRt2niR2FH38yEmX8w-VNEwIr3cNjROWNGmJR1BCb1j4OgncQQsv37IRzmpbFdGtcLHVquDpk9w=w408-h363-k-no',
    addnote='đang hoạt động tại 29/23 Đoàn Thị Điểm (5.0, 244 review, review mới ~3 tuần), mở T3–CN 10–19h')
# Chạm Cọ
upd(339,address='14G Đặng Văn Ngữ, Phú Nhuận (chi nhánh 2: 39/29 Nguyễn Trãi, Q1)',lat=10.7966617,lng=106.6696505,
    maps_url='https://www.google.com/maps/place/Ch%E1%BA%A1m+C%E1%BB%8D+workshop/@10.7966617,106.6696505,17z/data=!3m1!4b1!4m6!3m5!1s0x3175290015054f81:0xf215057890add56a!8m2!3d10.7966617!4d106.6696505!16s%2Fg%2F11z7h07qzz',
    maps_kind='direct',status='likely_operating',rating=4.8,reviews=97,
    img='https://lh3.googleusercontent.com/grass-cs/AABkmLduYs7bOZxA081HDmu4sdT60hZrXsI8JBIwWpZfdVWSrD-wNzx4ifGisSC3nY700BEaS78faCoOKM-Q9g2pDI_aFONy0TwKC-TSZ3H_P26dnQt9-CqHf7t0YIeeR5D4Xyex1cGBbGKSVMF8=w408-h306-k-no',
    addnote='đang hoạt động ở 14G Đặng Văn Ngữ (4.8, 97 review, review mới 8 ngày) và 39/29 Nguyễn Trãi Q1 (4.9, 34 review)')
# NOIRE
upd(335,name='NOIRE Cafe & Bistro - The Mett',address='Tòa The Mett, 15 Trần Bạch Đằng, An Khánh (Thủ Thiêm), TP Thủ Đức',lat=10.7781644,lng=106.7139747,
    maps_url='https://www.google.com/maps/place/NOIRE+Cafe+%26+Bistro+-+The+Mett/@10.7781644,106.7139747,17z/data=!3m1!4b1!4m6!3m5!1s0x31752fd53149c0f3:0x62378b38a492d202!8m2!3d10.7781644!4d106.7139747!16s%2Fg%2F11wfhg0xr8',
    maps_kind='direct',status='likely_operating',rating=4.7,reviews=792,
    img='https://lh3.googleusercontent.com/grass-cs/AABkmLci73cdvmWGfbd5XrwINvyBSSFXPxazeKMkNYMztQfhxY65DU_-yXNXCoDXUBnET5wq_P_Nu4LqNeeyRf5-x155CtyvsQgGCbmEWsYVLXPDqaPXIIejzXYMcGKW32EE92dOmesGbxd-Unu4=w408-h612-k-no',
    addnote='đang hoạt động ở The Mett 15 Trần Bạch Đằng (4.7, 792 review); Maps ghi giá ₫1–400k/người')
# closed / hidden
upd(402,status='closed',addnote='Candleholic chỉ có ở Hà Nội (120 Bùi Thị Xuân HBT, 30 Xuân Diệu Tây Hồ); 14 Đặng Dung Q1 không có cửa hàng → ẩn')
upd(416,status='closed',addnote='Tea & Pet báo "Đóng cửa vĩnh viễn" (đóng ~1/2021) → ẩn')
upd(14,status='closed',addnote='không có Lavender ở 384/40 NKKN, chỉ có Lavender Coffee & Tea House ở 137 Trần Huy Liệu (quán khác) → ẩn')
upd(63,status='closed',addnote='không có SAY CHEESE ở 38 Nguyễn Trãi Q1 (chỉ có chi nhánh Hải Phòng) → ẩn')
# Saigon Saigon photo
upd(385,img='https://lh3.googleusercontent.com/gps-cs-s/ANWiy9T4XkmDaUhOTsJOpZU-V1Jm8pzQ-A0xI7F4N_p7wek_kdzB5JAFQ-Li5KcWTqs1wYcXahKPKQUmy7d1CSdPeuETn8Kud32UGTUN-akdpGzrhkOxr_P8AGGvqhyNUsOwo0IGg_xusVD-kTM=w203-h152-k-no',
    addnote='đang hoạt động (4.0, 173 review), giá Maps ₫200–700k/người; đổi ảnh sang không gian quầy bar')
json.dump(d,open('src/data.json','w'),ensure_ascii=False,indent=1)
print('visible',sum(1 for x in d if x.get('status')!='closed'),'with image',sum(1 for x in d if x.get('status')!='closed' and x.get('image')))
