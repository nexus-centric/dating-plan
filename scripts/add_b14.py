"""b14: Ovenmaru Chicken + similar Korean fried/roasted chicken & chimaek places with social/review sources.
Inputs: data/b14/verify.json (live Google Maps check via scripts/gm_verify_b14.cjs). Appends only; idempotent."""
import json, re, shutil, os, io, unicodedata, urllib.request
from PIL import Image
D='src/data.json'; TODAY='2026-11-02'
if not os.path.exists('tmp/data-before-b14.json'): shutil.copy(D,'tmp/data-before-b14.json')
d=json.load(open(D)); V=json.load(open('data/b14/verify.json'))
have={x['name'] for x in d}
def norm(s): s=unicodedata.normalize('NFD',s or '').lower(); s=''.join(c for c in s if unicodedata.category(c)!='Mn').replace('đ','d'); return re.findall(r'[a-z0-9]+',s)
def slug(s): return '-'.join(norm(s))[:50]
def photo(url,s):
    out=f'public/images/b14-{s}.webp'
    if os.path.exists(out): return '/'+out[7:]
    try:
        url=re.sub(r'=w\d+-h\d+[^&]*$','=w800-h800-k-no',url)
        b=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read()
        im=Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((800,800)); im.save(out,'WEBP',quality=78); return '/'+out[7:]
    except Exception as e: print('photo fail',s,e); return None
