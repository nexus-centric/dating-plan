# v6: append new researched places (prices sourced 2026-10-26) + fill a few existing gaps. Append-only.
import json, re, urllib.parse
D='src/data.json'; d=json.load(open(D)); gm=json.load(open('data/gm_search_v6.json'))
C='2026-10-26'
def hrs(s):
    if not s: return None
    iv=re.findall(r'(\d\d):(\d\d) đến (\d\d):(\d\d)', s)
    if not iv: return None
    o=int(iv[-1][0])*60+int(iv[-1][1]) if len(iv)>1 else int(iv[0][0])*60+int(iv[0][1])
    a=iv[-1]; c=int(a[2])*60+int(a[3])
    if c<=o: c+=1440
    return [o,c]
def hstr(s):
    if not s: return None
    m=re.match(r'[^,]+,(.*?), Sao chép',s); return (m.group(1).replace(' đến ','–') + ' (giờ Thứ Hai theo Google Maps)') if m else None
def mk(q,name,kind,typ,cat,area,pmin,pmax,unit,cmin,cmax,src,conf,note,desc,moods,extra_src=(),addr=None,hours=None,oh=None,status='likely_operating'):
    r=gm.get(q) if q else None
    it=dict(name=name,type=typ,category=cat,district=area,address=addr,price_per_couple_vnd=cmax if cmax is not None else cmin,price_note=note,
      opening_hours=oh,mood_tags=moods,description_vi=desc,source_urls=[src,*extra_src],source='web',out_of_area=False,status=status,date_checked=C,
      rating=None,reviews=None,lists=[],maps_url=None,lat=None,lng=None,website=None,google_category=None,hours=hours,area=area,kind=kind,
      price_min=pmin,price_max=pmax,price_unit=unit,couple_min=cmin,couple_max=cmax,price_source_url=src,price_confidence=conf,price_checked=C,
      price_method='web_research_v7',maps_kind='search',image=None,note=None)
    if r and r.get('url') and '/place/' in r['url'] and not r.get('error'):
        u=r['url']; m=re.search(r'!3d([\d.]+)!4d([\d.]+)',u); h=re.search(r'0x[0-9a-f]+:(0x[0-9a-f]+)',u)
        if m: it['lat'],it['lng']=float(m.group(1)),float(m.group(2))
        if h: it['maps_url']=f'https://maps.google.com/?cid={int(h.group(1),16)}'; it['maps_kind']='direct'; it['source_urls'].append(it['maps_url'])
        if not addr and r.get('address'): it['address']=r['address'].replace('Địa chỉ: ','')
        rt=re.search(r'\n(\d,\d)\n',r.get('main',''))
        if rt: it['rating']=float(rt.group(1).replace(',','.'))
        it['google_category']=r.get('category')
        if hours is None: it['hours']=hrs(r.get('hours'))
        if oh is None: it['opening_hours']=hstr(r.get('hours'))
        if r.get('temp_closed') or r.get('perm_closed'): it['status']='uncertain'
    if not it['maps_url']:
        it['maps_url']='https://www.google.com/maps/search/?api=1&query='+urllib.parse.quote(f"{name} {addr or area} TP.HCM")
    if it['couple_min'] is None and it['couple_max'] is None and unit!='free': it['status']='uncertain'
    return it

