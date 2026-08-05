# Ảnh sản phẩm (tùy chọn)

Bot lệnh `/xem` chọn ảnh theo thứ tự:

1. File trong thư mục **`img/`** nếu có trong `data/img_folder_map.json` (tên file rút gọn của bạn).
2. File local tại đây, **tên file = đúng tên sản phẩm** + đuôi `.jpg` / `.png` / `.jpeg` (bỏ ký tự `\ / : * ? " < > |` nếu có trong tên).
3. File `default.jpg` trong thư mục này.
4. Trường **`image_url`** trên document trong Cosmos (seed `data/seed_products.py` gán sẵn URL placeholder).
5. Ảnh stock (Unsplash) theo từ khóa trong tên sản phẩm.

Ví dụ: sản phẩm *Sữa rửa mặt Cetaphil* → đặt file `Sữa rửa mặt Cetaphil.jpg` để luôn hiển thị ảnh của bạn, không cần đổi database.

Danh sách đủ 49 tên chuẩn (nếu đặt ảnh trực tiếp trong `images/`): xem `EXPECTED_FILENAMES.txt` (tạo lại bằng `python data/list_expected_image_files.py`).

Ảnh thật nên để trong **`img/`** và map trong `data/img_folder_map.json` (xem `img/README.md`). Sản phẩm không map và không có file trong `images/` sẽ dùng `image_url` trên Cosmos hoặc ảnh Unsplash.
