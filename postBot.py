
BOT_TOKEN = "6023329219:AAHD_zrHWUUosaWtBmoWBtNMfEc5ndu1DjQ"
CHANNEL_ID = "-1002174111727"  # Kanalingiz username yoki ID sini yozing

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Holatlar
ASK_PHOTO, ASK_INFO, ASK_PRICE = range(3)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Assalomu alaykum! Iltimos, mahsulot uchun rasm yuboring.")
    return ASK_PHOTO

# Rasm qabul qilish
async def ask_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.photo:
        context.user_data['photo'] = update.message.photo[-1].file_id
        await update.message.reply_text("Endi mahsulot haqida maʼlumot yuboring.")
        return ASK_INFO
    else:
        await update.message.reply_text("Iltimos, mahsulot uchun rasm yuboring.")
        return ASK_PHOTO

# Maʼlumot qabul qilish
async def ask_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['info'] = update.message.text
    await update.message.reply_text("Endi mahsulotning narxini yuboring.")
    return ASK_PRICE

# Narx qabul qilish va kanalda post qilish
async def ask_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['price'] = update.message.text

    # Kanalga post qilish
    photo = context.user_data['photo']
    info = context.user_data['info']
    price = context.user_data['price']

    # Tugmalar
    keyboard = [
        [InlineKeyboardButton("💵 Sotib Olish", url="https://t.me/MobileMarket_A_X_Bot")],
        [InlineKeyboardButton("📱 Kategoriyani ko'rish", url="https://t.me/MobileMarketGroup_A_X")],  # URLni o'zgartiring
        [InlineKeyboardButton("📝 Adminga yozish", url="https://t.me/Abdumomin1994")]  # URLni o'zgartiring
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Kanaldagi post
    await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=photo,
        caption=f"\n<b>{info}</b>\n\n\n<b>Narxi:</b> {price}",
        parse_mode="HTML",
        reply_markup=reply_markup,
    )

    # Foydalanuvchiga javob
    await update.message.reply_photo(
        photo=photo,
        caption=f"Kanalingizga quyidagicha joylandi:\n\n{info}\n\n<b>Narxi:</b> {price}\n\n yana qo'shish uchun /start ni bosing",
        parse_mode="HTML",
        reply_markup=reply_markup,
    )

    return ConversationHandler.END

# Bekor qilish
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Jarayon bekor qilindi.")
    return ConversationHandler.END

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_PHOTO: [MessageHandler(filters.PHOTO, ask_photo)],
            ASK_INFO: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_info)],
            ASK_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_price)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("Bot ishlayapti...")
    app.run_polling()
