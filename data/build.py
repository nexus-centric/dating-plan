import json
D="2026-10-25"
S=dict(caubason="https://caubason.com/dia-diem-hen-ho-sai-gon/",mia="https://mia.vn/cam-nang-du-lich/cac-dia-diem-hen-ho-o-sai-gon-17524",
park="https://theparksaigon.com/top-dia-diem-hen-ho-lang-man-buoi-toi-tai-quan-1-the-park-rooftop/",pin="https://pinguide.city/district-1/guides/date-ideas-saigon-district-1/",
elle="https://www.elle.vn/trai-nghiem/workshop-cho-cap-doi-tai-sai-gon-valentine/",tripi="https://tripi.vn/blog/vi/kinh-nghiem-hay/kham-pha-nhung-workshop-tuyet-voi-tai-sai-gon-danh-cho-cac-cap-doi-trong-mua-valentine-tripi",
exaw="https://exa.ai/library/places?q=4cac557f6aba4b85",vietbao="https://vietbao.vn/nhung-workshop-o-sai-gon-danh-cho-cac-cap-doi-vao-moi-cuoi-tuan-581347.html",
vi="https://vietinsiders.com/goi-y/workshop-cho-cap-doi-tphcm/",bay="https://www.bayhotelhcm.com/propeller-rooftop-bar-in-district-1/",zion="https://zionskyloungesaigon.com/en/book",
momento="https://www.tripadvisor.com.au/Restaurant_Review-g293925-d26635082-Reviews-Momento_Rooftop-Ho_Chi_Minh_City.html",tc="https://www.tripcurator.travel/guides/hcmc-rooftop-bars.html",
grand="https://www.therooftopguide.com/rooftop-bars-in-ho-chi-minh/rooftop-grand-lounge.html",master="https://masterescape.vn/",vspot="https://vietnamspot.ru/en/blog/ho-chi-minh-entertainment",
exae="https://exa.ai/library/places?q=ed4ff25247a365dd",pasta="https://pastafrescasaigon.com/en/fun-to-play/",zalo="https://zalopay.vn/quan-ca-phe-quan-3-4965",
ttg="https://thuytinhgiare.com/quan-ca-phe-tinh-nhan.html",p1="https://1phutsaigon.vn/quan-cafe-hen-ho-cuc-chat/",tripic="https://tripi.vn/blog/vi/xep-hang/top-12-quan-ca-phe-lang-man-nhat-sai-gon-danh-cho-cac-cap-doi-tripi",
lemon="https://www.lemon8-app.com/restaurants/7172860750032142850?region=vn",syphu="https://www.syphu.com.vn/quan-an-lang-man-cho-2-nguoi-o-sai-gon/",butcher="https://pasgo.vn/nha-hang/the-butcher-shop-and-grill-nguyen-ba-lan-3762",
water="https://mia.vn/cam-nang-du-lich/water-bus-saigon-12411",water2="https://saigonwaterbus.com/water-bus",htk="https://mytour.vn/vi/blog/bai-viet/cho-dem-ho-thi-ky-diem-hen-soi-dong-nhat-tphcm.html",
htk2="https://saigonvivu.com/cho-dem-sai-gon/",bmt="http://www.baotangmythuattphcm.com.vn/",didau="https://didau.com/giua-long-sai-gon-xuat-hien-1-tiem-banh-phap-cuc-ky-lang-man-chon-hen-ho-tra-banh-ly-tuong-khong-phai-ai-cung-biet",
exad="https://exa.ai/library/places?q=e40ccf5d68b3d696",exad2="https://exa.ai/library/places?q=218539db345c4270",sky="https://divui.com/blog/kinh-nghiem-tham-quan-saigon-skydeck-bitexco-2026/",
tcv="https://vietair.com.vn/du-lich-trong-nuoc/gia-ve-thao-cam-vien.html",btp="https://www.benthanhprincess.com.vn/vi/dining-experiences/",cgv="https://www.cgv.vn/en/theaters/special/sweetbox",
cgv2="https://rapchieuphim.com/rap/cgv-liberty-citypoint",war="https://www.baotangchungtichchientranh.vn/",mytour="https://mytour.vn/vi/blog/bai-viet/danh-sach-6-dia-diem-an-uong-lang-man-rieng-tu-de-hen-ho-o-quan-1-nhanh-chong-duoc-cac-cap-doi-ghi-lai.html")
items=[]
def A(name,typ,cat,dist,addr,price,hours,moods,desc,src,note=None,source="web",out=False):
    items.append(dict(name=name,type=typ,category=cat,district=dist,address=addr,price_per_couple_vnd=price,price_note=note,opening_hours=hours,mood_tags=moods,description_vi=desc,source_urls=[S.get(s,s) for s in src],source=source,out_of_area=out,status="likely_operating" if source=="web" else "user_provided",date_checked=D))