# v7: pet cafes, theater, live music, VR, free museums, cooking. Prices sourced 2026-10-26. Append-only.
VC='https://vincom.com.vn/trend/cafe-thu-cung'; SK='https://sankhauthiendang.vn/gia-ve-kich/'; NQ='https://congbao.hochiminhcity.gov.vn/29-2026-nq-hdnd/50039'
PET=['dễ thương','ngày mưa']; SHOW=['lãng mạn','nghệ thuật']
N=[
mk('Purrfect Coffee 8 Hoa Trà Phú Nhuận','Purrfect Coffee (cafe mèo)','experience','activity','cafe thú cưng','Phú Nhuận',99000,99000,'person',198000,198000,'https://thucung.edu.vn/purrfect-coffee','medium','Buffet nước 99k/người','Cafe mèo, vé buffet đồ uống, chơi với mèo.',PET,oh='09:30–21:30',hours=[570,1290]),
mk('Tea & Pets 242 Nguyễn Thiện Thuật Quận 3','Tea & Pets (cafe thú cưng)','experience','activity','cafe thú cưng','Quận 3',40000,50000,'person',80000,100000,VC,'low','Đồ uống 40–50k (Vincom, tham khảo)','Cafe chó mèo trong hẻm Bàn Cờ.',PET,oh='09:00–21:00',hours=[540,1260]),
mk('Tokyo Pet Center 284C Nguyễn Trọng Tuyển Phú Nhuận','Tokyo Pet Center (cafe thú cưng)','experience','activity','cafe thú cưng','Phú Nhuận',35000,60000,'person',70000,120000,VC,'low','Đồ uống 35–60k (Vincom, tham khảo)','Cafe thú cưng kèm pet shop.',PET,oh='09:00–22:00',hours=[540,1320]),
mk('Cherry Pet Coffee 212 Nguyễn Tri Phương Quận 10','Cherry Pet Coffee (chó, mèo, capybara)','experience','activity','cafe thú cưng','Quận 10',40000,None,'person',80000,None,'https://cherrypetcoffee.com/','low','Đồ uống từ 40k; có thể phụ thu khu capybara','Cafe chó mèo và capybara.',PET,['https://muctim.tuoitre.vn/5-quan-ca-phe-meo-sieu-yeu-tai-tphcm-danh-cho-cac-sen-101250508194849995.htm'],oh='08:00–22:00',hours=[480,1320]),
mk(None,'Yuna Alaska Coffee (cafe chó)','experience','activity','cafe thú cưng','Bình Thạnh',45000,65000,'person',90000,130000,'https://mytour.vn/vi/blog/bai-viet/yuna-alaska-coffee-thu-cung-de-thuong-so-1-sai-gon.html','low','45–65k/đồ uống','Cafe chó Alaska/Husky.',PET,addr='58 Nguyễn Gia Trí, Bình Thạnh',oh='08:30–22:30',hours=[510,1350],status='uncertain'),
mk('Sân khấu kịch Hoàng Thái Thanh 139 Bắc Hải','Sân khấu kịch Hoàng Thái Thanh','show','activity','xem kịch','Quận 10',270000,350000,'person',540000,700000,SK,'medium','Vé 270–350k (bảng giá tổng hợp); cityguide ghi 280k','Kịch tâm lý xã hội, suất tối cuối tuần.',SHOW),
mk('Sân khấu kịch 5B Võ Văn Tần','Sân khấu kịch Nhỏ 5B Võ Văn Tần','show','activity','xem kịch','Quận 3',200000,350000,'person',400000,700000,SK,'low','200–350k/vé (bảng giá tổng hợp)','Sân khấu kịch nhỏ lâu đời.',SHOW),
mk('Sân khấu kịch Thế Giới Trẻ','Sân khấu Thế Giới Trẻ','show','activity','xem kịch','Quận 1',200000,350000,'person',400000,700000,SK,'low','200–350k/vé (bảng giá tổng hợp)','Kịch hài, kịch kinh dị.',SHOW),
mk('Sân khấu Trống Đồng','Sân khấu Trống Đồng','show','activity','xem kịch','Quận 3',100000,250000,'person',200000,500000,SK,'low','100–250k/vé (bảng giá tổng hợp)','Kịch, cải lương, suất tối.',SHOW),
mk('Phòng trà Đồng Dao 164 Pasteur','Phòng trà Đồng Dao','show','nightlife','nhạc sống/phòng trà','Quận 1',40000,120000,'person',80000,240000,'https://trumreview.com/phong-tra-sai-gon/','low','Đồ uống 40–120k (tham khảo)','Phòng trà acoustic nhỏ, ca sĩ trẻ.',SHOW),
mk('Phòng trà Bến Thành 6 Mạc Đĩnh Chi','Phòng trà Bến Thành','show','nightlife','nhạc sống/phòng trà','Quận 1',120000,None,'person',240000,None,'https://www.vietnamairlines.com/vn/vi/travel-guide/phong-tra-sai-gon','low','Phụ thu đêm acoustic ~120k/người, chưa gồm đồ uống','Phòng trà nhạc trữ tình.',SHOW),
mk('Carmen Bar 8 Lý Tự Trọng','Carmen Bar (nhạc Latin sống)','show','nightlife','nhạc sống','Quận 1',150000,200000,'person',300000,400000,'https://kamereo.vn/blog/carmen-bar','low','Không vé vào; đồ uống 150–200k','Bar ban nhạc Latin/flamenco sống mỗi tối.',['lãng mạn','đêm muộn']),
mk('VRena Hà Đô Centrosa','VRena Hà Đô Centrosa (VR)','game','activity','thực tế ảo VR','Quận 10',220000,330000,'person',440000,660000,'https://vre-vietnam.com/vi/dia-diem/vrena-ha-do-centrosa','medium','30 phút: 220k (ngày thường ban ngày), 290k tối, 330k cuối tuần','Khu chơi VR nhiều người, bắn súng/đua xe.',['năng động']),
mk('Bảo tàng Hồ Chí Minh Bến Nhà Rồng','Bảo tàng Hồ Chí Minh – Bến Nhà Rồng','sight','sight','bảo tàng','Quận 4',0,0,'free',0,0,NQ,'medium','Không thuộc danh mục thu phí NQ 29/2026 (tham quan miễn phí)','Bảo tàng ven sông, view Bến Nhà Rồng.',['yên tĩnh'],status='likely_operating'),
mk('Bảo tàng Tôn Đức Thắng','Bảo tàng Tôn Đức Thắng','sight','sight','bảo tàng','Quận 1',0,0,'free',0,0,NQ,'medium','Không thuộc danh mục thu phí NQ 29/2026 (miễn phí)','Bảo tàng nhỏ cạnh bờ sông Bạch Đằng.',['yên tĩnh']),
mk('Saigon Cooking Class 80/1 Nguyễn Trãi','Saigon Cooking Class','workshop','activity','lớp nấu ăn','Quận 1',840000,840000,'person',1680000,1680000,'https://saigoncookingclass.com/our-services/cooking-class/','high','840k/người (vượt trần 1tr/2 người)','Lớp nấu 3 món Việt, sáng/chiều.',['đặc biệt']),
]
base=len(d)
for it in N: d.append(it)
def upd(i,name,**kw):
    assert d[i]['name']==name,(i,d[i]['name'])
    old=(d[i].get('couple_min'),d[i].get('couple_max'))
    srcs=kw.pop('src',[])
    d[i].update(kw); d[i]['price_checked']=C
    if srcs: d[i]['price_source_url']=srcs[0]; d[i]['source_urls']=list(dict.fromkeys(srcs+(d[i].get('source_urls') or [])))
    print(f"{i} {name}: {old} -> {(d[i].get('couple_min'),d[i].get('couple_max'))}")
