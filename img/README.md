# Ảnh sản phẩm (tên file tự đặt)

Bot map từ **tên đầy đủ trong database** → file trong thư mục này qua `data/img_folder_map.json`.

- **`AVT.jpg`**: ảnh đại diện bot — dùng trên [@BotFather](https://t.me/BotFather) (Set Bot Profile Picture), **không** dùng cho lệnh `/xem`.

## Thêm ảnh mới

1. Đặt file `.jpg` / `.png` vào `img/`.
2. Mở `data/img_folder_map.json`, thêm một dòng:  
   `"Tên sản phẩm đúng y trong DB": "img/tên_file_bạn.jpg"`

Tên sản phẩm phải **khớp 100%** với trường `name` trong Cosmos / `data/seed_products.py`. Danh sách chuẩn: `images/EXPECTED_FILENAMES.txt` (bỏ đuôi `.jpg`).

## Sản phẩm chưa có ảnh trong `img/` (đang dùng `images/` hoặc URL)

Còn 19 SP chưa map — khi có ảnh, thêm file + dòng trong JSON:

- Toner hoa cúc Kiehl's Calendula  
- Tẩy tế bào chết vật lý Cure Natural Aqua  
- Tẩy da chết COSRX BHA Blackhead Power  
- Serum phục hồi La Roche-Posay Hyalu B5  
- Serum cấp nước Timeless B5 Hydration  
- Serum dưỡng trắng Melano CC  
- Serum chống lão hoá Obagi Retinol 0.5  
- Kem dưỡng ẩm Clinique Moisture Surge  
- Kem dưỡng ẩm Laneige Water Bank  
- Kem dưỡng ngải cứu I'm From Mugwort  
- Kem chống nắng Skin1004 Madagascar  
- Kem chống nắng MartiDerm The Originals  
- Kem chống nắng Cell Fusion C Clear  
- Mặt nạ ngủ Laneige Water Sleeping Mask  
- Mặt nạ giấy Naruko Tràm Trà  
- Kem mắt Clinique All About Eyes  
- Dầu tẩy trang Shu Uemura Anti/Oxi+  
- Xịt khoáng La Roche-Posay Serozinc  
- Kem chấm mụn Mario Badescu Drying Lotion  