F,Ac,I="food","activity","idea"
# FOOD
A("The Park Rooftop Bar & Lounge",F,"rooftop bar","Quận 1","Tầng 5, 20 Đỗ Quang Đẩu, P. Phạm Ngũ Lão, Q.1",None,"Từ 17:00 đến khuya",["lãng mạn","chill","đêm muộn"],"Rooftop cocktail view phố, có acoustic/DJ cuối tuần.",["park","caubason"])
A("Propeller Rooftop Bar (Bay Hotel)",F,"rooftop bar","Quận 1","Tầng 17, 7 Ngô Văn Năm, Q.1",None,"16:00–23:00, đóng cửa thứ Hai",["lãng mạn","sang chảnh"],"Rooftop tầng 17 view sông Sài Gòn và hoàng hôn.",["bay"])
A("Zion Sky Lounge & Dining",F,"rooftop bar","Quận 1","Tầng 14, 87A Hàm Nghi, Q.1",None,"16:00–03:00 hằng ngày",["sang chảnh","đêm muộn"],"Sky lounge tầng 14, có ghi chú chuẩn bị cho sinh nhật/kỷ niệm khi đặt bàn.",["zion"])
A("Momento Rooftop (trước đây Cocoon Rooftop)",F,"rooftop bar","Quận 1","Tầng 8, 105 Cô Giang, Q.1",None,"16:00–00:30; T6–T7 đến 04:00",["chill","đêm muộn"],"Rooftop ngoài trời nhạc hay, pizza và cocktail giữa trung tâm.",["momento"])
A("Chill Skybar (AB Tower)",F,"rooftop bar","Quận 1","Tầng 76, AB Tower, 2 Hải Triều, Q.1 (theo nguồn)",400000,"17:00–02:00",["sang chảnh","lãng mạn","đêm muộn"],"Rooftop cao, view 360° thành phố, dress code smart casual.",["tc"],note="Min spend 200.000đ/người theo TripCurator (tháng 5/2026); nguồn ghi vị trí lẫn lộn AB Tower/Bitexco — cần kiểm tra địa chỉ")
A("Rooftop Grand Lounge (Hotel Grand Saigon)",F,"rooftop bar/nhà hàng","Quận 1","8 Đồng Khởi, Q.1",None,"06:00–00:00 hằng ngày",["sang chảnh","lãng mạn"],"Rooftop tầng 20 trong khách sạn cổ, view sông, có ban nhạc sống.",["grand"])
A("Bar57",F,"bar","Quận 1","57 Nguyễn Du, Q.1",None,None,["lãng mạn","đêm muộn"],"Quán bar được gợi ý cho buổi tối hẹn hò ở Q.1.",["park"])
A("The Refinery",F,"nhà hàng/bistro","Quận 1","74 Hai Bà Trưng, Q.1",None,None,["lãng mạn","chill"],"Bistro yên tĩnh, riêng tư được gợi ý cho cặp đôi.",["pin"])
A("Cork and Bottle",F,"wine bar","Quận 1","7 Thái Văn Lung, Q.1",None,None,["lãng mạn","sang chảnh"],"Quán rượu vang nhỏ, không gian yên tĩnh.",["pin"])
A("CỘI",F,"nhà hàng Việt","Quận 1","77–79 Lý Tự Trọng, Q.1",None,None,["lãng mạn","chill"],"Nhà hàng không gian riêng tư, ấm cúng ở trung tâm.",["pin"])
A("Trên Tầng Thượng",F,"cafe","Quận 3","540/19 Cách Mạng Tháng Tám, P.11, Q.3",None,"07:00–23:30",["chill","lãng mạn"],"Cafe trên tầng thượng nhà máy cũ, view sân ga, nhạc nhẹ 19:30–21:30.",["zalo"],note="Giá đồ uống 60.000–75.000đ/món")
A("3Đ Chill Cafe",F,"cafe","Quận 3","120/4 Trần Quốc Thảo, P.14, Q.3",None,"07:00–22:00",["chill","ngày mưa","rẻ mà vui"],"Cafe trong hẻm, sân cây xanh, gạch bông vintage.",["zalo"],note="Giá đồ uống 45.000–60.000đ/món")
A("OZ Coffee House",F,"cafe","Quận 3 / Bình Thạnh","CS: 207/31 Lê Văn Sỹ Q.3; 30 Huỳnh Tịnh Của Q.3; 273/46 Nguyễn Văn Đậu Bình Thạnh",None,"08:00–23:30 (Huỳnh Tịnh Của: 08:00–22:00)",["lãng mạn","chill","ngày mưa"],"Cafe tình nhân quốc dân, có phòng riêng cho 2 người.",["zalo","ttg"],note="Giá 30.000–250.000đ/món tùy chi nhánh")
A("Oromia Coffee & Lounge",F,"cafe","Quận 3","193A/D3 Nam Kỳ Khởi Nghĩa, Q.3 (nguồn khác ghi 93A/D3)",None,"07:00–22:00/23:00",["chill","lãng mạn"],"Cafe trong hẻm có hồ cá Koi, lên đèn buổi tối.",["ttg","p1"],note="Giá 40.000–150.000đ/món; địa chỉ các nguồn không thống nhất")
A("Lavender",F,"cafe","Quận 3","384/40 Nam Kỳ Khởi Nghĩa, P.8, Q.3",None,"08:00–21:00",["lãng mạn","chill"],"Cafe phong cách Pháp tông tím oải hương.",["ttg"],note="Từ 49.000đ/món")
A("Pergola Cafe",F,"cafe","Phú Nhuận","28A Trần Cao Vân, P.12, Phú Nhuận",None,"07:00–23:00",["lãng mạn","chill"],"Cafe sân vườn phong cách châu Âu cổ điển.",["ttg"])
A("Nến Cafe",F,"cafe","Phú Nhuận","110A Nguyễn Đình Chính, P.15, Phú Nhuận",None,"07:00–23:00",["lãng mạn","ngày mưa"],"Cafe ánh nến với 6 khu vực phong cách khác nhau.",["ttg"],note="Giá 30.000–110.000đ/món")
A("The Dome Kaffe",F,"cafe","Phú Nhuận","10/16 Đoàn Thị Điểm, Phú Nhuận",None,"09:30–22:00 (nguồn khác 08:00–22:00)",["chill","ngày mưa"],"Cafe tối giản đen trắng kiểu Hàn, bánh ngọt đẹp.",["tripic","p1"])
A("Ráng Chiều Rooftop",F,"rooftop cafe","Phú Nhuận","39A Trần Khắc Chân, P.15, Phú Nhuận",None,"16:00–23:30",["chill","lãng mạn","rẻ mà vui"],"Rooftop bình dân ngắm hoàng hôn.",["p1"])
A("Trăng Non Rooftop",F,"rooftop cafe","Bình Thạnh","302 Nguyễn Văn Đậu, Bình Thạnh",None,"17:00–23:30",["lãng mạn","chill"],"Rooftop như khu rừng nhỏ, đèn vàng ngắm sao.",["p1"])
A("Chạng Vạng Rooftop Hàng Xanh",F,"rooftop cafe","Bình Thạnh","72/6 P.24, Bình Thạnh",None,"08:00–22:00",["chill","rẻ mà vui"],"Rooftop lâu đời, acoustic cuối tuần.",["p1"])
A("Cà phê Thủy Trúc",F,"cafe sân vườn","Bình Thạnh","197 Đinh Bộ Lĩnh, P.26, Bình Thạnh",None,"07:00–21:00",["chill","rẻ mà vui"],"Cafe sân vườn kiểu đồng quê có suối, cầu nhỏ.",["ttg"],note="Giá 35.000–100.000đ/món")
A("The Deck Saigon",F,"nhà hàng","Thảo Điền (TP Thủ Đức)","38 Nguyễn Ư Dĩ, Thảo Điền",None,None,["lãng mạn","sang chảnh"],"Nhà hàng view sông Sài Gòn sang trọng.",["lemon"],note="Nguồn: khoảng 200.000–800.000đ/người (tóm tắt tìm kiếm, chưa mở trang gốc)")
A("Quán Bụi Garden",F,"nhà hàng Việt","Thảo Điền (TP Thủ Đức)","55A Ngô Quang Huy, Thảo Điền",None,None,["chill","lãng mạn"],"Nhà hàng sân vườn món Việt yên tĩnh.",["syphu"],note="Khoảng 50.000–250.000đ/người theo tóm tắt tìm kiếm")
A("The Butcher Shop & Grill",F,"steakhouse","Thảo Điền (TP Thủ Đức)","29 Nguyễn Bá Lân, Thảo Điền",None,None,["lãng mạn","sang chảnh"],"Nhà hàng steak & món Âu ấm cúng.",["butcher"],note="Khoảng 200.000–400.000đ/người")
A("Vérité Patisserie",F,"tiệm bánh/dessert","Quận 1","84/1 Trần Đình Xu, Q.1",None,None,["lãng mạn","chill"],"Tiệm bánh Pháp, nhạc piano/violin cuối tuần.",["didau"])
A("Châteraisé Lê Thánh Tôn",F,"dessert","Quận 1","29A Lê Thánh Tôn, Q.1",None,None,["chill","ngày mưa"],"Tiệm bánh Nhật tối giản, nhiều tầng ngồi.",["exad"])
A("Tarobu Dessert",F,"dessert","Quận 3","204C Điện Biên Phủ, Q.3",None,"12:00–22:00",["chill","rẻ mà vui"],"Quán chè/dessert cho buổi chiều tối.",["exad2"])
A("Chợ ẩm thực Hồ Thị Kỷ",F,"chợ đêm/street food","Quận 10","Hẻm Hồ Thị Kỷ, Q.10",None,"Khoảng 15:00–23:00",["rẻ mà vui","năng động","đêm muộn"],"Chợ ẩm thực đường phố sôi động, không thu vé.",["htk","htk2"])
A("Benthanh Princess – du thuyền ăn tối",F,"du thuyền nhà hàng","Quận 1 (bến sông Sài Gòn)",None,1960000,None,["lãng mạn","sang chảnh","kỷ niệm"],"Du thuyền ăn tối 2 giờ trên sông Sài Gòn.",["btp"],note="Set menu 2026 từ 980.000đ/người (đã gồm thuế, phí, vé thuyền)")
A("Tròn Kitchen",F,"nhà hàng","Quận 3","262c Đ. Lê Văn Sỹ, Phường 14, Quận 3",None,None,[],"Nhà hàng do người dùng gợi ý.",[],source="user")
# ACTIVITIES
A("Phố đi bộ Nguyễn Huệ",Ac,"đi dạo","Quận 1","Đường Nguyễn Huệ, Q.1",0,"Đẹp nhất sau 18:00",["rẻ mà vui","lãng mạn","đêm muộn"],"Dạo phố đi bộ, nghe nhạc đường phố, nhạc nước cuối tuần.",["caubason","mia"],note="Miễn phí vào; giá 0 chỉ là phí vào cửa")
A("Đường sách Nguyễn Văn Bình",Ac,"đi dạo/sách","Quận 1","Đường Nguyễn Văn Bình, cạnh Nhà thờ Đức Bà, Q.1",None,None,["chill","rẻ mà vui"],"Con đường sách rợp cây, đọc sách và cafe.",["caubason"])
A("Cà phê bệt Nhà thờ Đức Bà",Ac,"đi dạo","Quận 1","Công xã Paris, Q.1",None,None,["rẻ mà vui","chill"],"Ngồi bệt uống cafe ngắm phố quanh nhà thờ.",["mia"],note="Khu vực nhà thờ có thể đang trùng tu")
A("Thảo Cầm Viên",Ac,"công viên/sở thú","Quận 1",None,120000,None,["chill","rẻ mà vui"],"Dạo vườn cây cổ thụ, nhà kính lan, chụp ảnh vintage.",["caubason","tcv"],note="Vé người lớn 60.000đ")
A("Nhà hát Thành phố",Ac,"nghệ thuật/biểu diễn","Quận 1","7 Công trường Lam Sơn, Q.1",None,None,["sang chảnh","lãng mạn"],"Xem opera, kịch, biểu diễn trong nhà hát cổ.",["mia"])
A("Phố Tây Bùi Viện",Ac,"phố đêm","Quận 1","Phố Bùi Viện, Q.1",None,None,["năng động","đêm muộn"],"Phố đêm náo nhiệt với bar và quán ăn.",["mia"])
A("Bến Bạch Đằng",Ac,"bờ sông","Quận 1","Đường Tôn Đức Thắng, Q.1",None,None,["lãng mạn","rẻ mà vui"],"Ngắm sông và thành phố lên đèn.",["mia"])
A("Buýt đường sông Sài Gòn (Water Bus)",Ac,"thuyền trên sông","Quận 1 (ga Bạch Đằng)",None,60000,"Hằng ngày, theo lịch tàu trên website",["lãng mạn","rẻ mà vui"],"Đi buýt sông ngắm thành phố từ mặt nước.",["water","water2"],note="15.000đ/lượt, khứ hồi 30.000đ/người")
A("Saigon Skydeck (Bitexco)",Ac,"điểm ngắm cảnh","Quận 1","Bitexco Financial Tower, 2 Hải Triều, Q.1",480000,"09:30–21:30",["lãng mạn","ngày mưa"],"Ngắm toàn cảnh Sài Gòn từ trên cao lúc hoàng hôn.",["sky"],note="Vé người lớn 240.000đ")
A("Bảo tàng Mỹ thuật TP.HCM",Ac,"bảo tàng","Quận 1",None,120000,"08:00–17:00 hằng ngày",["chill","ngày mưa"],"Xem tranh trong tòa nhà Pháp cổ.",["bmt"],note="Từ 1/10/2026 vé 60.000đ/người (theo tóm tắt tìm kiếm)")
A("Bảo tàng Chứng tích Chiến tranh",Ac,"bảo tàng","Quận 3",None,None,"07:30–17:30 hằng ngày (bán vé đến 17:00)",["ngày mưa"],"Bảo tàng lịch sử, phù hợp cặp đôi thích tìm hiểu.",["war"])
A("CGV Liberty Citypoint – Sweetbox",Ac,"rạp chiếu phim","Quận 1","59–61 Pasteur, Q.1",None,None,["ngày mưa","lãng mạn"],"Rạp có ghế đôi Sweetbox vách ngăn cao.",["cgv2","cgv"])
A("Gốm Sài Gòn",Ac,"workshop gốm","Quận 1 / Quận 3","26 Lý Tự Trọng Q.1; 42 Nguyễn Huệ Q.1; 6C Tú Xương Q.3",900000,"CN 6C Tú Xương: 08:00–22:00 (Maps)",["kỷ niệm","ngày mưa","chill"],"Workshop làm gốm 3 giờ, tự tay tạo hình và trang trí.",["elle","tripi","exaw","vietbao"],note="Khoảng 450.000đ/người tại 6C Tú Xương (Tripi); CN 42 Nguyễn Huệ chỉ có trong bài ELLE cũ — cần kiểm tra")
A("Tipsy Art",Ac,"workshop vẽ tranh","Quận 1","6B Nguyễn Cảnh Chân, P. Nguyễn Cư Trinh, Q.1",None,None,["kỷ niệm","ngày mưa"],"Workshop vẽ tranh 3 giờ có họa sĩ hướng dẫn.",["elle"])
A("Coming Home Candle",Ac,"workshop nến","Quận 1","Lầu 1, 158/17 Nguyễn Công Trứ, Q.1",None,None,["kỷ niệm","lãng mạn","ngày mưa"],"Tự làm nến thơm tạo hình làm quà tặng.",["elle","exaw"])
A("Haru Craft Ceramic Studio",Ac,"workshop gốm","Bình Thạnh","15/10 Nguyễn Huy Tưởng, Bình Thạnh",None,None,["kỷ niệm","chill"],"Studio gốm tối giản kiểu Hàn cho cặp đôi.",["vi"],note="300.000–600.000đ/buổi (không rõ người hay buổi)")
A("Clover Pottery Studio & Cafe",Ac,"workshop gốm","Bình Thạnh","193 Lê Quang Định, Bình Thạnh",None,None,["chill","rẻ mà vui"],"Vừa uống cafe vừa nặn gốm, không dùng bàn xoay.",["vi"],note="250.000–450.000đ (đơn vị không rõ)")
A("Bibouyo",Ac,"workshop vẽ tranh","Thảo Điền (TP Thủ Đức)","191B Nguyễn Văn Hưởng, Thảo Điền",600000,None,["kỷ niệm","chill"],"Vẽ tranh trong không gian như phòng triển lãm nhỏ.",["vi"],note="Từ 300.000đ/người")
A("Master Escape Room",Ac,"escape room","Quận 10 / Phú Nhuận","268 Tô Hiến Thành Q.10; Tầng 4, 240 Nguyễn Đình Chính, Phú Nhuận",None,None,["năng động","ngày mưa"],"Giải đố 60 phút; phòng 'Liên' cho 2–8 người.",["master"])
A("Karaoke ICOOL Thành Thái",Ac,"karaoke","Quận 10","120 Thành Thái, Q.10",None,"24/7 (Maps)",["năng động","đêm muộn","ngày mưa"],"Phòng karaoke riêng, âm thanh tốt.",["exae","vspot"],note="iCool 120.000–350.000đ/giờ/phòng (VietnamSpot 7/2026)")
A("Bowling Vạn Hạnh Mall",Ac,"bowling","Quận 10","Tầng 5, 11 Sư Vạn Hạnh, Q.10",None,None,["năng động","ngày mưa"],"Chơi bowling trong trung tâm thương mại.",["pasta"],note="Nguồn chung: 60.000–100.000đ/người/game; chưa xác nhận còn hoạt động")
A("Trượt băng Vincom Landmark 81",Ac,"trượt băng","Bình Thạnh","Landmark 81, Bình Thạnh",None,None,["năng động","ngày mưa"],"Trượt băng trong nhà cùng nhau.",[],source="user")
A("Bắn cung ở Cung Văn hóa Lao động",Ac,"thể thao","Quận 1","Cung Văn hóa Lao động, Q.1",None,None,["năng động"],"Thử bắn cung cùng nhau giữa trung tâm.",[],source="user")
A("Cắm trại suối La Ngâu (2N1Đ/3N2Đ)",Ac,"chuyến đi xa","Bình Thuận (ngoài HCM)",None,None,None,["năng động","kỷ niệm"],"Cắm trại ở suối La Ngâu, đi xe máy khoảng 4–5 giờ.",[],source="user",out=True)
# IDEAS
for n,d,m in [("Sáng tác bài hát tặng đối phương (AI hỗ trợ)","Cùng AI viết và thu một bài hát tặng người ấy.",["kỷ niệm","lãng mạn"]),
("Tạo công thức nước uống đặt tên theo đối phương","Pha chế đồ uống riêng và đặt tên theo người ấy.",["kỷ niệm","rẻ mà vui"]),
("DIY theo TikTok rồi cùng đi mua đồ về làm","Chọn video DIY cute, đi mua nguyên liệu và làm cùng nhau, rời xa điện thoại.",["chill","ngày mưa"]),
("Homestay double date đổi phòng (gợi ý Bliss Home)","Rủ thêm một cặp, book 2 phòng, setup hoạt động cho cặp kia rồi đổi phòng (máy chiếu, nấu ăn, bida, PS4, boardgame, Nintendo, lego).",["năng động","kỷ niệm"]),
("Đổi quần áo cho nhau, nấu ăn và chụp ảnh","Mặc đồ của nhau, cùng nấu ăn và chụp ảnh kỷ niệm.",["rẻ mà vui","kỷ niệm"])]:
    A(n,I,"idea",None,None,None,None,m,d,[],source="user")
