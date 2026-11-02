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
      price_method='web_research_v6',maps_kind='search',image=None,note=None)
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
V='https://vietnammm.com/'; SH='https://saigonhomestay.com/best-street-food-in-saigon/'
F=lambda: None
N=[
# ---- cheap dinners ----
mk('Cơm tấm Ba Ghiền 84 Đặng Văn Ngữ','Cơm Tấm Ba Ghiền','restaurant','food','cơm tấm','Phú Nhuận',75000,145000,'person',150000,290000,V+'com-tam-ba-ghien/','medium','Cơm sườn ~81k, thập cẩm 145k/phần (vietnammm 8/2026)','Cơm tấm sườn cốt lết nướng than, Michelin Bib Gourmand.',['rẻ mà vui'],[SH]),
mk('Phở Hòa Pasteur Quận 3','Phở Hòa Pasteur','restaurant','food','phở','Quận 3',75000,105000,'person',150000,210000,V+'pho-hoa-pasteur/','medium','Tô thường 75–90k, tô lớn 90–105k','Phở bò Nam Bộ từ 1968, Michelin Bib Gourmand.',['rẻ mà vui','đêm muộn'],[SH]),
mk('Phở Lệ Nguyễn Trãi Quận 5','Phở Lệ (Nguyễn Trãi)','restaurant','food','phở','Quận 5',75000,75000,'person',150000,150000,SH,'medium','Tô ~75k (saigonhomestay, xác minh 6/2026)','Phở bò nổi tiếng Chợ Lớn, mở đến nửa đêm.',['rẻ mà vui','đêm muộn']),
mk('Hủ tiếu Nam Vang Nhân Quán Quận 3','Nhân Quán – Hủ Tiếu Nam Vang','restaurant','food','hủ tiếu','Quận 3',55000,85000,'person',110000,170000,'https://www.vietnamtourism.com/vi/an-hu-tieu-o-sai-gon-10-quan-nguoi-ia-phuong-tin-tuong','medium','55–75k/tô, tô đầy đủ ~85k','Hủ tiếu Nam Vang khô/nước lâu năm.',['rẻ mà vui'],['https://nhahanghonghanh.vn/hu-tieu-nam-vang-cach-mang-thang-8/']),
mk('Hủ tiếu Hồng Phát Võ Văn Tần Quận 3','Hủ Tiếu Hồng Phát (Võ Văn Tần)','restaurant','food','hủ tiếu','Quận 3',50000,50000,'person',100000,100000,SH,'medium','~50k/tô (saigonhomestay)','Hủ tiếu Nam Vang quán gia đình Bàn Cờ.',['rẻ mà vui']),
mk('Bánh mì Huỳnh Hoa Quận 1','Bánh Mì Huỳnh Hoa','streetfood','food','bánh mì','Quận 1',35000,68000,'person',70000,136000,SH,'medium','35–68k/ổ','Ổ bánh mì “khủng” nổi tiếng Sài Gòn, mua mang đi ăn khi dạo phố.',['rẻ mà vui']),
mk('Bánh xèo Đinh Công Tráng Quận 1','Bánh Xèo 46A','restaurant','food','bánh xèo','Quận 1',80000,110000,'person',160000,220000,SH,'medium','80–110k/phần','Bánh xèo miền Tây giòn rụm, quán lâu đời.',['rẻ mà vui']),
mk('Ốc Oanh Vĩnh Khánh Quận 4','Ốc Oanh (Vĩnh Khánh)','restaurant','food','ốc / hải sản','Quận 4',100000,250000,'dish',200000,500000,V+'oc-oanh-vinh-khanh/','medium','Món ốc 100–250k (ước 2 món/2 người); hỏi giá trước khi gọi','Quán ốc Michelin Selected trên phố ốc Vĩnh Khánh.',['năng động','đêm muộn'],['https://vnexpress.net/pho-oc-dem-vinh-khanh-tap-nap-khach-5004873.html']),
mk('Bún chả Hà Nội 26 Lê Văn Sỹ','Bún Chả Hà Nội 26','restaurant','food','bún chả','Quận 1',45000,70000,'person',90000,140000,'https://travel.com.vn/tin-tuc-du-lich/bun-cha-ha-noi-v18342.aspx','low','45–70k/suất','Bún chả nướng than kiểu Hà Nội.',['rẻ mà vui']),
mk('Bún riêu Gánh Bến Thành','Bún Riêu Gánh Chợ Bến Thành','streetfood','food','bún riêu','Quận 1',35000,57000,'person',70000,114000,'https://webreview.vn/bun-rieu-ganh-ben-thanh-le-thanh-ton.html','medium','35–40k/tô, thêm topping ~57k','Bún riêu gánh lâu đời cạnh chợ Bến Thành.',['rẻ mà vui']),
mk('Lẩu dê Lê Văn Sỹ Phú Nhuận','Lẩu Dê Tri Kỷ','restaurant','food','lẩu','Phú Nhuận',280000,320000,'couple',280000,320000,'https://webreview.vn/lau-de-tri-ky.html','medium','Lẩu dê nhỏ 280k, size L 320k (nồi cho 2–3 người)','Lẩu dê bình dân, ngồi lai rai buổi tối.',['rẻ mà vui','ngày mưa'],['https://webreview.vn/lau-de-l-lau-de-tri-ky.html']),
mk('Bánh canh cua Út Lệ Quận 3','Bánh Canh Cua Út Lệ','streetfood','food','bánh canh','Quận 10',40000,80000,'person',80000,160000,'https://ghiensaigon.com/banh-canh-cua-ut-le/','medium','40–80k/tô tùy topping','Bánh canh cua đặc sệt, bán từ chiều tối.',['rẻ mà vui'],['https://www.foody.vn/ho-chi-minh/banh-canh-cua-to-hien-thanh']),
mk('Bột chiên Đạt Thành Quận 5','Bột Chiên Đạt Thành','streetfood','food','bột chiên','Quận 3',40000,40000,'person',80000,80000,'https://www.momo.vn/page/9814729','low','Trung bình ~40k/người (MoMo)','Bột chiên trứng giòn kiểu người Hoa.',['rẻ mà vui']),
mk('Bò né 3 Ngon Quận 1','Bò Né 3 Ngon (Đinh Tiên Hoàng)','restaurant','food','bò né','Quận 1',60000,74000,'person',120000,148000,'https://food.be.com.vn/ho-chi-minh/bo-ne-3-ngon-hiep-binh-116299','low','Giá chi nhánh khác của chuỗi: 60k thường, 74k đặc biệt','Bò né chảo gang, mở đến 23h.',['rẻ mà vui','đêm muộn']),
mk('Sủi cảo Hà Ký 138 Châu Văn Liêm','Hà Ký – Sủi Cảo, Hủ Tiếu (Châu Văn Liêm)','restaurant','food','sủi cảo / hủ tiếu','Quận 5',55000,55000,'person',110000,110000,'https://exa.ai/library/place/cnxm8p50pkf','low','Hủ tiếu khô thập cẩm ~55k','Quán sủi cảo, hủ tiếu người Hoa ở Chợ Lớn.',['rẻ mà vui']),
mk(None,'Phở Quỳnh','restaurant','food','phở','Quận 1',80000,80000,'person',160000,160000,SH,'low','Tô ~80k (saigonhomestay)','Phở bò khu Phạm Ngũ Lão.',['rẻ mà vui','đêm muộn'],addr='323 Phạm Ngũ Lão, Q.1'),
mk(None,'Cơm Tấm Phúc Lộc Thọ','restaurant','food','cơm tấm','Quận 3',60000,60000,'person',120000,120000,SH,'low','~60k/phần (saigonhomestay)','Cơm tấm quen của dân Lê Văn Sỹ.',['rẻ mà vui'],addr='339 Lê Văn Sỹ, Q.3'),
mk(None,'Hủ Tiếu Nam Vang Quỳnh','restaurant','food','hủ tiếu','Quận 1',50000,55000,'person',100000,110000,SH,'low','50–55k/tô','Hủ tiếu Nam Vang khu Bến Thành.',['rẻ mà vui'],addr='86 Lê Thị Riêng, Q.1',oh='06:00–23:00 (saigonhomestay)',hours=[360,1380]),
mk(None,'Cuốn N Roll','restaurant','food','gỏi cuốn','Quận 1',40000,55000,'person',80000,110000,SH,'low','40–55k/phần 4 cuốn','Gỏi cuốn, món cuốn thanh nhẹ.',['rẻ mà vui'],addr='12 Nguyễn Trung Trực, Q.1',oh='10:00–22:00 (saigonhomestay)',hours=[600,1320]),
mk(None,'Bún Bò Gánh (Nguyễn Trãi)','restaurant','food','bún bò Huế','Quận 1',65000,75000,'person',130000,150000,SH,'low','65–75k/tô','Bún bò Huế cay nồng, hợp bữa tối.',['rẻ mà vui'],addr='110 Nguyễn Trãi, Q.1',oh='06:00–22:00 (saigonhomestay)',hours=[360,1320]),
mk(None,'Bánh Xèo Ăn Là Ghiền','restaurant','food','bánh xèo','Quận 1',80000,80000,'person',160000,160000,SH,'low','~80k/phần','Bánh xèo, món cuốn miền Tây.',['rẻ mà vui'],addr='74 Sương Nguyệt Ánh, Q.1'),
# ---- mid / nicer dinners ----
mk('Bếp Mẹ Ỉn 136/9 Lê Thánh Tôn','Bếp Mẹ Ỉn – Lê Thánh Tôn','restaurant','food','món Việt','Quận 1',99000,179000,'dish',260000,360000,'https://www.momo.vn/page/9790515','medium','~150k/người; món 99–179k (ước 2 món)','Món Việt trong hẻm xinh, decor hoài cổ.',['chill','lãng mạn'],['https://6ixgo.com/vi/Bep-Me-In-Le-Thanh-Ton.ri99']),
mk('Secret Garden Restaurant Pasteur','Secret Garden (158 Pasteur)','restaurant','food','món Việt sân thượng','Quận 1',150000,250000,'person',300000,500000,'https://www.pasgo.vn/nha-hang/nha-hang-secret-garden-158bis-pasteur---huong-vi-dong-que-nam-bo-791','medium','150–250k/người','Nhà hàng món quê trên sân thượng chung cư cũ.',['lãng mạn','chill'],['https://tamsusaigon.com/quan-an-gia-dinh-quan-1/']),
mk('Cục Gạch Quán Quận 1','Cục Gạch Quán','restaurant','food','món Việt','Quận 1',150000,350000,'person',300000,700000,'https://foodhunter.vn/quan-com-que-sai-gon-ngon/','medium','150–350k/người','Nhà cổ, món nhà quê tinh tế, hợp hẹn hò nhẹ nhàng.',['lãng mạn','kỷ niệm'],['https://tamsusaigon.com/quan-an-gia-dinh-quan-1/']),
mk('Quán Ăn Ngon 138 Nam Kỳ Khởi Nghĩa','Quán Ăn Ngon 138','restaurant','food','món Việt 3 miền','Quận 1',120000,250000,'person',240000,500000,'https://doisongphapluat.com.vn/quan-an-gia-dinh-ngon-duoc-yeu-thich-nhat-o-tp-hcm-a690815.html','medium','120–250k/người','Biệt thự Pháp, món ăn 3 miền nhiều lựa chọn.',['chill'],['https://foodhunter.vn/quan-com-que-sai-gon-ngon/']),
mk("Pizza 4P's Lê Thánh Tôn","Pizza 4P's Lê Thánh Tôn",'restaurant','food','pizza Nhật – Ý','Quận 1',168000,440000,'dish',340000,880000,'https://pizza4ps.com/vn/menu/','high','Pizza 168–440k (ước 2 món/2 người)','Pizza lò củi phô mai tự làm, cần đặt bàn.',['lãng mạn','chill']),
mk('Gogi House Lê Thánh Tôn','GoGi House Vincom Đồng Khởi','restaurant','food','nướng Hàn Quốc','Quận 1',199000,539000,'person',398000,1078000,'https://aeonmall-tanphuceladon.com.vn/tin-tuc/gogi-house-gia-ve-va-thuc-don.html','medium','Buffet 199–539k/người','Buffet nướng Hàn Quốc trong Vincom.',['năng động','ngày mưa']),
# ---- dessert / cafe / bar ----
mk('Chè Hiển Khánh Quận 1','Chè Hiển Khánh','dessert','food','chè','Quận 3',22500,67000,'dish',56000,134000,'https://hoantien365.com/quan-an/che-hien-khanh','medium','Chè 28–39k, flan 67k','Quán chè lâu năm, chè thạch, bánh flan.',['rẻ mà vui'],[V+'che-hien-khanh/']),
mk('Kem Bạch Đằng Lê Lợi Quận 1','Kem Bạch Đằng (Lê Lợi)','dessert','food','kem','Quận 1',40000,110000,'dish',80000,220000,'https://www.foody.vn/ho-chi-minh/kem-bach-dang/video','medium','40–110k (Foody)','Kem trái dừa huyền thoại, gần phố đi bộ Nguyễn Huệ.',['rẻ mà vui','kỷ niệm']),
mk('Cộng Cà Phê Hồ Con Rùa','Cộng Cà Phê (Hồ Con Rùa)','cafe','food','cafe','Quận 3',59000,69000,'drink',118000,138000,'https://congcaphe.com/product/556/cot-dua-ca-phe','high','Cốt dừa cà phê 59–69k','Cafe phong cách bao cấp, ngay vòng xoay Hồ Con Rùa.',['chill','kỷ niệm'],['https://saigon-navi.com/guide/cong-caphe-hcmc/']),
mk('Saigon Ơi Cafe Quận 1','Cà phê Sài Gòn Ơi (42 Nguyễn Huệ)','cafe','food','cafe view phố','Quận 1',50000,65000,'drink',100000,130000,'https://bandembanhom.com/ca-phe-sai-gon-oi-khu-vuon-nho-giua-long-thanh-pho/','low','Đồ uống 50–65k (menu tham khảo)','Cafe ban công chung cư 42 Nguyễn Huệ nhìn xuống phố đi bộ.',['chill','lãng mạn']),
mk('Social Club Rooftop Bar Hotel des Arts','Social Club Rooftop (Hôtel des Arts)','bar','food','rooftop bar','Quận 3',280000,350000,'drink',560000,700000,'https://vietnamwithme.com/2026/05/22/social-club-rooftop-saigon/','medium','Cocktail 280–350k; 15:00–19:00 giảm 50% đồ uống','Rooftop tầng 24 có hồ bơi, ngắm hoàng hôn.',['lãng mạn','sang chảnh'],['https://saigon-scene.com/top-rooftop-bars-in-saigon/']),
mk('Saigon Saigon Rooftop Bar Caravelle','Saigon Saigon Rooftop Bar (Caravelle)','bar','food','rooftop bar','Quận 1',200000,700000,'drink',400000,1400000,'https://e.vnexpress.net/photo/places/ho-chi-minh-citys-famous-wartime-bar-gets-new-look-5129391.html','medium','Cocktail 200–700k, +5% phí dịch vụ & thuế; mở lại 28/9/2026','Rooftop lịch sử trên khách sạn Caravelle, nhìn Nhà hát TP.',['lãng mạn','sang chảnh'],['https://www.caravellehotel.com/saigon-saigon-bar/'],oh='16:00–01:00 hằng ngày',hours=[960,1500]),
# ---- activities ----
mk('Galaxy Nguyễn Du Quận 1','Galaxy Cinema Nguyễn Du','cinema','activity','rạp phim','Quận 1',45000,95000,'ticket',90000,190000,'https://viettelstore.vn/tin-tuc/rap-chieu-phim-hcm','medium','Vé 2D 45–95k tùy suất/ngày','Rạp lâu đời trung tâm Q1, giá mềm.',['ngày mưa','rẻ mà vui'],['https://cinenjoy.com/gia-ve/galaxy-cinema']),
mk('CGV Vincom Đồng Khởi','CGV Vincom Center Đồng Khởi','cinema','activity','rạp phim','Quận 1',79000,135000,'ticket',158000,270000,'https://viettelstore.vn/tin-tuc/rap-cgv-hcm','medium','2D người lớn 79–135k; Sweetbox +26–30k','Rạp CGV trong Vincom Đồng Khởi.',['ngày mưa']),
mk('Cinestar Quốc Thanh 271 Nguyễn Trãi','Cinestar Quốc Thanh','cinema','activity','rạp phim','Quận 1',45000,70000,'ticket',90000,140000,'https://phimvn.blog/gia-ve-cinestar','medium','2D: T2 45k, T3–5 ~65k, cuối tuần ~70k','Rạp giá rẻ, có ghế giường nằm C’MÊ.',['ngày mưa','rẻ mà vui'],['https://hieumephim.com/danh-gia-cum-rap-chieu-phim-viet-nam/']),
mk('Galaxy Cinema Tân Bình 246 Nguyễn Hồng Đào','Galaxy Cinema Tân Bình','cinema','activity','rạp phim','Tân Bình',45000,95000,'ticket',90000,190000,'https://viettelstore.vn/tin-tuc/rap-chieu-phim-hcm','low','Mức chung Galaxy HCM 45–95k','Rạp Galaxy khu Bàu Cát.',['ngày mưa','rẻ mà vui'],['https://cinenjoy.com/gia-ve/galaxy-cinema']),
mk(None,'Superbowl Tân Sơn Nhất (bowling)','game','activity','bowling','Tân Bình',35000,65000,'session',70000,130000,'https://enjoyvietnamtravel.com/blog/top-bowling-venues-in-ho-chi-minh-city-and-practical-tips','low','35–60k/game (2023) / 65k/game; Foody 50–100k — gọi xác nhận','24 lane bowling + khu game, gần sân bay.',['năng động'],['https://www.foody.vn/ho-chi-minh/superbowl-tan-son-nhat','https://www.myguidevietnam.com/things-to-do/saigon-superbowl'],addr='A43 Trường Sơn, P.4, Tân Bình',oh='09:30–23:00 (Foody)',hours=[570,1380],status='uncertain'),
mk('Billiards Phú Nhuận Tâm Billiards','ASAP Billiards (Thích Quảng Đức)','game','activity','bida','Phú Nhuận',69000,69000,'hour',69000,138000,'https://bidatop.com/clb-bida-asap/','medium','69k/giờ/bàn (1–2 giờ)','CLB bida rộng, mở đến khuya.',['năng động','đêm muộn']),
mk(None,'CLB Bida Right Now (Tân Định)','game','activity','bida','Quận 1',59000,90000,'hour',60000,180000,'https://bidatop.com/clb-bida-right-now-phuong-tan-dinh-tphcm/','low','59–90k/giờ; từ 21h 60k/giờ','Bida trung tâm Q1, giá mềm sau 21h.',['năng động','đêm muộn'],['https://www.xanhsm.com/news/bida-quan-1-tphcm']),
mk(None,'Spirit Escape (Bình Thạnh)','game','activity','escape room','Bình Thạnh',159000,189000,'person',318000,378000,'https://spiritescape.vn/','high','60 phút: 159k trước 18h ngày thường, 189k sau 18h/cuối tuần','Phòng thoát hiểm chủ đề tâm linh, cần đặt trước.',['năng động','ngày mưa'],addr='71D Nguyễn Thượng Hiền, P.5, Bình Thạnh'),
mk('VietClimb Saigon Thảo Điền','Skywalk Climbing (leo núi nhân tạo)','game','activity','leo núi trong nhà','Bình Thạnh',200000,280000,'person',400000,560000,'https://saigonclimbing.com/pricing/','high','Boulder 200k/ngày; người lớn 280k/ngày gồm giày + HLV','Tường leo núi trong nhà, thử thách vận động cho 2 người.',['năng động'],addr='168/42 Nguyễn Gia Trí, Bình Thạnh'),
mk('Saigon Archery Club','CLB Bắn cung Nhà Văn hóa Thanh Niên','game','activity','bắn cung','Quận 1',70000,70000,'session',140000,280000,'https://bancungsaigon.com/','high','70k/30 phút/người (có HLV, bảo hộ)','Bắn cung giữa trung tâm, có hướng dẫn cho người mới.',['năng động','rẻ mà vui'],addr='21 Phạm Ngọc Thạch, Q.1',oh='08:00–22:00',hours=[480,1320]),
mk('Karaoke ICOOL Phan Xích Long','Karaoke ICOOL Phan Xích Long','game','activity','karaoke','Phú Nhuận',150000,300000,'hour',150000,600000,'https://vibessaigon.com/icool-karaoke/','low','Mức chung ICOOL 150–300k/giờ/phòng (1–2 giờ); giờ vàng rẻ hơn','Karaoke phòng riêng, hát cho nhau nghe.',['năng động','đêm muộn','ngày mưa']),
mk('Landmark 81 SkyView','Landmark 81 SkyView (đài quan sát)','sight','activity','đài quan sát','Bình Thạnh',300000,500000,'ticket',600000,1000000,'https://vincom.com.vn/store/landmark-81-skyview','high','300k T2–T6, 500k cuối tuần/lễ (người lớn)','Đài quan sát cao nhất VN, ngắm thành phố lên đèn.',['lãng mạn','kỷ niệm'],['https://vietnamtourexpert.com/landmark-81/']),
mk('Miu Miu Spa Quận 1','Miu Miu Spa 1 (Chu Mạnh Trinh)','spa','activity','massage','Quận 1',330000,500000,'session',660000,1000000,'https://www.miumiuspa.com/feature-12/massage-nhanh','high','Express 30’ 330k, foot 70’ 440k, body 60’ 500k/người; không cần tip','Spa massage nổi tiếng không tip, mở đến 23h.',['chill','kỷ niệm'],['https://nightlife.wiki/wiki/miumiu-spa']),
mk(None,'Ceramic Club (Q3)','workshop','activity','làm gốm','Quận 3',300000,550000,'person',600000,1100000,'https://vietinsiders.com/goi-y/workshop-lam-gom/','medium','300–550k/buổi/người','Nặn hoặc vẽ gốm, bàn xoay có nghệ nhân hướng dẫn.',['chill','kỷ niệm'],addr='59 Hẻm 7 Trần Quang Diệu, P.14, Q.3'),
mk(None,'Vườn Nhà Gốm','workshop','activity','làm gốm','Bình Thạnh',200000,400000,'person',400000,800000,'https://vietinsiders.com/goi-y/workshop-lam-gom/','medium','200–400k/buổi/người','Xưởng gốm trong vườn xanh, nhịp chậm.',['chill','kỷ niệm'],addr='301 Lê Quang Định, P.7, Bình Thạnh'),
mk(None,'Heny Garden (workshop nến thơm)','workshop','activity','làm nến thơm','Quận 10',250000,450000,'person',500000,900000,'https://vietinsiders.com/goi-y/workshop-lam-nen-thom-tphcm/','medium','250–450k/người','Học làm nến bài bản: chọn bấc, phối tinh dầu.',['chill','ngày mưa'],addr='370/24 Hoà Hảo, P.5, Q.10',oh='09:30–21:00 hằng ngày',hours=[570,1260]),
mk(None,'The Candle Holic','workshop','activity','làm nến thơm','Quận 1',450000,None,'person',900000,None,'https://vietinsiders.com/goi-y/workshop-lam-nen-thom-tphcm/','medium','Từ 450k/người','Nến tối giản cao cấp, phối hương & hoa khô.',['chill','lãng mạn'],addr='14 Đặng Dung, P. Tân Định, Q.1',oh='09:30–21:30 hằng ngày',hours=[570,1290]),
mk(None,'First Sight (Message Candle)','workshop','activity','làm nến thơm','Phú Nhuận',350000,None,'person',700000,None,'https://vietinsiders.com/goi-y/workshop-lam-nen-thom-tphcm/','medium','Từ 350k/người; cần đặt trước','Nến giấu thông điệp bên trong – quà kỷ niệm cho nhau.',['lãng mạn','kỷ niệm'],addr='23 Hoa Huệ, P.7, Phú Nhuận'),
mk(None,'Nến Thơm Tâm An','workshop','activity','làm nến thơm','Quận 1',350000,600000,'person',700000,1200000,'https://vietinsiders.com/goi-y/workshop-lam-nen-thom-tphcm/','medium','350–600k/người tùy gói','Nến hoa khô / đá năng lượng trong không gian thiền.',['chill'],addr='Lầu 2, 101 Trần Hưng Đạo, Q.1',oh='09:00–21:00 hằng ngày',hours=[540,1260]),
# ---- free / cheap walks & culture ----
mk('Hồ Con Rùa Quận 3','Hồ Con Rùa','sight','activity','dạo phố / ăn vặt','Quận 3',0,0,'free',0,0,'https://maps.google.com/?cid=3340651953480855379','medium','Không thu vé (không gian công cộng); ăn vặt quanh hồ tự chọn','Vòng xoay công viên nhỏ, buổi tối đông bạn trẻ ngồi ăn vặt.',['rẻ mà vui','chill','đêm muộn']),
mk('Công viên Tao Đàn Quận 1','Công viên Tao Đàn','sight','activity','công viên','Quận 1',0,0,'free',0,0,'https://maps.google.com/?cid=4535741078771275632','medium','Không thu vé','Công viên cây cổ thụ giữa Q1, dạo bộ mát.',['rẻ mà vui','chill']),
mk('Công viên Lê Văn Tám Quận 1','Công viên Lê Văn Tám','sight','activity','công viên','Quận 1',0,0,'free',0,0,'https://maps.google.com/?cid=7666491876929007457','medium','Không thu vé; gỏi khô bò, ăn vặt quanh công viên','Công viên rợp bóng cây, nhiều món ăn vặt xung quanh.',['rẻ mà vui','chill']),
mk('Nhà thờ Tân Định Quận 3','Nhà thờ Tân Định (nhà thờ màu hồng)','sight','activity','check-in nhà thờ','Quận 3',0,0,'free',0,0,'https://maps.google.com/?cid=8699547463492745602','medium','Không thu vé; giờ tham quan bên trong giới hạn','Nhà thờ hồng nổi tiếng, chụp ảnh bên ngoài.',['rẻ mà vui','kỷ niệm']),
mk('Chùa Ngọc Hoàng Đa Kao','Chùa Ngọc Hoàng (Phước Hải Tự)','sight','activity','chùa cổ','Quận 1',0,0,'free',0,0,'https://maps.google.com/?cid=4102120846024444045','medium','Không thu vé','Chùa cổ hơn 100 năm, không gian trầm mặc.',['chill']),
mk('Chợ hoa Hồ Thị Kỷ Quận 10','Chợ hoa Hồ Thị Kỷ','sight','activity','chợ hoa','Quận 10',0,0,'free',0,0,'https://maps.google.com/?cid=9847044473358350069','medium','Vào cửa miễn phí; mua hoa tùy ý','Chợ hoa sỉ nhộn nhịp ngay cạnh chợ ăn vặt Hồ Thị Kỷ.',['rẻ mà vui','lãng mạn']),
mk('Cầu Ánh Sao Phú Mỹ Hưng','Cầu Ánh Sao (Phú Mỹ Hưng)','sight','activity','dạo đêm','Quận 7',0,0,'free',0,0,'https://maps.google.com/?cid=17123664406864648589','medium','Không thu vé','Cây cầu đi bộ đổi màu đèn bên Hồ Bán Nguyệt.',['lãng mạn','rẻ mà vui']),
mk('Hồ Bán Nguyệt Phú Mỹ Hưng','Hồ Bán Nguyệt','sight','activity','dạo đêm','Quận 7',0,0,'free',0,0,'https://maps.google.com/?cid=6827587011548868897','medium','Không thu vé','Dạo quanh hồ, ngắm cầu Ánh Sao lên đèn.',['lãng mạn','chill']),
mk('Bảo tàng Phụ nữ Nam Bộ Quận 3','Bảo tàng Phụ nữ Nam Bộ','sight','activity','bảo tàng','Quận 3',0,0,'free',0,0,'https://congbao.hochiminhcity.gov.vn/cong-bao/van-ban/nghi-quyet/so/29-2026-nq-hdnd/ngay/27-08-2026/tai-ve/50039','medium','Miễn phí tham quan (NQ 29/2026, từ 1/10/2026)','Bảo tàng nhỏ về áo dài, phụ nữ Nam Bộ – đi buổi chiều.',['chill','ngày mưa'],['https://www.idctravel.com/blog/10-best-museums-in-ho-chi-minh-city.html']),
mk('Bảo tàng Lịch sử Việt Nam 2 Nguyễn Bỉnh Khiêm','Bảo tàng Lịch sử TP.HCM','sight','activity','bảo tàng','Quận 1',60000,60000,'ticket',120000,120000,'https://www.baotanglichsutphcm.com.vn/ban-tin/thong-bao-thay-doi-muc-phi-tham-quan-bao-tang','high','60k/người từ 1/10/2026','Bảo tàng cổ vật trong khuôn viên Thảo Cầm Viên.',['chill','ngày mưa']),
]
names={x['name'].lower() for x in d}
add=[x for x in N if x['name'].lower() not in names]
print('new',len(add),'skipped dup',len(N)-len(add))
# ---- fill existing gaps ----
def upd(i, **kw):
    for k,v in kw.items(): d[i][k]=v
