from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def skintype_keyboard() -> InlineKeyboardMarkup:
    """Bàn phím chọn loại da"""
    keyboard = [
        [
            InlineKeyboardButton("🌟 Da dầu", callback_data="skin_oily"),
            InlineKeyboardButton("💧 Da khô", callback_data="skin_dry"),
        ],
        [
            InlineKeyboardButton("✨ Da hỗn hợp", callback_data="skin_combo"),
            InlineKeyboardButton("🌸 Da nhạy cảm", callback_data="skin_sensitive"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def confirm_order_keyboard() -> InlineKeyboardMarkup:
    """Bàn phím xác nhận / hủy đơn hàng"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Xác nhận đặt hàng", callback_data="order_confirm"),
            InlineKeyboardButton("❌ Hủy", callback_data="order_cancel"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def category_keyboard() -> InlineKeyboardMarkup:
    """Bàn phím chọn danh mục sản phẩm"""
    keyboard = [
        [
            InlineKeyboardButton("🧴 Làm sạch & Tẩy trang", callback_data="cat_cleanser"),
            InlineKeyboardButton("💧 Toner & Xịt khoáng", callback_data="cat_toner"),
        ],
        [
            InlineKeyboardButton("✨ Serum & Tinh chất", callback_data="cat_serum"),
            InlineKeyboardButton("🌸 Kem dưỡng & Mắt", callback_data="cat_cream"),
        ],
        [
            InlineKeyboardButton("☀️ Kem chống nắng", callback_data="cat_sunscreen"),
            InlineKeyboardButton("🎭 Mặt nạ & Khác", callback_data="cat_mask"),
        ],
        [
            InlineKeyboardButton("🛍️ Xem tất cả sản phẩm", callback_data="cat_all"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

SKINTYPE_LABELS = {
    "skin_oily": "Da dầu",
    "skin_dry": "Da khô",
    "skin_combo": "Da hỗn hợp",
    "skin_sensitive": "Da nhạy cảm",
}

SKINTYPE_VALUES = {
    "skin_oily": "da dầu",
    "skin_dry": "da khô",
    "skin_combo": "da hỗn hợp",
    "skin_sensitive": "da nhạy cảm",
}