for it in items:
    if it["name"] in("Bowling Vạn Hạnh Mall","Cà phê bệt Nhà thờ Đức Bà","Chill Skybar (AB Tower)"): it["status"]="uncertain"
json.dump(items,open("research_hcm.json","w"),ensure_ascii=False,indent=1)
lists={"Homestay date":"JstNKoGpSRf4jUiH8","Work date":"sZJi6rErfWy9TMoU8","Shopping date":"3CNqX3m9q8M4BPoH9","Spa date":"MvXmS43BR6Qd31jf8","Tổ hợp game date":"EYfYJYynFmzsTPiM8","Picnic date":"7Ue1uSXuk6h3vXL77","Check-in date":"otUdBrSjCje92v6J8","Photobooth date":"QqvwiYgZV9thEnW1A","Deep talk date":"jyL4V8KgepKC92d86","Fine Dining date":"H8ftWDMThzsZNvWz5","Workshop date":"yhnNcKAgV1tpc7vy7"}
json.dump([dict(category=k,url="https://maps.app.goo.gl/"+v,readable=False,places=[],note="Redirects to JS-only Google Maps page; contents need a browser") for k,v in lists.items()],open("bliss_home_maps_lists.json","w"),ensure_ascii=False,indent=1)
L=["# Research HCM date ideas (checked "+D+")\n","| # | Tên | Type | Category | Quận | Giá/cặp (VND) | Giờ | Mood | Mô tả | Status | Nguồn |","|---|---|---|---|---|---|---|---|---|---|---|"]
for i,x in enumerate(items,1):
    p=x["price_per_couple_vnd"]; p=("" if p is None else f"{p:,}")+((" ("+x["price_note"]+")") if x["price_note"] else "")
    L.append(f"| {i} | {x['name']} | {x['type']} | {x['category']} | {x['district'] or ''} | {p or 'null'} | {x['opening_hours'] or ''} | {', '.join(x['mood_tags'])} | {x['description_vi']} | {x['status']}{' OUT_OF_AREA' if x['out_of_area'] else ''} | {' '.join(x['source_urls']) or 'user'} |")
L+=["\n## Bliss Home Google Maps lists (chưa đọc được)\n"]+[f"- {k}: https://maps.app.goo.gl/{v}" for k,v in lists.items()]
open("research_hcm.md","w").write("\n".join(L))
from collections import Counter
print(Counter(x["type"] for x in items)); print(Counter((x["type"],x["district"]) for x in items))
