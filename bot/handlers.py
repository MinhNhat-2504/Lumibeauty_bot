from telegram import Update
from telegram.error import TelegramError
import json
import os
from pathlib import Path
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from bot.keyboards import skintype_keyboard, confirm_order_keyboard, category_keyboard, SKINTYPE_LABELS, SKINTYPE_VALUES
from bot.messages import (
    WELCOME_MSG, SKINTYPE_MSG, NO_SKINTYPE_MSG, NO_PRODUCTS_MSG,
    format_product, format_order
)
from database import users, products, orders
from bot.ai import get_ai_response

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_IMAGES_DIR = _PROJECT_ROOT / "images"
_IMG_FOLDER_MAP_PATH = _PROJECT_ROOT / "data" / "img_folder_map.json"
_img_folder_map: dict[str, str] | None = None


def _get_img_folder_map() -> dict[str, str]:
    global _img_folder_map
    if _img_folder_map is None:
        if _IMG_FOLDER_MAP_PATH.is_file():
            _img_folder_map = json.loads(_IMG_FOLDER_MAP_PATH.read_text(encoding="utf-8"))
        else:
            _img_folder_map = {}
    return _img_folder_map


def _img_folder_file_for(product_name: str) -> Path | None:
    rel = _get_img_folder_map().get(product_name)
    if not rel:
        return None
    path = _PROJECT_ROOT / rel.replace("/", os.sep)
    return path if path.is_file() else None

# States cho ConversationHandler đặt hàng
CHOOSE_PRODUCT, ENTER_QUANTITY, ENTER_NAME, ENTER_ADDRESS, CONFIRM_ORDER = range(5)


# ──────────────────────────────────────────
# /start
# ──────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users.save_user(user.id, user.username)
    await update.message.reply_text(WELCOME_MSG, parse_mode="Markdown")


# ──────────────────────────────────────────
# /skintype
# ──────────────────────────────────────────
async def skintype(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        SKINTYPE_MSG,
        reply_markup=skintype_keyboard(),
        parse_mode="Markdown"
    )

async def skintype_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    skin_key = query.data  # e.g. "skin_oily"
    skin_value = SKINTYPE_VALUES[skin_key]
    label = SKINTYPE_LABELS[skin_key]

    users.update_skintype(query.from_user.id, skin_value)
    await query.edit_message_text(
        f"✅ Đã lưu loại da của bạn: *{label}*\n\n"
        f"Dùng /recommend để xem gợi ý sản phẩm phù hợp nhé! 💄",
        parse_mode="Markdown"
    )


# ──────────────────────────────────────────
# /recommend
# ──────────────────────────────────────────
async def recommend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    skin = users.get_skintype(user_id)

    if not skin:
        await update.message.reply_text(NO_SKINTYPE_MSG)
        return

    prods = products.get_products_by_skintype(skin)
    if not prods:
        await update.message.reply_text(NO_PRODUCTS_MSG)
        return

    msg = f"💄 *Sản phẩm phù hợp với {skin} của bạn:*\n\n"
    for i, p in enumerate(prods[:8], 1):
        msg += format_product(p, i) + "\n"
    await update.message.reply_text(msg, parse_mode="Markdown")


# ──────────────────────────────────────────
# /products
# ──────────────────────────────────────────
async def product_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🗂️ *Chọn danh mục sản phẩm bạn muốn xem:*",
        reply_markup=category_keyboard(),
        parse_mode="Markdown"
    )

