# Manual price research 2026-10-26. key = exact item name. (min,max,unit,couple_min,couple_max,url,conf,note)
# unit: person|drink|session|ticket|couple|hour|room|dish|free
R = {}
def P(name,mn,mx,unit,cmin,cmax,url,conf,note,status=None):
    R[name]=dict(price_min=mn,price_max=mx,price_unit=unit,couple_min=cmin,couple_max=cmax,price_source_url=url,price_confidence=conf,price_note=note,**({'status_override':status} if status else {}))
P('Tròn Kitchen',200000,300000,'person',400000,600000,'https://wanderboat.ai/restaurants/vietnam/ho-chi-minh-city/tr%C3%B2n-kitchen/E42IRz6RQfymeT7k5Zwa-w','medium','Khoảng giá Maps 200–600k (theo nhóm); sashimi cá hồi 150k, trứng cá hồi 160k (6ixgo)')
P('Trượt băng Vincom Landmark 81',195000,250000,'ticket',450000,560000,'https://vincom.com.vn/store/vincom-ice-rink-landmark-81','high','Vé từ 1m40: 195k T2–T6, 250k T7–CN/lễ + thuê giày 30k/người')
P('Bắn cung ở Cung Văn hóa Lao động',50000,80000,'person',100000,160000,'https://wanderlog.com/place/details/5101560/clb-b%E1%BA%AFn-cung-galaxy-galaxy-archery-club','low','CLB Galaxy: 50k/30 phút, 80k/giờ (review 1/2025). ⚠️ Nguồn tổng hợp báo CLB đã ngưng/tạm đóng từ 26/10/2025 – gọi 0908 191 595 trước','uncertain')
P('The Park Rooftop Bar & Lounge',200000,400000,'person',400000,800000,'https://theparksaigon.com/wp-content/uploads/2026/04/MENU-THE-PARK-ROOFTOP-AND-LOUNGE.pdf','high','Cocktail 200–280k/ly; set Steak Dinner 589k, Seafood 789k (chưa VAT 8%)')
P('Propeller Rooftop Bar (Bay Hotel)',180000,300000,'person',360000,600000,'https://www.therooftopguide.com/rooftop-bars-in-ho-chi-minh/propeller-rooftop-bar-hcmc.html','medium','Cocktail ~180k, bia từ 85k; T4 Ladies Night mua 2 tặng 1')
P('Zion Sky Lounge & Dining',260000,380000,'drink',520000,760000,'https://zionskyloungesaigon.com/en/menu','high','Cocktail signature 300–320k, mocktail 260k (+10% VAT +9% phí phục vụ)')
P('Momento Rooftop (trước đây Cocoon Rooftop)',100000,300000,'person',200000,600000,'https://restaurantguru.com/Cocoon-Rooftop-Bar-Ho-Chi-Minh-City','low','Đồ uống ~50–130k; happy hour 16–21h gieo xúc xắc (momentorooftop.com)')
P('Rooftop Grand Lounge (Hotel Grand Saigon)',200000,300000,'drink',400000,600000,'https://www.foody.vn/ho-chi-minh/grand-cafe-grand-hotel-saigon/thuc-don','medium','Cocktail ~200–300k/ly; 15–17h mua 1 tặng 1 một số món')
P('Ráng Chiều Rooftop',39000,99000,'drink',100000,200000,'https://www.greensm.com/vn-vi/news/rang-chieu-rooftop-phu-nhuan','medium','Đồ uống/món 39–99k')
P('Bar57',150000,240000,'drink',300000,480000,'https://localvietnam.net/b/bar57-sai-gon','low','Cocktail ~240k, giờ vàng ~150k (review tổng hợp)')
P('The Refinery',300000,700000,'person',600000,1400000,'https://therefinerysaigon.com/wp-content/uploads/2025/12/tr-menu-chinese--official-2526.pdf','high','Menu 2025-26: set trưa 235–340k; món chính 440–450k, steak 740k–1tr; brunch cuối tuần 450k')
P('Cork and Bottle',300000,550000,'person',600000,1100000,'https://webreview.vn/cork-bottle-thai-van-lung.html','low','Chi tiêu ~300–550k/người theo review; ly vang ~180k (nguồn cũ)')
P('CỘI',100000,200000,'person',200000,400000,'https://vietnam-gift.com/en/news/coi-kissa-saigon/','low','Cà phê ~60–90k, cocktail ~150–250k (blog, menu không công bố)')
P('Pergola Cafe',50000,550000,'dish',None,None,'https://www.foody.vn/ho-chi-minh/pergola','medium','Món 50–550k; platter từ 699k (pergola.vn) – khó ước tính cho 2')
P('The Dome Kaffe',35000,75000,'drink',70000,150000,'https://shopeefood.vn/ho-chi-minh/the-dome-kaffe','medium','Đồ uống 35–75k/món (+phí DV 5%, VAT 10% theo menu cũ)')
P('Trăng Non Rooftop',30000,55000,'drink',60000,110000,'https://bandembanhom.com/review-trang-non-rooftop/','low','⚠️ Nguồn báo đã ngừng hoạt động từ 29/10/2025; giá cũ 30–55k/ly','closed')
P('Chạng Vạng Rooftop Hàng Xanh',39000,269000,'dish',150000,400000,'https://www.foody.vn/ho-chi-minh/chang-vang-rooftop-beer/thuc-don','low','Foody: 15–90k (cũ); nguồn khác 39–269k/món (beer + đồ nhậu)')
P('Vérité Patisserie',80000,200000,'dish',200000,400000,'https://jore.vn/verite-patisserie-review-beautiful-cakes-and-pastries-near-ben-thanh-market/','medium','Bánh signature 150–200k/cái, bánh nướng 50–150k; set 4 bánh từ 536k (FB)')
P('Châteraisé Lê Thánh Tôn',None,None,'dish',None,None,'https://mayuirina.blog/chateraisevietnam/','low','Chỉ thấy giá bánh kem dâu 14cm 430k; bánh lẻ chưa rõ giá')
P('Tarobu Dessert',16000,49000,'dish',60000,100000,'https://nishivietnam.com/tarobu/','medium','Món từ 16k; đá bào matcha khoai dẻo 49k')
P('Chợ ẩm thực Hồ Thị Kỷ',7000,70000,'dish',100000,200000,'https://mia.vn/cam-nang-du-lich/cho-am-thuc-ho-thi-ky-12237','medium','Món ăn vặt 7–70k (xiên nướng 15k, trà đào 10–15k); 2 người ăn no ~100–200k')
P('Yoko Cafe (nhạc sống)',60000,100000,'drink',120000,200000,'https://diadiem247.com/tp-ho-chi-minh/yoko-cafe-ho-chi-minh-l367850.html','low','Đồ uống 60–100k; đêm sự kiện có vé 150–250k (Saigoneer 2025)')
P("Sax n' Art Jazz Club",150000,275000,'drink',300000,550000,'https://www.foody.vn/ho-chi-minh/sax-nart-cafe','low','Đồ uống 150–275k; đêm đặc biệt phụ thu chỗ 300–500k (ticketgo 3/2025)')
P('Acoustic Bar Ngô Thời Nhiệm',80000,180000,'drink',160000,360000,'https://6ixgo.com/vi/Acoustic-Bar-Ngo-Thoi-Nhiem.ri67','medium','Bia ~80k; cocktail 170–180k')
P('VOTRI - Cabinet of Curiosities',270000,270000,'drink',540000,540000,'https://6ixgo.com/vi/VOTRI-Cabinet-of-Curiosities.ri43','medium','Cocktail 270k/ly; giảm 30% 18–20h')
P('Umatcha Se - Omakase Matcha - HVB',69000,95000,'drink',140000,190000,'https://www.yenpremium.com/umatcha-se-dia-diem-matcha-omakase-dau-tien-tai-viet-nam/','medium','Đồ uống matcha 69–95k; Nama matcha từ 59k')
P('BỜM - Kitchen & Wine Bar',199000,1699000,'person',600000,1500000,'https://amthuchiendai.vn/cam-nhan-ve-bom-kitchen-wine-bar-tphcm/','medium','Set 199k++ – 1.699k++/người; món chính ~269–299k++; set Valentine 2026 2,4tr++/2 người')
P('Fenice - Cuisine & Bar',300000,1000000,'person',600000,2000000,'https://topgo.vn/ho-chi-minh/fenice-cuisine-bar/','low','300k–1tr/người (topgo)')
P('GLAMISQUE - Fusion Dining',400000,688000,'person',800000,1376000,'https://glamisque.vn/hoi-tho-am-thuc-dong-duong-set-menu-lamant-1992/','high','Set cặp đôi từ 400k/người; set L’amant 1992 688k/người')
P("Smith's Kitchen & Bar",450000,1500000,'dish',1000000,2500000,'https://cdn.silverlandhotels.com/wp-content/uploads/2025/05/Smiths-Alacarte.pdf','high','Món chính 450k–1,5tr; cocktail 220–250k (+5% phí DV, VAT)')
P('Trạm Hầm Quận 3',69000,259000,'dish',300000,600000,'https://9club.vn/san-pham/tram-ham/','medium','Món 69–259k, cocktail 119–159k')
P('Tủ Bar',165000,400000,'drink',330000,800000,'https://exa.ai/library/place/0pt92ym6v7p','low','Cocktail không menu ~200–400k/ly; review: 330k/2 ly')
P('KKAEN Da Kuffee',32000,59000,'drink',64000,120000,'https://ghien.cafe/ho-chi-minh/kkaen-da-kuffee','medium','Cà phê/trà 32–59k')
P('Bodega Saigon',300000,None,'person',600000,None,'https://vietnamnightlife.com/bodega-769-16.html','low','Club: quầy bar từ 300k; bàn VIP từ 4tr (chưa VAT/phí)')
P('Every Half Coffee Roasters - Võ Thị Sáu',50000,85000,'drink',100000,170000,'https://food.be.com.vn/ho-chi-minh/every-half-coffee-roasters-pham-ngoc-thach-112287','medium','Đồ uống 50–85k, bánh 55–70k (menu beFood)')
for n in ['WorkFlow Thảo Điền - Working Space & Café','WorkFlow Gò Vấp - Working Space & Café','WorkFlow Quận 3 - Working Space & Café']:
    P(n,50000,85000,'drink',100000,170000,'https://wanderlog.com/vi/place/details/10865381/workflow-th%E1%BA%A3o-%C4%91i%E1%BB%81n-working-space--cafe','medium','Đồ uống 50–85k (menu WorkFlow Thảo Điền; chi nhánh khác có thể khác)')
