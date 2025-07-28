import os
from flask import Flask
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot juragan aktif!", 200

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

TOKEN = os.environ.get("TOKEN")

main_message = (
    "🎉 *Selamat datang juragan di BAHASENAK* 🎉\n\n"
    "Mau beli *VIP JURAGAN*? Langsung pilih paket VIP di bawah ini ya juragan 👇"
)

main_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("💎 VIP INDO (50k)", callback_data="vip_indo")],
    [InlineKeyboardButton("💎 VIP JILBAB (50k)", callback_data="vip_jilbab")],
    [InlineKeyboardButton("💎 VIP EROPA (50k)", callback_data="vip_eropa")],
    [InlineKeyboardButton("💎 VIP JAPAN (50k)", callback_data="vip_japan")],
    [InlineKeyboardButton("💎 ALL VIP (100k)", callback_data="vip_all")],
])

transfer_message = (
    "💳 *Oke juragan!*\n\n"
    "Silahkan transfer ke nomor ini ya juragan:\n"
    "DANA: 081311361110\n"
    "Atas Nama: JAXX TEGXX HARXX\n\n"
    "Jika sudah, bot akan *otomatis mengundang kamu kedalam groupnya!* 🧙‍♂️ Admin : @Jancuk168\n\n"
    "_Untuk kembali ke menu utama, cukup ketik /start ya juragan_ 🔄"
)

waiting_message = (
    "📸 Oke, bukti transfer sudah diterima ya juragan!\n"
    "Tunggu *1-3 menit* yaa, LINK INVIET akan dikirim langsung ke juragan ✉️\n\n"
    "Kalau belum muncul juga, boleh kontak admin: @Jancuk168 ☎️"
)

user_transfer_state = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(main_message, reply_markup=main_keyboard, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in user_transfer_state:
        if update.message.photo:
            await update.message.reply_text(waiting_message, parse_mode="Markdown")
        else:
            await update.message.reply_text(transfer_message, parse_mode="Markdown")
    else:
        await update.message.reply_text(main_message, reply_markup=main_keyboard, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    vip_options = {
        "vip_indo": "🔥 *VIP INDO (50k)*\n\nVIP indo khusus INDONESIA...",
        "vip_jilbab": "🧕 *VIP JILBAB (50k)*\n\nSudah dipastikan durasinya panjang...",
        "vip_eropa": "👸 *VIP EROPA (50k)*\n\nCocok yang suka cari drama...",
        "vip_japan": "🎌 *VIP JAPAN (50k)*\n\nDurasi panjang minimal 10 menit...",
        "vip_all": "💎 *ALL VIP (100k)*\n\nSemua paket langsung dikasih juragan...",
    }

    vip_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Kembali", callback_data="back")],
        [InlineKeyboardButton("✅ Lanjutkan", callback_data="lanjut_transfer")]
    ])

    if query.data == "back":
        user_transfer_state.discard(user_id)
        await query.edit_message_text(main_message, reply_markup=main_keyboard, parse_mode="Markdown")
    elif query.data in vip_options:
        await query.edit_message_text(vip_options[query.data], reply_markup=vip_keyboard, parse_mode="Markdown")
    elif query.data == "lanjut_transfer":
        user_transfer_state.add(user_id)
        await query.edit_message_text(transfer_message, parse_mode="Markdown")

# === JALANKAN BOT ===
keep_alive()

app_telegram = ApplicationBuilder().token(TOKEN).build()
app_telegram.add_handler(CommandHandler("start", start))
app_telegram.add_handler(MessageHandler(filters.ALL, handle_message))
app_telegram.add_handler(CallbackQueryHandler(button_handler))
app_telegram.run_polling()