async def category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    cat = query.data
    prods = products.get_all_products()
    filtered_prods = []
    
    titles = {
        "cat_cleanser": "Làm sạch & Tẩy trang",
        "cat_toner": "Toner & Xịt khoáng",
        "cat_serum": "Serum & Tinh chất",
        "cat_cream": "Kem dưỡng & Mắt",
        "cat_sunscreen": "Kem chống nắng",
        "cat_mask": "Mặt nạ & Khác",
        "cat_all": "Tất cả sản phẩm"
    }
    title = titles.get(cat, "")

    if cat == "cat_all":
        filtered_prods = prods
    else:
        for p in prods:
            name_lower = p['name'].lower()
            if cat == "cat_cleanser" and ("sữa rửa mặt" in name_lower or "tẩy trang" in name_lower or "cleanser" in name_lower):
                filtered_prods.append(p)
            elif cat == "cat_toner" and ("toner" in name_lower or "nước hoa hồng" in name_lower or "xịt khoáng" in name_lower):
                filtered_prods.append(p)
            elif cat == "cat_serum" and ("serum" in name_lower or "tinh chất" in name_lower or "dầu dưỡng" in name_lower):
                filtered_prods.append(p)
            elif cat == "cat_cream" and ("kem" in name_lower and "chống nắng" not in name_lower) or ("chấm mụn" in name_lower):
                filtered_prods.append(p)
            elif cat == "cat_sunscreen" and ("chống nắng" in name_lower or "sunscreen" in name_lower or "anessa" in name_lower):
                filtered_prods.append(p)
            elif cat == "cat_mask" and ("mặt nạ" in name_lower or "tế bào chết" in name_lower or "da chết" in name_lower or "aqua" in name_lower):
                filtered_prods.append(p)

    if not filtered_prods:
        await query.edit_message_text(f"😔 Hiện không có sản phẩm nào trong danh mục *{title}*.", parse_mode="Markdown")
        return

    import os
    img_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'img')
    for i, p in enumerate(filtered_prods, 1):
        formatted = format_product(p, i)
        img_file = None
        if p.get('image'):
            img_path = os.path.join(img_dir, p['image'])
            if os.path.exists(img_path):
                img_file = img_path
        if img_file:
            with open(img_file, "rb") as photo:
                await query.message.reply_photo(photo=photo, caption=formatted, parse_mode="Markdown")
        else:
            await query.message.reply_text(formatted, parse_mode="Markdown")
    # Gợi ý mẹo cuối cùng (có thể bỏ nếu không cần)
    # await query.message.reply_text("🖼️ *Mẹo:* Gõ lệnh `/xem <tên sản phẩm>` để xem hình ảnh!", parse_mode="Markdown")


# ──────────────────────────────────────────
# /search
# ──────────────────────────────────────────
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🔍 Vui lòng nhập từ khóa sau lệnh.\nVí dụ: `/search serum`",
            parse_mode="Markdown"
        )
        return

    keyword = " ".join(context.args)
    results = products.search_products(keyword)

    if not results:
        await update.message.reply_text(f"😔 Không tìm thấy sản phẩm nào với từ khóa *'{keyword}'*.", parse_mode="Markdown")
        return

    msg = f"🔍 *Kết quả tìm kiếm cho '{keyword}':*\n\n"
    for i, p in enumerate(results, 1):
        msg += format_product(p, i) + "\n"
    
    msg += "\n🖼️ *Mẹo:* Gõ lệnh `/xem <tên sản phẩm>` để xem hình ảnh!"
    await update.message.reply_text(msg, parse_mode="Markdown")

# ──────────────────────────────────────────
# /xem (Xem ảnh sản phẩm)
# ──────────────────────────────────────────