P('GEEK Hub Huynh Van Banh',30000,30000,'person',60000,60000,'https://www.momo.vn/page/1022893','medium','Phí chỗ ngồi 30k/4 giờ (chưa gồm đồ uống)')
P('Chợ Bến Thành – khu ăn uống buổi tối',50000,200000,'dish',200000,400000,'https://saucefish.com/vi/5-mon-an-dang-thu-nhat-cho-ben-thanh-bay-du-lich-noi-tieng-sai-gon/','medium','Món 50–200k (bún thịt nướng 70k, bánh canh cua 70k); khu du lịch nên giá cao')
P('Timezone Vincom Đồng Khởi',250000,350000,'couple',250000,350000,'https://thelandmark81.com.vn/timezone-vincom-dong-khoi/','low','Không vé vào; nạp thẻ 250k→300k credit, 350k→450k credit (dùng chung 2 người)')
P('Sân Patin Vietnam Roller Rink & Academy',60000,75000,'ticket',120000,150000,'https://kiddogovn.com/vi/activity/vietnam-roller-rink-academy-cong-hoa','medium','60k ngày thường, 75k cuối tuần, gồm giày + bảo hộ, không giới hạn giờ')
P('Real Escape Sài Gòn',169000,199000,'person',338000,398000,'https://realescape.vn/bang-gia/','high','1 giờ: 169k T2–T5, 189k cuối tuần, 199k lễ; combo 2 giờ 269k/người')
P('Jump Arena HimLam',170000,210000,'ticket',340000,420000,'https://jumparena.vn/pages/gia-ve','high','T2–T5 170k không giới hạn; cuối tuần/lễ 210k/120 phút')
P('Jump Arena Starmart Gò Vấp',140000,180000,'ticket',280000,360000,'https://jumparena.vn/pages/gia-ve','high','T2–T5 140k không giới hạn; cuối tuần/lễ 180k/120 phút')
for n in ['Tiệm Gội Đầu Mèo Xù - Nguyễn Gia Trí','Tiệm Gội Đầu Mèo Xù - Lê Văn Sỹ']:
    P(n,79000,119000,'person',158000,238000,'https://tiemgoidaumeoxu.vn/','high','Gội cơ bản 15p từ 49k; gội massage 30p từ 79k; 45p cổ vai gáy từ 119k')
