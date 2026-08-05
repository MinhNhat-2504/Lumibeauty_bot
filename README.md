# Lumi Beauty Bot

Chatbot Telegram tư vấn mỹ phẩm, kèm một trang admin để quản lý đơn hàng. Đây là đồ án môn Điện toán đám mây của mình: dữ liệu để trên Azure Cosmos DB, phần tư vấn dùng Gemini, đóng gói bằng Docker cho dễ deploy.

Bot tên là Lumi, trả lời tiếng Việt. Khách có thể gõ lệnh hoặc cứ nhắn tin bình thường, cả hai đều chạy được.

## Bot làm được gì

| Lệnh | Công dụng |
|---|---|
| `/start` | Lời chào + danh sách lệnh |
| `/skintype` | Chọn loại da (da dầu / khô / hỗn hợp / nhạy cảm), lưu lại vào DB |
| `/recommend` | Gợi ý sản phẩm dựa trên loại da đã lưu |
| `/products` | Duyệt sản phẩm theo danh mục, có gửi kèm ảnh |
| `/search <từ khóa>` | Tìm theo tên hoặc mô tả |
| `/xem <tên SP>` | Gửi ảnh sản phẩm cỡ lớn |
| `/order` | Đặt hàng, hỏi từng bước rồi mới chốt |
| `/myorder` | Xem 10 đơn gần nhất |
| `/ask <câu hỏi>` | Hỏi AI tư vấn da |

Nhắn tin thường (không có `/`) thì bot đẩy sang Gemini trả lời. Mình có nhét cả danh sách sản phẩm trong shop vào prompt nên nó chỉ gợi ý hàng đang có, và khi khách muốn mua thì nó hướng khách gõ `/order` chứ không tự chốt đơn.

`/order` là một ConversationHandler 5 bước: chọn sản phẩm → số lượng → tên người nhận → địa chỉ → bấm nút xác nhận. Đang đặt hàng dở mà muốn thoát thì gõ `/cancel`.

## Trang admin

Chạy riêng bằng Flask ở cổng 5050:

- Thống kê tổng user, đơn hàng, sản phẩm và doanh thu (đơn đã hủy thì không tính)
- Xem / tìm / xóa user
- Lọc đơn theo trạng thái và đổi trạng thái trực tiếp
- Xem toàn bộ catalog sản phẩm

Giao diện là một file `templates/dashboard.html` thuần HTML/CSS/JS, gọi mấy endpoint `/api/stats`, `/api/users`, `/api/orders`, `/api/products`.

## Công nghệ

- Python 3.10
- python-telegram-bot 20+ (async)
- Azure Cosmos DB (NoSQL) — 3 container: `users`, `orders`, `products`
- Google Gemini (`google-generativeai`)
- Flask cho trang admin
- Docker

## Chạy thử ở máy

```bash
git clone https://github.com/MinhNhat-2504/Lumibeauty_bot.git
cd Lumibeauty_bot

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

Copy `.env.example` thành `.env` rồi điền key vào:

```env
TELEGRAM_TOKEN=...
COSMOS_ENDPOINT=https://<tên-account>.documents.azure.com:443/
COSMOS_KEY=...
COSMOS_DATABASE=lumibeauty
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.0-flash
```

Chỗ lấy key: `TELEGRAM_TOKEN` xin ở [@BotFather](https://t.me/BotFather), `GEMINI_API_KEY` lấy tại [Google AI Studio](https://aistudio.google.com/apikey), còn hai biến Cosmos vào Azure Portal → Cosmos DB → mục Keys.

Đổ dữ liệu sản phẩm (64 sản phẩm mẫu), chỉ chạy **một lần** duy nhất:

```bash
python data/seed_products.py
```

Rồi bật bot và trang admin ở hai terminal khác nhau:

```bash
python app.py         # bot, chế độ long polling
python dashboard.py   # admin, mở http://localhost:5050
```

Database và container không cần tạo tay, code dùng `create_*_if_not_exists` nên lần chạy đầu nó tự tạo.

## Cấu trúc thư mục

```
app.py                  # điểm khởi động bot, đăng ký handler
dashboard.py            # Flask server cho trang admin
Dockerfile
requirements.txt

bot/
  handlers.py           # toàn bộ logic lệnh, dài nhất repo
  ai.py                 # gọi Gemini, dựng prompt kèm danh sách sản phẩm
  keyboards.py          # các inline keyboard
  messages.py           # text cố định + hàm format

database/
  cosmos.py             # kết nối Cosmos, cache client và container
  users.py              # partition key /telegram_id
  orders.py             # partition key /user_id
  products.py           # partition key /id

data/
  seed_products.py      # dữ liệu sản phẩm mẫu
  img_folder_map.json   # map tên sản phẩm -> tên file ảnh

img/                    # ảnh sản phẩm
images/                 # thư mục ảnh phụ (xem phần lưu ý)
templates/dashboard.html
```

## Deploy bằng Docker

```bash
docker build -t lumi-beauty-bot .
docker run --env-file .env -p 8443:8443 lumi-beauty-bot
```

Khi đưa lên Cloud Run hay Render thì thêm mấy biến này, bot sẽ tự chuyển từ polling sang webhook:

```env
ENVIRONMENT=production
WEBHOOK_URL=https://<url-service-của-bạn>
PORT=8080
```

Dockerfile mặc định chạy `app.py`. Muốn chạy trang admin trong container thì override lệnh: `docker run ... lumi-beauty-bot python dashboard.py`.

## Vài chỗ cần lưu ý

**Đừng chạy `seed_products.py` hai lần.** Script sinh `uuid` mới mỗi lần chạy nên chạy lại là dữ liệu nhân đôi chứ không ghi đè. Lỡ chạy rồi thì xóa container `products` trên Azure Portal rồi seed lại.

**Cách bot tìm ảnh.** Ưu tiên file trong `img/` theo mapping ở `data/img_folder_map.json`, không có thì tìm trong `images/` theo đúng tên sản phẩm, rồi tới `images/default.jpg`, cuối cùng mới fallback ra link ảnh trên mạng. Thêm ảnh mới thì bỏ file vào `img/` và nhớ khai báo trong file JSON.

**Handler lệnh đăng ký ở `group=-1`.** Làm vậy để đang trong luồng `/order` vẫn gõ được `/xem` hay `/products`, nếu để group mặc định thì ConversationHandler nuốt hết tin nhắn.

**Model Gemini có fallback.** Google hay đổi tên model nên trong `bot/ai.py` mình để một danh sách thử lần lượt: model trong `.env` trước, không được thì `gemini-2.0-flash`, rồi `gemini-1.5-flash`. Hết cả ba thì bot trả lời câu xin lỗi và mời khách dùng lệnh có sẵn.

**File `.env` đã được gitignore**, đừng commit lên nhé.

## License

MIT. Đồ án học tập, không dùng cho mục đích thương mại.