def get_product_image(product: dict) -> str:
    """Ưu tiên /img (map tên file rút gọn), rồi /images đúng tên sản phẩm, URL, stock."""
    product_name = product["name"]

    # Bỏ các kí tự đặc biệt trong tên sản phẩm để tránh lỗi khi đọc file
    safe_name = "".join(c for c in product_name if c not in r'\/:*?"<>|')

    # 1. Ảnh trong thư mục img/ (tên file tự đặt — map trong data/img_folder_map.json)
    img_mapped = _img_folder_file_for(product_name)
    if img_mapped is not None:
        return str(img_mapped)

    # 2. Ảnh trong images/ trùng tên sản phẩm (VD: Sữa rửa mặt CeraVe.jpg)
    for ext in (".jpg", ".png", ".jpeg"):
        file_path = _IMAGES_DIR / f"{safe_name}{ext}"
        if file_path.is_file():
            return str(file_path)

    # 3. Ảnh mặc định trong thư mục images/
    default_path = _IMAGES_DIR / "default.jpg"
    if default_path.is_file():
        return str(default_path)

    # 4. URL từ Cosmos / seed (placeholder hoặc link CDN của bạn)
    url = (product.get("image_url") or "").strip()
    if url:
        return url

    # 5. Link Unsplash theo từ khóa
    name_lower = product_name.lower()
    if "sữa rửa mặt" in name_lower or "cleanser" in name_lower or "tẩy trang" in name_lower:
        return "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=600&q=80"
    elif "toner" in name_lower or "nước hoa hồng" in name_lower or "xịt khoáng" in name_lower:
        return "https://images.unsplash.com/photo-1608248593842-8021c64fd54d?w=600&q=80"
    elif "serum" in name_lower or "tinh chất" in name_lower or "dầu dưỡng" in name_lower:
        return "https://images.unsplash.com/photo-1629198688000-71f23e745b6e?w=600&q=80"
    elif "chống nắng" in name_lower:
        return "https://images.unsplash.com/photo-1556228720-192a6af4e865?w=600&q=80"
    elif "mặt nạ" in name_lower or "tế bào chết" in name_lower or "da chết" in name_lower:
        return "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=600&q=80"
    elif "dưỡng mắt" in name_lower or "kem mắt" in name_lower:
        return "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=600&q=80"
    elif "nước tẩy trang" in name_lower or "dầu tẩy trang" in name_lower or "micellar" in name_lower:
        return "https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=600&q=80"
    elif "chấm mụn" in name_lower:
        return "https://images.unsplash.com/photo-1616394584738-fc6e612e71b9?w=600&q=80"
    else:  # Kem dưỡng & còn lại
        return "https://images.unsplash.com/photo-1611004128038-1616f73dbbe9?w=600&q=80"


async def _reply_product_photo_for_product(update: Update, p: dict) -> None:
    """Gửi ảnh + caption cho một document sản phẩm (không parse_mode — tránh lỗi entity Telegram)."""
    img_src = get_product_image(p)
    sk = ", ".join(p.get("skintype", []))
    caption = (
        f"📸 Ảnh minh họa sản phẩm\n"
        f"{p['name']}\n"
        f"💰 Giá: {p['price']:,} VNĐ\n"
        f"🧴 Loại da: {sk}\n"
        f"📝 {p.get('description', '')}\n\n"
        f"👉 Dùng lệnh /order để chốt đơn nhé!"
    )
    if len(caption) > 1024:
        caption = caption[:1021] + "..."

    try:
        if img_src.startswith("http"):
            await update.message.reply_photo(photo=img_src, caption=caption)
        else:
            with open(img_src, "rb") as photo:
                await update.message.reply_photo(photo=photo, caption=caption)
    except TelegramError:
        if img_src.startswith("http"):
            await update.message.reply_text(
                "Không gửi được ảnh (Telegram không tải được link). "
                f"Bạn mở thử trình duyệt:\n{img_src}\n\n{caption}"
            )
        else:
            await update.message.reply_text(
                f"Không đọc được file ảnh: {img_src}\n\n{caption}"
            )
    except OSError:
        await update.message.reply_text(
            f"Không mở được file ảnh: {img_src}\n\n{caption}"
        )


async def reply_product_photo_by_keyword(update: Update, keyword: str) -> bool:
    """Tìm SP theo từ khóa, gửi ảnh. Trả False nếu không có kết quả."""
    results = products.search_products(keyword.strip())
    if not results:
        return False
    await _reply_product_photo_for_product(update, results[0])
    return True