# chains by prefix
CHAIN = [
 ('Phaya Thai Spa',dict(price_min=399000,price_max=599000,price_unit='person',couple_min=798000,couple_max=1198000,price_source_url='https://phayathaispa.com/',price_confidence='high',price_note='Body massage 60’ 399k – 90’ 599k; foot 60’ 379k (chưa VAT)')),
 ('Phaya thai spa',None),
 ('Life4cuts',dict(price_min=70000,price_max=100000,price_unit='session',couple_min=70000,couple_max=100000,price_source_url='https://www.tripadvisor.com/Attraction_Review-g293925-d25423141-Reviews-Life4cuts_Nowzone-Ho_Chi_Minh_City.html',price_confidence='medium',price_note='Basic 4 cuts 70k/lượt (2 dải ảnh), Multi frame 100k – 1 lượt đủ cho 2 người')),
 ('Life Four Cut',None),
 ('Photo Palette',dict(price_min=60000,price_max=130000,price_unit='session',couple_min=70000,couple_max=110000,price_source_url='https://www.reviewphotobooth.com/photobooths/photo-palette-huynh-thuc-khang',price_confidence='medium',price_note='Basic ~60–100k, Palette Air 70–110k/lượt (2 dải ảnh)')),
 ('PHOTO OBJET',dict(price_min=70000,price_max=100000,price_unit='session',couple_min=70000,couple_max=100000,price_source_url='https://www.facebook.com/photoobjetvietnam/posts/122192951240291645/',price_confidence='medium',price_note='70–100k/lượt (bảng giá FB Photo Objet VN 10/2025)')),
 ('Photo Objet',None),
 ('Photoism',dict(price_min=70000,price_max=100000,price_unit='session',couple_min=70000,couple_max=100000,price_source_url='https://simpletech.vn/blogs/photobooth/7-dia-diem-chup-anh-photobooth-tai-sai-gon',price_confidence='medium',price_note='70–100k/lượt; frame idol ~150k (blog 8/2025)')),
 ('Mothaiba',dict(price_min=70000,price_max=100000,price_unit='session',couple_min=70000,couple_max=100000,price_source_url='https://www.vietnamairlines.com/gb/en/plan-book/travel/travel-guide/photobooth-ha-noi',price_confidence='low',price_note='~70–100k cho 2 dải ảnh (bài tổng hợp, chi nhánh HN)')),
 ('Bliss Homestay',dict(price_min=None,price_max=None,price_unit='room',couple_min=250000,couple_max=550000,price_source_url='https://www.hotels1000.com/VN/Qu%E1%BA%ADn-T%C3%A2n-B%C3%ACnh/108379195530721/Bliss-Home',price_confidence='low',price_note='Từ ~250k/3 giờ; qua đêm 22h–11h ~550k (review) – giá theo phòng, inbox để chốt')),
 ('Bliss Home Signature',None),
]
P('Bảo tàng Chứng tích Chiến tranh',60000,60000,'ticket',120000,120000,'https://baotangchungtichchientranh.vn/en/visit','high','Từ 1/10/2026: 60k/người/lượt; SV miễn phí')
P('CGV Liberty Citypoint – Sweetbox',95000,130000,'ticket',190000,260000,'https://fptshop.com.vn/tin-tuc/danh-gia/gia-ve-cgv-182577','medium','Ghế đôi Sweetbox = vé thường (70–105k) + 25k/người; giá đơn vị theo ghế/người')
P("CGV L'amour (rạp giường nằm) Hoàng Văn Thụ",300000,600000,'couple',300000,600000,'https://viettelstore.vn/tin-tuc/rap-lamour','medium','Giường nằm cho 2: ~600k; T4 ~400k, Culture Day ~300k')
P('CineB Saigon (chiếu phim ngoài trời)',80000,80000,'ticket',160000,160000,'https://tuoitre.vn/diem-la-sai-gon-hut-nguoi-tre-965136.htm','low','⚠️ Giá cũ 80k gồm bắp nước (báo cũ <2024); review gần đây cho thấy đã ngừng hoạt động','closed')
P('Tipsy Art',440000,440000,'person',880000,880000,'https://tipsyart.vn/pages/to-create','high','440k/người/3,5 giờ gồm toan, màu, 2 đồ uống')
P('Coming Home Candle',250000,600000,'person',500000,1200000,'https://vietinsiders.com/goi-y/workshop-lam-nen-thom-tphcm/','medium','Từ 250k/người; nến dessert 400–600k')
P('Master Escape Room',169000,199000,'person',338000,398000,'https://escaperoomclub.com/escape-room/vietnam/thanh-pho-ho-chi-minh/thanh-pho-ho-chi-minh/master-escape-saigon-the-promise-ki-tuc-xa/','medium','60 phút: 169k (T2–T6 trước 17h), 189k tối/cuối tuần, 199k lễ')
P('Nhà hát Thành phố',600000,1800000,'ticket',1200000,3600000,'https://cityguide.vn/vn/ho-chi-minh/su-kien/van-hoa-va-nghe-thuat/bieu-dien-san-khau/xiec-tre-a-o-show-18611b68-5b11-42e9-bf3f-242ba89871d1','medium','Tùy chương trình: À Ố Show 800k–1,75tr; ballet HBSO 600k–1,8tr (2026)')
P('Thương Xanh Film Store – chụp/tráng film',65000,120000,'session',65000,120000,'https://thuongxanhfilmstore.vn/pages/trang-scan-film-trangden','high','Tráng scan C-41 65k/cuộn 35mm, trắng đen 100k; (giá theo cuộn film)')
P('Ddreamer (làm nhẫn bạc)',950000,1500000,'person',3000000,3000000,'https://ddreamerjewelry.com/workshops/all-workshops/workshops-faq/','high','950k/người (nhóm 2–4) + bạc tối thiểu ~550k/nhẫn → ~3tr/2 người')
P('Sân khấu kịch Hồng Vân',200000,350000,'ticket',400000,700000,'https://sankhauthiendang.vn/san-khau/hong-van/','low','Tham khảo 200–350k/vé; gọi 028 2244 6454 để chốt')
P('Wichita Tarot Cafe',250000,300000,'session',250000,300000,'https://wichita-tarot.com/bieu-phi/','high','Trực tiếp 250k/30 phút (đặt trước), 300k không đặt trước; 1 phiên có thể xem cho cặp đôi')
P('Printaphy Photobooth',3000000,7000000,'session',None,None,'https://hcm.inhat.vn/photobooth-tphcm/','low','⚠️ Là dịch vụ photobooth cho sự kiện (gói từ 3tr), không phải tiệm chụp lẻ','uncertain')
for n in ['Golden Lotus','Golden Lotus Healing World']:
    P(n,390000,560000,'person',780000,1120000,'https://goldenlotus.world/mot-lieu-trinh-massage-ca-ngay-em-ai.html','high','Massage chân 60’ 390k; body 430–560k (website)')
