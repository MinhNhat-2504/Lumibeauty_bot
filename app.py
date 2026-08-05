import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from bot.handlers import (
    start, skintype, skintype_callback,
    recommend, product_list, search,
    my_orders, get_order_conversation_handler,
    ask_ai, normal_chat, category_callback, view_image
)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Lệnh ở group=-1 để luôn chạy trước ConversationHandler (vd: đang /order vẫn dùng được /xem)
    app.add_handler(CommandHandler("start", start), group=-1)
    app.add_handler(CommandHandler("skintype", skintype), group=-1)
    app.add_handler(CommandHandler("recommend", recommend), group=-1)
    app.add_handler(CommandHandler("products", product_list), group=-1)
    app.add_handler(CommandHandler("search", search), group=-1)
    app.add_handler(CommandHandler("xem", view_image), group=-1)
    app.add_handler(CommandHandler("myorder", my_orders), group=-1)
    app.add_handler(CommandHandler("ask", ask_ai), group=-1)

    # ConversationHandler cho /order
    app.add_handler(get_order_conversation_handler())

    # Handler cho chat tự nhiên bằng AI
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, normal_chat))

    # Callback xử lý nút chọn danh mục sản phẩm
    app.add_handler(CallbackQueryHandler(category_callback, pattern="^cat_"))

    # Callback xử lý nút chọn loại da
    app.add_handler(CallbackQueryHandler(skintype_callback, pattern="^skin_"))

    ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

    if ENVIRONMENT == "production":
        # Chạy Webhook trên Cloud (Render, Google Cloud Run)
        PORT = int(os.environ.get('PORT', '8443'))
        WEBHOOK_URL = os.environ.get('WEBHOOK_URL') # Ví dụ: https://my-bot.onrender.com
        
        print(f"[Lumi Beauty Bot] is running in Webhook mode on port {PORT}...")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=f"{WEBHOOK_URL}"
        )
    else:
        # Chạy Long Polling khi DEV ở Local
        print("[Lumi Beauty Bot] is running in Polling mode (Local)...")
        app.run_polling()

if __name__ == "__main__":
    main()