async def view_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "🖼️ Vui lòng nhập tên sản phẩm cần xem ảnh.\nVí dụ: `/xem CeraVe`",
            parse_mode="Markdown"
        )
        return

    keyword = " ".join(context.args)

    results = products.search_products(keyword)

    if not results:
        await update.message.reply_text(f"😔 Không tìm thấy sản phẩm nào với từ khóa *'{keyword}'*.", parse_mode="Markdown")
        return

    # Lấy kết quả đầu tiên tốt nhất để show ảnh bự
    p = results[0]
    
    # Ưu tiên lấy ảnh từ thuộc tính 'image' trỏ vào thư mục img/ của team
    img_filename = p.get('image')
    img_src = None
    if img_filename:
        # Construct the path relative to the current file's directory
        current_dir = os.path.dirname(__file__)
        # Assuming 'img' directory is at the same level as 'bot' directory
        # So, go up one level from 'handlers.py' (which is in 'bot') to the project root, then into 'img'
        project_root = os.path.dirname(current_dir)
        possible_path = os.path.join(project_root, "img", img_filename)
        if os.path.exists(possible_path):
            img_src = possible_path

    # Nếu không có hoặc file bị thiếu, fallback về bộ máy mockups cũ
    if not img_src:
        img_src = get_mock_image(p['name'])
    
    caption = (
        f"📸 *Ảnh minh họa sản phẩm:*\n"
        f"*{p['name']}*\n"
        f"💰 Giá: {p['price']:,} VNĐ\n"
        f"🧴 Loại da: {', '.join(p.get('skintype', []))}\n"
        f"📝 {p.get('description', '')}\n\n"
        f"👉 _Dùng lệnh /order để chốt đơn ngay nhé!_"
    )
    
    await update.message.reply_photo(photo=img_url, caption=caption, parse_mode="Markdown")



# ──────────────────────────────────────────
# /order – ConversationHandler
# ──────────────────────────────────────────
async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛒 *Đặt hàng*\n\nVui lòng nhập *tên sản phẩm* bạn muốn đặt:\n"
        "(Dùng /products để xem danh sách sản phẩm)",
        parse_mode="Markdown"
    )
    return CHOOSE_PRODUCT

async def order_get_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    # Đang trong /order mà tin nhắn /xem … lọt vào đây (vd. bản cũ chưa group=-1): gửi ảnh, giữ bước chọn SP
    if text.lower().startswith("/xem"):
        kw = text[4:].strip()
        if not kw:
            await update.message.reply_text(
                "Gõ /xem <tên sản phẩm> để xem ảnh, hoặc chỉ gõ tên sản phẩm để đặt. /cancel để hủy."
            )
            return CHOOSE_PRODUCT
        if not await reply_product_photo_by_keyword(update, kw):
            await update.message.reply_text(f"Không tìm thấy sản phẩm với '{kw}'.")
        else:
            await update.message.reply_text(
                "Bạn vẫn đang đặt hàng — nhập tên sản phẩm (như trong danh sách) để tiếp tục, hoặc /cancel."
            )
        return CHOOSE_PRODUCT

    if text.startswith("/"):
        await update.message.reply_text(
            "Đang đặt hàng — chỉ nhập tên sản phẩm (không gõ lệnh khác), hoặc /cancel."
        )
        return CHOOSE_PRODUCT

    product_name = text
    if not product_name:
        await update.message.reply_text("Vui lòng nhập tên sản phẩm hoặc /cancel.")
        return CHOOSE_PRODUCT

    product = products.get_product_by_name(product_name)
    if not product:
        found = products.search_products(product_name)
        if found:
            product = found[0]
        else:
            await update.message.reply_text(
                "❌ Không tìm thấy sản phẩm này. Vui lòng nhập lại hoặc /cancel để hủy."
            )
            return CHOOSE_PRODUCT

    context.user_data["order_product"] = product
    await update.message.reply_text(
        f"✅ Sản phẩm: *{product['name']}* – {product['price']:,} VNĐ\n\n"
        f"Nhập *số lượng* bạn muốn đặt:",
        parse_mode="Markdown"
    )
    return ENTER_QUANTITY

async def order_get_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        qty = int(update.message.text.strip())
        if qty <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text("❌ Số lượng không hợp lệ. Vui lòng nhập số nguyên dương.")
        return ENTER_QUANTITY

    context.user_data["order_quantity"] = qty
    await update.message.reply_text("👤 Nhập *họ tên người nhận hàng* của bạn:", parse_mode="Markdown")
    return ENTER_NAME

async def order_get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    context.user_data["order_name"] = name
    await update.message.reply_text("📍 Nhập *địa chỉ giao hàng* của bạn:", parse_mode="Markdown")
    return ENTER_ADDRESS

