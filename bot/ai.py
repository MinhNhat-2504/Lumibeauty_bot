import os
import google.generativeai as genai
from database.products import get_all_products
from bot.messages import AI_ERROR_BUSY_MSG, AI_ERROR_NO_KEY_MSG
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = (os.getenv("GEMINI_MODEL") or "").strip()

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Thứ tự thử model: env trước, sau đó các bản flash thường gặp (Google đổi tên model theo thời gian).
_MODEL_FALLBACKS = [
    GEMINI_MODEL,
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]


def _product_list_for_prompt() -> str:
    try:
        products = get_all_products()
    except Exception as e:
        print(f"[AI] Không tải danh sách sản phẩm từ Cosmos: {e}")
        products = []
    if not products:
        return "(Chưa tải được danh sách từ CSDL — hãy tư vấn chung và gợi ý khách dùng /products, /search.)"
    return "\n".join(
        f"- {i + 1}. {p['name']} (Giá: {p['price']} VNĐ, Loại da: {', '.join(p.get('skintype', []))}): {p.get('description', '')}"
        for i, p in enumerate(products)
    )


def get_ai_response(user_query: str) -> str:
    if not GEMINI_API_KEY:
        return AI_ERROR_NO_KEY_MSG

    product_list_str = _product_list_for_prompt()

    system_prompt = f"""Bạn là Lumi, một chuyên gia tư vấn mỹ phẩm nhiệt tình và thân thiện của cửa hàng Lumi Beauty.
Bạn sẽ giúp khách hàng chọn sản phẩm phù hợp với tình trạng da của họ và hỗ trợ mua hàng bằng tiếng Việt.
Hãy trả lời ngắn gọn, lịch sự, có sử dụng emoji, cách dòng dễ đọc. KHÔNG trả lời quá dài (tối đa 250 chữ).

Đây là danh sách các sản phẩm ĐANG CÓ tại cửa hàng cùng Số thứ tự của chúng:
{product_list_str}

LƯU Ý QUAN TRỌNG DÀNH CHO BẠN:
1. Khi khách hàng hỏi tư vấn da: Hãy phân tích và đưa ra 1-2 gợi ý tốt nhất từ danh sách trên cùng lý do phù hợp.
2. NẾU KHÁCH TỎ Ý ĐỊNH MUA HÀNG (Ví dụ: "Tôi muốn mua số 6", "Lấy cho tôi cái này", "Đặt hàng", "Giá bao nhiêu"): BẮT BUỘC BẠN PHẢI HƯỚNG DẪN HỌ NHƯ SAU: "Tuyệt vời quá! Để đặt hàng, bạn hãy gõ lệnh /order và làm theo hướng dẫn của tớ nha! 🥰🛒"
3. KHÔNG BAO GIỜ tự mình chốt/xác nhận đơn hàng, luôn luôn bắt khách hàng gõ lệnh /order.
4. Nếu không chắc hoặc không có trong danh sách: khuyên dùng /products hoặc /search, giọng điệu nhẹ nhàng như tin nhắn CSKH.

Câu hỏi/Tin nhắn của khách hàng: {user_query}
"""

    seen: set[str] = set()
    last_err: Exception | None = None
    for name in _MODEL_FALLBACKS:
        if not name or name in seen:
            continue
        seen.add(name)
        try:
            model = genai.GenerativeModel(name)
            response = model.generate_content(system_prompt)
            try:
                out = (response.text or "").strip()
            except (ValueError, AttributeError):
                out = ""
            if not out:
                last_err = RuntimeError(f"Model {name} trả về nội dung rỗng (có thể bị chặn bởi safety).")
                print(f"[AI] {last_err}")
                continue
            return out
        except Exception as e:
            last_err = e
            print(f"[AI] Model '{name}' lỗi: {type(e).__name__}: {e}")

    if last_err:
        print(f"[AI] Đã thử hết model, lỗi cuối: {last_err}")
    return AI_ERROR_BUSY_MSG