P('An Nhật Wellness Onsen & Jjimjilbang, Spa',199000,268000,'ticket',398000,536000,'https://www.healthandbeauty1.com/VN/Xa-Phu-Rieng/287010304497357/An-Nh%E1%BA%ADt-Onsen---Jjimjilbang-%26-Spa','medium','Vé onsen + jjimjilbang từ 268k; giờ vàng T2–T6 19–22h 199k')
P('Massage Cổ Phong Q3 | Gội Đầu Dưỡng Sinh',349000,890000,'person',698000,1780000,'https://massagecophong.com/bang-gia/','high','Gội dưỡng sinh 349k; massage body 60’ 690k, 90’ 890k')
P('MASSAGE HẠ SPA Tân Bình',299000,399000,'person',598000,798000,'https://haspamassage.vn/menu-english/','high','Gội dưỡng sinh 299k; massage 60’ 399k kèm xông hơi')
P('Lạc Yên Healing Spa - Gội Đầu Dưỡng Sinh',69000,199000,'person',138000,398000,'https://www.lemon8-app.com/@buanaodian/7566185770949624341?region=vn','low','Liệu trình 69–199k (review Lemon8)')
P('Infinity Racing Vincom Thảo Điền',270000,390000,'person',540000,780000,'https://infinity.racing/vi/','high','Go-kart người lớn 270–390k/lượt; sim racing 100k')
P('JP BOWLING & GAME CENTER',30000,65000,'person',80000,150000,'https://blogkinhdoanh.edu.vn/gia-bowling-gigamall-bao-nhieu-choi-o-day-co-dang-dong-tien-bat-gao/','medium','30–55k/lượt/người (lễ 65k) + giày 10k')
P('Lava Planet Vincom Thảo Điền',None,None,'session',None,None,'https://thelandmark81.com.vn/lava-planet-vincom-thao-dien/','low','Không vé cổng, nạp thẻ theo trò – chưa có bảng giá công khai')
P('Another Saigon by LG',0,0,'free',0,0,'https://www.lofficielvietnam.com/toys-tech/metime-by-lg-tai-another-saigon-tam-gac-au-lo-dje-cong-nghe-la-cach-chung-ta-yeu','medium','Không gian/sự kiện mở cửa miễn phí (2026); một số workshop cần đăng ký trước')
P('Workshop Hub',None,None,'person',None,None,'https://mio.travel/p/workshop-hub','low','Chỉ thấy keychain nón lá ~5 USD/người; workshop nến/tranh/resin chưa công bố giá')
P('XOXO SAIGON - Workshop, Accessories, Custom',30000,500000,'person',None,None,'https://www.lemon8-app.com/@username01234567676767/7635706724389552647?region=sg','low','Vòng charm Ý tính theo charm (từ 30k/charm); review: tổng <20 USD')
P('CHUCKY BEETLE INDUSTRY',209000,649000,'person',418000,1298000,'https://chuckybeetleindustry.com/workshop/','high','Workshop 209k / 389k / 649k mỗi người tùy concept')
P('Haru Craft Ceramic Studio',500000,600000,'person',1000000,1200000,'https://tripi.vn/blog/vi/kinh-nghiem-hay/kham-pha-niem-vui-lam-gom-tai-6-dia-chi-duoc-yeu-thich-trai-nghiem-tuyet-voi-cho-ca-gia-dinh-tripi','medium','~500–600k/người (blog 2025)')
P('Clover Pottery Studio & Cafe',180000,380000,'person',360000,760000,'https://vieclam.net/blog/workshop-lam-gom-tphcm-28336/','medium','Tô vẽ gốm từ 180k; làm gốm ~380k/người')
P('Hiên Concept',450000,450000,'person',900000,900000,'https://sgtt.thesaigontimes.vn/thoa-suc-sang-tao-voi-4-workshop-thu-vi-o-tphcm/','medium','Workshop gốm 450k/người, nhận sản phẩm sau 15–20 ngày')
P('MYU MEMORIES - Trang Sức Phụ Kiện Italy',None,None,'person',None,None,'https://myumemories.com/workshop/','high','Giá theo sản phẩm; cọc 30k/người trừ vào sản phẩm')
def PB(n,mn,mx,url,conf,note): P(n,mn,mx,'session',mn,mx,url,conf,note+' – 1 lượt chụp đủ cho 2 người')
PB('PixelB photobooth',90000,90000,'https://exa.ai/library/place/zsvlx303q30','low','~90k/lượt (phản hồi khách)')
PB('PixelB Vintage Photobooth',90000,90000,'https://exa.ai/library/place/zsvlx303q30','low','~90k/lượt (theo chi nhánh PixelB Tân Bình)')
PB('Twinkle.booth',70000,120000,'https://photobooth.joelin.cc/vi/vietnam/locations/twinklebooth/','low','~70–120k/lượt (khách báo)')
PB('Paris Booth',80000,100000,'https://photobooth.joelin.cc/vi/brand/paris-booth/','medium','80k (ảnh 15×5) / 100k (15×10), 2 tấm')
PB('MÈO MỐC PHOTOBOOTH QUẬN 5 (PHƯỜNG CHỢ LỚN)',70000,100000,'https://photobooth.joelin.cc/vi/vietnam/locations/meo-moc-quan-5/','medium','70–100k/lượt')
PB('Ngói Photobooth - Nguyễn Tri Phương',60000,90000,'https://photobooth.joelin.cc/vi/brand/ngoi-photobooth/','medium','Original 60k, Film 90k/lượt')
PB('Foto.Flicker Photobooth Saigon',80000,110000,'https://reviewphotobooth.com/photobooths/thuong-hieu/foto-flicker','low','80k (3 ảnh) / 110k (4 ảnh) – giá chi nhánh Hà Nội')
P('85B Homestay',None,None,'room',750000,1800000,'https://vungtautourism.com/85b-homestay/','medium','750k–1,8tr/đêm/phòng tùy phòng & ngày')
P('Sense Homes An Dương Vương',None,None,'room',650000,825000,'https://sensevn.com/','high','Từ 650k (Gò Vấp) – 825k (Q3)/đêm/phòng')
P('Sense Homestay Quận Tân Bình',None,None,'room',650000,825000,'https://sensevn.com/','medium','Chuỗi Sense: từ 650–825k/đêm/phòng (website)')
# ---- Structuring prices already found in earlier research (notes from data/research_hcm / web_additions) ----
# (min,max,unit,cmin,cmax,conf) ; source = item's first source_url ; note kept
E = {
 'Chill Skybar (AB Tower)':(200000,None,'person',400000,None,'medium'),
 'Trên Tầng Thượng':(60000,75000,'drink',120000,150000,'medium'),
 '3Đ Chill Cafe':(45000,60000,'drink',90000,120000,'medium'),
 'OZ Coffee House':(30000,250000,'dish',None,None,'low'),
 'Oromia Coffee & Lounge':(40000,150000,'dish',100000,300000,'low'),
 'Lavender':(49000,None,'drink',100000,None,'low'),
 'Nến Cafe':(30000,110000,'drink',60000,220000,'medium'),
 'Cà phê Thủy Trúc':(35000,100000,'drink',70000,200000,'medium'),
 'The Deck Saigon':(200000,800000,'person',400000,1600000,'low'),
 'Quán Bụi Garden':(50000,250000,'person',200000,500000,'low'),
 'The Butcher Shop & Grill':(200000,400000,'person',400000,800000,'low'),
 'Benthanh Princess – du thuyền ăn tối':(980000,None,'person',1960000,None,'high'),
 'Du thuyền Saigon Princess – ăn tối trên sông':(980000,None,'person',1960000,None,'medium'),
 'Phố đi bộ Nguyễn Huệ':(0,0,'free',0,0,'high'),
 'Thảo Cầm Viên':(60000,60000,'ticket',120000,120000,'medium'),
 'Buýt đường sông Sài Gòn (Water Bus)':(15000,30000,'ticket',30000,60000,'medium'),
 'Saigon Skydeck (Bitexco)':(240000,240000,'ticket',480000,480000,'medium'),
 'Bảo tàng Mỹ thuật TP.HCM':(60000,60000,'ticket',120000,120000,'medium'),
 'Bảo tàng Thành phố Hồ Chí Minh (Dinh Gia Long)':(60000,60000,'ticket',120000,120000,'medium'),
 'Dinh Độc Lập':(80000,80000,'ticket',160000,160000,'medium'),
 'Gốm Sài Gòn':(450000,450000,'person',900000,900000,'medium'),
 'Bibouyo':(300000,None,'person',600000,None,'medium'),
 'Karaoke ICOOL Thành Thái':(120000,350000,'hour',240000,700000,'medium'),
 'Bowling Vạn Hạnh Mall':(60000,100000,'person',120000,200000,'low'),
 'HARUFILM Nguyễn Thái Học':(80000,150000,'session',80000,150000,'medium'),
 'PHOTOBY Nguyễn Bỉnh Khiêm':(70000,100000,'session',70000,100000,'medium'),
 'PHOTOBY Nguyễn Khắc Nhu':(70000,100000,'session',70000,100000,'medium'),
 'SAY CHEESE Nguyễn Trãi':(60000,100000,'session',60000,100000,'medium'),
 'PHOTO TIME Nguyễn Gia Trí':(70000,110000,'session',70000,110000,'medium'),
 'PHOTO TIME Phú Nhuận':(70000,110000,'session',70000,110000,'low'),
 'PHOTO TIME Crescent Mall':(70000,110000,'session',70000,110000,'low'),
 'PHOTO TIME Sư Vạn Hạnh':(75000,130000,'session',75000,130000,'medium'),
 'PhotoYoyo':(65000,110000,'session',65000,110000,'medium'),
 'Fun Studio Điện Biên Phủ':(100000,200000,'session',100000,200000,'medium'),
 'Photo Story Cửu Long':(60000,100000,'session',60000,100000,'medium'),
 'Flash Box Photobooth':(70000,70000,'session',70000,70000,'low'),
 'Hachi Saigon – ảnh thẻ lấy liền':(80000,80000,'person',160000,160000,'medium'),
 'Gạo Nâu Profile – ảnh thẻ/profile Hàn':(550000,890000,'person',1100000,1780000,'medium'),
 'Fotopop Selfie Studio':(300000,300000,'session',300000,300000,'medium'),
 'NOTE – The Scent Lab (workshop nước hoa cặp đôi)':(550000,None,'person',1100000,None,'medium'),
 'Timeo Tuft Club (tufting len)':(499000,1999000,'person',998000,None,'medium'),
 'Sân khấu kịch IDECAF':(250000,450000,'ticket',500000,900000,'low'),
 'Sân khấu kịch Thiên Đăng':(250000,500000,'ticket',500000,1000000,'low'),
 'The Factory Contemporary Arts Centre':(80000,80000,'ticket',160000,160000,'medium'),
 'Saigon Outcast (leo núi nhân tạo)':(150000,250000,'person',300000,500000,'medium'),
 'Sân Pickleball 189/1 Cống Quỳnh':(150000,300000,'hour',150000,300000,'medium'),
 'M.O.M Cooking Class':(1100000,1100000,'person',2200000,2200000,'medium'),
 'Hoa Túc – lớp nấu ăn':(350000,990000,'person',700000,1980000,'medium'),
 'Board Game Station':(50000,70000,'person',100000,140000,'medium'),
 'Button Boardgames':(None,100000,'person',None,None,'low'),
 'Méo Meo Cat Cafe':(105000,115000,'person',210000,230000,'medium'),
 'Bibli Library Café':(40000,85000,'dish',100000,200000,'medium'),
 'Tour ẩm thực đêm bằng xe máy':(1000000,1050000,'person',2000000,2100000,'medium'),
 'Tour xe đạp đêm Sài Gòn':(1250000,1270000,'person',2500000,2540000,'low'),
 'À Ố Show (xiếc tre – Lune Production)':(800000,1750000,'ticket',1600000,3500000,'high'),
 'Phố ẩm thực Vĩnh Khánh (phố ốc)':(50000,180000,'dish',200000,400000,'medium'),
}
FREE_NOTE = {
 'Đường sách Nguyễn Văn Bình':'Miễn phí vào; sách/cafe tính riêng',
 'Cà phê bệt Nhà thờ Đức Bà':'Miễn phí; nước mua ở xe đẩy ~15–30k/ly (tham khảo)',
 'Bến Bạch Đằng':'Công viên bờ sông miễn phí',
 'Phố Tây Bùi Viện':'Đi dạo miễn phí; đồ uống tại quán tính riêng',
 'Công viên gầm cầu Ba Son':'Công viên công cộng, miễn phí',
 'Công Viên Sala':'Công viên công cộng, miễn phí',
 'Công Viên Văn Hóa Gò Vấp':'Công viên công cộng, vào cửa miễn phí',
 'Công Viên Bờ Sông Sài Gòn Tp Thủ Đức':'Công viên công cộng, miễn phí (trò chơi tính riêng)',
 'City Park, The Global City':'Công viên mở, miễn phí vào',
}
R['WorkFlow Thảo Điền - Working Space & Cafe']=R['WorkFlow Thảo Điền - Working Space & Café']
P('FuniFun! Thiso Mall Trường Chinh - Phan Huy Ích',150000,180000,'ticket',300000,360000,'https://thietkelapdatkhuvuichoi.com/review-khu-vui-choi-funifun/','low','150k ngày thường, 180k cuối tuần/lễ mỗi người (blog 2026; khu vui chơi thiên về gia đình)')
P('Công Viên Vui Chơi Thỏ Trắng',275000,275000,'person',550000,550000,'https://diadiem247.com/tp-ho-chi-minh/cong-vien-giai-tri-tho-trang-le-thi-rieng-l180894.html','low','Vé Couple trọn gói 550k/2 người; vé lẻ trò 20–50k (nguồn có thể lẫn với CN Vũng Tàu)')
P('Khu công viên giải trí D-Joy',40000,60000,'ticket',200000,400000,'https://thietkelapdatkhuvuichoi.com/review-d-joy-nam-sai-gon-quan-7/','low','Không vé cổng; trò lẻ 40–60k/lượt')
P('Gigamall',0,0,'free',0,0,'https://gigamall.com.vn/','medium','TTTM vào cửa miễn phí; trò chơi/ăn uống tính riêng')