for i,n in ((40,'Bảo tàng Mỹ thuật TP.HCM'),(41,'Bảo tàng Chứng tích Chiến tranh'),(119,'Bảo tàng Thành phố Hồ Chí Minh (Dinh Gia Long)')):
    upd(i,n,price_note='60.000đ/người/lượt theo NQ 29/2026/NQ-HĐND, hiệu lực 01/10/2026',price_confidence='high',src=[NQ,'https://ticket.baotangchungtichchientranh.vn/terms-and-conditions.html','https://hcmc-museum.edu.vn/luu-tru/5482','https://baotangmythuattphcm.com.vn/tham-quan'])
upd(84,'Sân khấu kịch IDECAF',price_min=300000,price_max=350000,couple_min=600000,couple_max=700000,price_per_couple_vnd=700000,price_confidence='high',price_note='Vé 300k/350k (giá chính thức) [cũ: 250–450k]',src=['https://kichidecaf.com/'])
upd(44,'Tipsy Art',price_unit='couple',price_min=770000,price_max=770000,couple_min=770000,couple_max=770000,price_per_couple_vnd=770000,price_confidence='high',price_note='Gói vẽ đôi 770k; art jam 300k/3h; lẻ 440k/người [cũ 880k]',src=['https://tipsyart.vn/'])
upd(117,'Phòng trà Không Tên',price_min=50000,price_max=150000,couple_min=100000,couple_max=300000,price_per_couple_vnd=300000,price_unit='person',price_confidence='low',price_note='50–150k/người tham khảo; đêm ca sĩ lớn đắt hơn [cũ: không có giá]',src=['https://www.vietnamairlines.com/vn/vi/travel-guide/phong-tra-sai-gon'])
upd(83,'Acoustic Bar Ngô Thời Nhiệm',price_min=90000,price_max=200000,couple_min=180000,couple_max=400000,price_per_couple_vnd=400000,price_note='Không vé vào; đồ uống 90–200k [cũ 80–180k]',src=['https://district0.me/acoustic-bar'])
upd(203,'Timezone Vincom Đồng Khởi',price_min=100000,couple_min=100000,price_note='Không vé vào; thẻ từ 100k, gói 250k→300k, 350k→450k credit; 10:00–22:00',src=['https://timezonegames.com/vn/faq'])
upd(396,'Karaoke ICOOL Phan Xích Long',price_min=59000,couple_min=118000,price_note='Giờ vàng từ 59k/giờ (2 giờ ~118k); giờ thường 150–300k/giờ',src=['https://karaokektv.vn/karaoke-icool-266-268-270-phan-xich-long/'])
upd(368,'Phở Quỳnh',price_min=79000,price_max=89000,couple_min=158000,couple_max=178000,price_per_couple_vnd=178000,price_confidence='medium',price_note='79–89k/tô [cũ ~80k]',src=['https://vietnammm.com/pho-quynh-sai-gon/'])
upd(373,'Bánh Xèo Ăn Là Ghiền',price_min=60000,price_max=90000,couple_min=120000,couple_max=180000,price_per_couple_vnd=180000,price_note='60–90k/phần [cũ ~80k]',src=['https://www.foody.vn/ho-chi-minh/banh-xeo-an-la-ghien'])
upd(365,'Bột Chiên Đạt Thành',price_min=35000,price_max=40000,couple_min=70000,couple_max=80000,price_confidence='medium',price_note='35k (1 trứng) / 40k (2 trứng) [cũ 40k]',src=['https://danviet.vn/bot-chien-dat-thanh'])
upd(369,'Cơm Tấm Phúc Lộc Thọ',status='uncertain',note='Foody/MoMo ghi cơ sở 458 Lê Văn Sỹ (Tân Bình) giá 32–139k, khác địa chỉ 339 Lê Văn Sỹ đang lưu – cần xác minh')
json.dump(d,open(D,'w'),ensure_ascii=False,indent=1)
print('added',len(N),'from idx',base,'total',len(d))
