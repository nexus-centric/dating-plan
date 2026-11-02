# Hẹn Hò Sài Gòn 💞 (demo)

Web app (PWA) gợi ý kế hoạch hẹn hò cho cặp đôi ở trung tâm TP.HCM. React + Vite + TypeScript + Tailwind, không backend.

## Chạy
```bash
npm install
npm run dev        # http://localhost:5173
npm run build      # kiểm tra TS + build ra dist/
npm run preview    # http://localhost:4173
```

## Dữ liệu (cập nhật 26/10/2026)
- `src/data.json` = bản copy của `data/merged_hcm.json`, sinh bởi `python3 scripts/merge_v2.py` từ:
  `data/research_hcm.json` (nghiên cứu web) + `data/web_additions.json` + `data/new_types_hcm.json` + list Bliss Home (`data/bliss_home_places.json`).
- Địa chỉ Bliss lấy từ trang Google Maps công khai của từng địa điểm (`scripts/gm_details.cjs` → `data/raw_bliss/_gm_details.json`);
  quận suy ra từ toạ độ Google Maps + ranh giới quận cũ (GADM, `scripts/geo_util.py`). Không tìm được địa chỉ → `data/unresolved_bliss.json`.
- Loại ra: `data/excluded_hcm.json` (ngoài trung tâm / ngoài TP.HCM, đóng cửa vĩnh viễn). Trùng lặp đã gộp: `data/duplicates_merged.json`.
- lat/lng: toạ độ Google Maps (Bliss) hoặc Nominatim (`scripts/forward_geocode.py`, 1 req/s, chỉ nhận khi đúng quận).
- Trường thêm: `rating, reviews, lat, lng, lists, maps_url, website, google_category, area` (quận chuẩn hoá), `kind` (loại dùng cho planner), `hours` ([mở, đóng] phút).
- Bộ lọc khu vực lấy tự động từ `area` trong dữ liệu (`DISTRICTS` trong `src/data.ts`).

## Planner
- Quy tắc slot & combo: xem đầu `src/planner.ts` (bữa tối chỉ nhà hàng/phố ẩm thực; bar/rooftop/cafe/dessert ở slot 2).
- Hai điểm luôn cùng quận hoặc quận kề (`ADJ_LIST`), hiện khoảng cách km nếu có toạ độ; giờ mở cửa không khớp = phạt điểm mềm + cảnh báo.
- Ảnh: thêm `"image": "https://..."` hoặc `/photos/x.jpg` trong `public/photos/`.

## Ảnh chụp màn hình
`npm run build && npx vite preview --port 4173 &` rồi `node scripts/screenshots.cjs` → `screenshots/`.

## Deploy miễn phí
- **Cloudflare Pages**: kết nối repo → Build command `npm run build`, output `dist`. Hoặc `npx wrangler pages deploy dist`.
- **Vercel**: import repo (preset Vite tự nhận) hoặc `npx vercel --prod`.
