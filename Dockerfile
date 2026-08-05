# ── Bước 1: Chọn base image ───────────────────────────────
# Dùng Python 3.10 bản slim (nhẹ ~120MB, không có thư viện thừa)
FROM python:3.10-slim

# ── Bước 2: Thiết lập thư mục làm việc trong container ────
# Mọi lệnh RUN/COPY sau đây đều chạy tương đối với /app
WORKDIR /app

# ── Bước 3: Cài dependencies TRƯỚC khi copy code ──────────
# Tách riêng bước này để Docker tận dụng cache layer:
# Nếu code thay đổi mà requirements.txt không đổi → không cài lại pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Bước 4: Copy toàn bộ source code vào container ────────
# File .env KHÔNG được copy (đã có trong .gitignore/.dockerignore)
# Secrets sẽ được inject qua biến môi trường khi chạy
COPY . .

# ── Bước 5: Khai báo port ─────────────────────────────────
# Cloud Run inject PORT=8080, Render inject PORT=10000, v.v.
# EXPOSE chỉ để tài liệu hóa, không thực sự mở port
EXPOSE 8080

# ── Bước 6: Lệnh khởi chạy ────────────────────────────────
# Mặc định: chạy bot (polling hoặc webhook tùy biến ENVIRONMENT)
# Để chạy Dashboard thay vì bot: override CMD khi docker run
#   docker run ... python dashboard.py
CMD ["python", "app.py"]