async def order_get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    address = update.message.text.strip()
    context.user_data["order_address"] = address

    product = context.user_data["order_product"]
    qty = context.user_data["order_quantity"]
    name = context.user_data["order_name"]
    total = product["price"] * qty

    summary = (
        f"📋 *Xác nhận đơn hàng:*\n\n"
        f"👤 Người nhận: *{name}*\n"
        f"🧴 Sản phẩm: *{product['name']}*\n"
        f"📦 Số lượng: {qty}\n"
        f"📍 Địa chỉ: {address}\n"
        f"💰 Tổng tiền: *{total:,} VNĐ*\n"
    )
    await update.message.reply_text(
        summary,
        reply_markup=confirm_order_keyboard(),
        parse_mode="Markdown"
    )
    return CONFIRM_ORDER

async def order_confirm_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "order_cancel":
        await query.edit_message_text("❌ Đã hủy đơn hàng.")
        context.user_data.clear()
        return ConversationHandler.END

    # Lưu đơn hàng
    product = context.user_data["order_product"]
    qty = context.user_data["order_quantity"]
    name = context.user_data["order_name"]
    address = context.user_data["order_address"]
    user_id = query.from_user.id

    order_id = orders.create_order(user_id, product["name"], qty, name, address)
    await query.edit_message_text(
        f"✅ *Đặt hàng thành công!*\n\n"
        f"Mã đơn hàng: `{order_id[:8]}...`\n"
        f"Cảm ơn bạn đã mua hàng tại Lumi Beauty! 🌸",
        parse_mode="Markdown"
    )
    context.user_data.clear()
    return ConversationHandler.END

async def order_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Đã hủy đặt hàng.")
    context.user_data.clear()
    return ConversationHandler.END


# ──────────────────────────────────────────
# /myorder
# ──────────────────────────────────────────
async def my_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    order_list = orders.get_orders_by_user(user_id)

    if not order_list:
        await update.message.reply_text("📦 Bạn chưa có đơn hàng nào.")
        return

    msg = "📦 *Đơn hàng của bạn:*\n\n"
    for i, o in enumerate(order_list, 1):
        msg += format_order(o, i) + "\n"
    await update.message.reply_text(msg, parse_mode="Markdown")


# ──────────────────────────────────────────
# /ask
# ──────────────────────────────────────────
async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "✨ Vui lòng nhập câu hỏi sau lệnh.\nVí dụ: `/ask Da tôi dạo này nổi mụn, nên dùng gì?`",
            parse_mode="Markdown"
        )
        return

    query = " ".join(context.args)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    response = get_ai_response(query)
    # Vì Markdown Của Telegram hỗ trợ bị giới hạn, ta sẽ không cần parse quá phức tạp, hoặc chỉ đơn thuần gửi plain HTML/Markdown mặc định.
    # Sử dụng None để tránh bị lỗi parse MarkdownV2 nếu AI trả về định dạng lạ. 
    await update.message.reply_text(response)

# ──────────────────────────────────────────
# Giao tiếp tự nhiên bằng AI (Không cần lệnh)
# ──────────────────────────────────────────
async def normal_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    # Chỉ xử lý nếu không phải là câu lệnh (không bắt đầu bằng '/')
    if not query.startswith('/'):
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        response = get_ai_response(query)
        await update.message.reply_text(response)

# ──────────────────────────────────────────
# Build ConversationHandler for /order
# ──────────────────────────────────────────
def get_order_conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("order", order_start)],
        states={
            CHOOSE_PRODUCT: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_get_product)],
            ENTER_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_get_quantity)],
            ENTER_NAME:     [MessageHandler(filters.TEXT & ~filters.COMMAND, order_get_name)],
            ENTER_ADDRESS:  [MessageHandler(filters.TEXT & ~filters.COMMAND, order_get_address)],
            CONFIRM_ORDER:  [CallbackQueryHandler(order_confirm_callback, pattern="^order_")],
        },
        fallbacks=[CommandHandler("cancel", order_cancel)],
    )