upd(38, address='10B Tôn Đức Thắng, Q.1 (ga Bạch Đằng)', price_source_url='https://saigonwaterbus.com/water-bus', price_confidence='high', price_checked=C, opening_hours='07:00–21:00 T2–T6; 07:00–23:00 T7, CN, lễ', hours=[420,1260], lat=10.7752626, lng=106.7068754, maps_url='https://maps.google.com/?cid=4852626611537157215', maps_kind='direct', rating=4.4)
upd(34, price_source_url='https://saigonzoo.vn/ve-tham-quan', price_note='60k/người cao từ 1,3m', price_confidence='high', price_checked=C, opening_hours='07:00–18:30 (ngừng bán vé 17:30)', hours=[420,1110])
upd(4, couple_max=700000, price_max=350000, price_note='Cocktail ~350k++; happy hour 17:30–20:00 combo 2 cocktail + snack 590k++', price_source_url='https://saigon-scene.com/top-rooftop-bars-in-saigon/', price_checked=C, price_confidence='medium')
upd(94, price_note='50k/người/5 giờ, kèm nước 70k', price_source_url='https://boardgamecf.com/gia-ve-dich-vu-board-game-station-30-co-bac', price_confidence='high', price_checked=C)
upd(49, price_min=159000, price_max=189000, couple_min=318000, couple_max=378000, price_per_couple_vnd=378000, price_note='60 phút 159–189k/người tùy giờ/ngày; combo 2 tiếng từ 259k', price_source_url='https://masterescape.vn/', price_confidence='high', price_checked=C)
upd(28, opening_hours='17:00–22:00 (Google Maps)', hours=[1020,1320])
upd(90, status='uncertain', note='Google Maps 26/10/2026 ghi “Tạm thời đóng cửa” – gọi trước')
d.extend(add); json.dump(d,open(D,'w'),ensure_ascii=False,indent=1)
import collections
print(collections.Counter(x['kind'] for x in add)); print(collections.Counter(x['area'] for x in add))
print('direct maps',sum(x['maps_kind']=='direct' for x in add),'coords',sum(x['lat'] is not None for x in add))
print('fully priced',sum(x['couple_min'] is not None and x['couple_max'] is not None for x in add))