BAD_PHOTO={'pacho'}  # Maps hero showed a different shop sign (Cheat Code); checked by eye 2026-11-02
# key, display name, area, pmin, pmax (per person), price source, confidence, price note, social sources, mood, description
P=[
('ovenmaru-q1','Ovenmaru Chicken – Điện Biên Phủ','Quận 1',120000,220000,'https://www.foody.vn/ho-chi-minh/oven-maru-chicken-am-thuc-han-quoc','medium','Foody: món 40k–300k; gà nướng lò ~170–190k/phần nhỏ (đủ 2 người), có panchan miễn phí',
 ['https://www.foody.vn/ho-chi-minh/oven-maru-chicken-am-thuc-han-quoc','https://www.facebook.com/ovenmaruvn','https://saigonreview.vn/topAZ/quan-ga-ran-han-quoc-ngon-o-tp-hcm'],['hẹn hò','ăn no'],'Gà nướng lò kiểu Hàn (ít dầu) lâu năm ở Đa Kao; kèm kimchi, salad, củ cải miễn phí. Foody 8.2/10 (754 bình luận).'),
('ovenmaru-anphu','Ovenmaru Chicken – An Phú','TP Thủ Đức (Q2 cũ)',120000,220000,'https://www.foody.vn/ho-chi-minh/oven-maru-chicken-nguyen-quy-canh/thuc-don','medium','Foody: món 40k–300k; menu chi nhánh (FlipHTML5 2022) gà 170k–340k/phần',
 ['https://www.foody.vn/ho-chi-minh/oven-maru-chicken-nguyen-quy-canh/thuc-don','https://fliphtml5.com/ixdtz/noes/OVENMARU_Chicken_menu_2022_online/'],['hẹn hò','ăn no'],'Chi nhánh Ovenmaru ở An Phú (Q2 cũ): gà nướng lò Hàn Quốc, cơm kimchi phô mai, tokbokki.'),
('kjeju-q1','K-Jeju Chicken – Tôn Thất Đạm','Quận 1',200000,300000,'https://kjejuchicken.com/thuc-don','medium','Menu chính thức: gà 421k–497k/phần cho 2–3 người, nửa con 259k; mở tới khuya',
 ['https://www.facebook.com/garankjejuchicken','https://kjejuchicken.com/'],['đêm muộn','ăn no'],'Chimaek kiểu Hàn: gà rán sốt + bia tuyết; mở muộn, có phòng riêng.'),
('kjeju-q7','K-Jeju Chicken – Phú Mỹ Hưng','Quận 7',200000,300000,'https://kjejuchicken.com/thuc-don','medium','Menu chính thức (chuỗi): gà 421k–497k/phần cho 2–3 người, nửa con 259k',
 ['https://mosia.io/k-jeju-chicken/','https://kjejuchicken.com/'],['đêm muộn','ăn no'],'Chi nhánh K-Jeju ở Hưng Vượng 2 (PMH): gà rán Hàn + bia tuyết, không gian rộng.'),
('chickentalk','Chicken Talk 치킨톡 – Lê Văn Lương','Quận 7',120000,200000,'https://www.chickentalkvietnam.com/menu?menu=menu','medium','Menu chính thức: gà 160k (M)–300k (L), combo từ 240k',
 ['https://www.foody.vn/ho-chi-minh/chicken-talk-ga-ran-le-van-luong.w1ralx','https://www.momo.vn/page/1054063'],['ăn no','vui vẻ'],'Quán gà rán Hàn Quốc ở Q7 (gần PMH); gà chiên xù, gà hun khói, mì tương đen, tokbokki, bia.'),
('donchicken-pxl','Don Chicken – Phan Xích Long','Phú Nhuận',120000,200000,'https://www.donchicken.vn/pages/order','medium','Website: gà rán 189k, gà sốt 209k, không xương 199k; Foody 76k–330k',
 ['https://www.foody.vn/ho-chi-minh/don-chicken-nha-hang-ga-nuong-han-quoc-phan-xich-long','https://dineout.grab.com/vn/vi/restaurants/don-chicken-phan-xich-long--5-C2VJN7DFLTXUT6'],['hẹn hò','ăn no'],'Chuỗi gà nướng/gà rán Hàn Quốc trên phố ẩm thực Phan Xích Long.'),
('bonchon-ltt','Bonchon – Lý Tự Trọng','Quận 1',115000,230000,'https://bonchon.com.vn/loai-san-pham/combo','medium','Website: combo gà S 139k / M 229k / L 339k',
 ['https://www.facebook.com/bonchon.vn','https://saigonreview.vn/topAZ/quan-ga-ran-han-quoc-ngon-o-tp-hcm'],['ăn no'],'Chuỗi gà rán Hàn Quốc nổi tiếng (cánh gà sốt tỏi xì dầu) ngay trung tâm Q1.'),
('bonchon-ngt','Bonchon – Nguyễn Gia Trí','Bình Thạnh',115000,230000,'https://bonchon.com.vn/loai-san-pham/combo','medium','Website: combo gà S 139k / M 229k / L 339k',
 ['https://www.facebook.com/bonchon.vn','https://exa.ai/library/places?q=ca2811277cbba9c3'],['ăn no'],'Bonchon trên đường Nguyễn Gia Trí (D2 cũ), khu sinh viên Bình Thạnh.'),
('goobne-nvc','Goobne Chicken – Nguyễn Văn Cừ','Quận 1',100000,200000,'https://emdoi.vn/goobne-chicken/','medium','Blog: món 100k–300k; gà truyền thống ~150–160k, UFO cheese fondue 330k',
 ['https://www.foody.vn/bai-viet/lan-tron-trong-the-gioi-ga-han-quoc-ngap-tran-pho-mai-chinh-hieu-cua-goobne-chicken-18962','https://www.facebook.com/goobnevn/'],['hẹn hò','ăn no'],'Gà nướng lò Hàn Quốc, nổi tiếng món gà UFO phô mai kéo sợi.'),
('otoke-pvt','Gà Rán Otoké – Phan Văn Trị','Bình Thạnh',75000,150000,'https://www.otokechicken.vn/','medium','Website: combo 4 miếng 145k, 6 miếng 215k',
 ['https://tadiha.com/otoke-chicken-ga-ran-han-quoc-phan-van-tri-pd36017.htm','https://www.facebook.com/otokechicken/'],['bình dân','ăn no'],'Gà rán sốt Hàn giá mềm, hợp bữa tối nhanh.'),
('chivago-q1','Chivago Chicken – Nguyễn Thái Học','Quận 1',100000,250000,'https://www.foody.vn/ho-chi-minh/chivago-chicken-ga-ran-han-quoc-bia','medium','Foody: 100k–500k; gà rán 184k–205k/phần (beFood)',
 ['https://www.foody.vn/ho-chi-minh/chivago-chicken-ga-ran-han-quoc-bia/binh-luan','https://www.threads.net/@chivagovn'],['đêm muộn','ăn no'],'Chi nhánh Q1 của Chivago (gà rán Hàn & bia); Foody 8.5/10.'),
('pacho','Pacho Pocha Express 파초포차 – Thảo Điền','TP Thủ Đức (Q2 cũ)',100000,300000,'https://chungcuquan2.vn/review-pacho-pocha-quan-2-dia-diem-an-uong-sam-uat-tai-thao-dien/','medium','Review: 50k–300k/người; gà rán sốt cay, mì tương đen, soju',
 ['https://chungcuquan2.vn/review-pacho-pocha-quan-2-dia-diem-an-uong-sam-uat-tai-thao-dien/','https://us.trip.com/restaurant/vietnam/ho-chi-minh-city/detail/pacho-pocha-express-148098233/'],['đêm muộn','vui vẻ'],'Pocha (quán nhậu vỉa hè kiểu Hàn) ở Thảo Điền: gà rán, tokbokki, soju.'),
('papas-ntp',"Papas' Chicken – Nguyễn Tri Phương",'Quận 10',100000,200000,'https://mytour.vn/vi/blog/bai-viet/top-10-dia-diem-am-thuc-tuyet-voi-tren-duong-nguyen-tri-phuong-mytour.html','medium','Mytour: 100k–200k/người; gà rán KX sốt gia vị 170k (WebReview)',
 ['https://webreview.vn/ga-ran-kx-sot-gia-vi-papas-chicken-ga-ran-han-quoc-nguyen-tri-phuong.html','https://www.momo.vn/page/9891139'],['ăn no','vui vẻ'],'Chuỗi gà rán Hàn Quốc lâu năm, gà phô mai, có bán ½ phần 2 vị.'),
('gaxeo-hbt','GAXEO Chicken & Beer – Hai Bà Trưng','Quận 3',120000,200000,'https://tadiha.com/gaxeo-chicken-beer-amp-bbq-hai-ba-trung-pd36343.htm','low','Review cũ: gà phô mai 185k, tokbokki 150k (chưa có menu cập nhật)',
 ['https://tadiha.com/gaxeo-chicken-beer-amp-bbq-hai-ba-trung-prv36343.htm','https://mytour.vn/vi/blog/bai-viet/dan-dau-xu-huong-10-quan-ga-han-quoc-tai-sai-gon-ma-ban-khong-the-bo-qua.html'],['đêm muộn','ăn no'],'Gà phô mai & bia 2 tầng rộng ở Q3.'),
('shaepi',"S'haepi Chikin – Nguyễn Sơn Hà",'Quận 3',60000,120000,'https://www.momo.vn/page/9802062','low','MoMo: chi tiêu TB ~60k/người (gà rán sốt Hàn); chưa có menu đầy đủ',
 ['https://www.momo.vn/page/9802062','https://mytour.vn/vi/blog/bai-viet/6-dia-chi-hang-dau-de-thuong-thuc-ga-ran-ngon-tai-quan-3-tp-hcm.html'],['bình dân','ăn vặt'],'Quán gà rán sốt Hàn nhỏ (3 vị: truyền thống, cay, tương tỏi) trong hẻm Q3.'),
]
log=[]
for k,nm,area,pmin,pmax,src,conf,pn,social,mood,desc in P:
    v=V.get(k) or {}
    if nm in have: continue
    if not v.get('name') or v.get('perm_closed') or v.get('temp_closed') or not v.get('lat'): log.append(('skip',nm,v.get('name'))); continue
    r=float(v['rating'].replace(',','.')) if v.get('rating') else None
    it=dict(type='food',name=nm,kind='restaurant',category='nhà hàng',google_category=v.get('category') or 'Nhà hàng Hàn Quốc',district=area,area=area,
        address=(v.get('address') or '').replace('Địa chỉ: ',''),lat=v['lat'],lng=v['lng'],maps_url=v['url'],maps_kind='direct' if '/place/' in v['url'] else 'search',
        rating=r,reviews=None,price_min=pmin,price_max=pmax,price_unit='person',couple_min=pmin*2,couple_max=pmax*2,price_per_couple_vnd=None,price_note=pn,
        price_source_url=src,price_confidence=conf,price_method='web_source',price_checked=TODAY,opening_hours=None,hours=None,
        mood_tags=mood+['món Hàn'],source='b14',source_urls=list(dict.fromkeys(social+[src,v['url']])),social_review_urls=social,out_of_area=False,status='likely_operating',
        date_checked=TODAY,added=TODAY,lists=[],website=None,discovered_via='b14: Ovenmaru + quán gà Hàn/chimaek có review mạng xã hội; Google Maps verify',
        description_vi=desc,note=f"Google Maps {TODAY}: '{v['name']}' đang hoạt động, rating {v.get('rating')}. Số đánh giá Maps chưa đọc được (chế độ hạn chế).")
    if k=='chickentalk': it['note']+=' Nguồn blog ghi 502 Lê Văn Lương; Maps hiện 479 Lê Văn Lương.'
    if v.get('img') and k not in BAD_PHOTO:
        im=photo(v['img'],slug(nm))
        if im: it.update(image=im,image_credit='Google Maps',image_source_url=v['url'],image_kind='photo')
    have.add(nm); d.append(it); log.append(('add',area,nm))
json.dump(d,open(D,'w'),ensure_ascii=False,indent=1)
json.dump(log,open('data/b14/add_log.json','w'),ensure_ascii=False,indent=1)
for l in log: print(l)
