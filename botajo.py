from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from flask import Flask
from threading import Thread
import os

# === KEEP ALIVE SETUP ===
app = Flask('')

@app.route('/')
def home():
    return "Bot juragan aktif!", 200

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# === BOT SETUP ===
TOKEN = os.environ.get("TOKEN")  # Gunakan dari ENV, aman untuk hosting

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
    "REKENING CUMAN DANA JURAGAN.\n\n"
    "Jika sudah, bot akan *otomatis mengundang kamu kedalam groupnya!* 🧙‍♂️ Admin : @Jancuk168\n\n"
    "_Untuk kembali ke menu utama, cukup ketik /start ya juragan_ 🔄"
)

waiting_message = (
    "📸 Oke, bukti transfer sudah diterima ya juragan!\n"
    "Tunggu *1-3 menit* yaa, LINK INVIET akan dikirim langsung ke juragan ✉️\n\n"
    "Kalau belum muncul juga, boleh kontak admin: @Jancuk168 ☎️"
)

user_transfer_state = set()

def start(update, context):
    update.message.reply_text(main_message, reply_markup=main_keyboard, parse_mode="Markdown")

def handle_message(update, context):
    user_id = update.message.from_user.id
    if user_id in user_transfer_state:
        if update.message.photo:
            update.message.reply_text(waiting_message, parse_mode="Markdown")
        else:
            update.message.reply_text(transfer_message, parse_mode="Markdown")
    else:
        update.message.reply_text(main_message, reply_markup=main_keyboard, parse_mode="Markdown")

def button_handler(update, context):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id

    vip_options = {
        "vip_indo": "🔥 *VIP INDO (50k)*\n\nVIP indo khusus INDONESIA Kalau mau payment Pilih lanjut...",
        "vip_jilbab": "🧕 *VIP JILBAB (50k)*\n\nSudah dipastikan durasinya panjang Kalau mau payment Pilih lanjut...",
        "vip_eropa": "👸 *VIP EROPA (50k)*\n\nCocok yang suka cari drama Kalau mau payment Pilih lanjut...",
        "vip_japan": "🎌 *VIP JAPAN (50k)*\n\nDurasi panjang minimal 10 menit Kalau mau payment Pilih lanjut...",
        "vip_all": "💎 *ALL VIP (100k)*\n\nSemua paket langsung dikasih juragan Kalau mau payment Pilih lanjut!",
    }

    vip_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Kembali", callback_data="back")],
        [InlineKeyboardButton("✅ Lanjutkan", callback_data="lanjut_transfer")]
    ])

    if query.data == "back":
        user_transfer_state.discard(user_id)
        query.edit_message_text(main_message, reply_markup=main_keyboard, parse_mode="Markdown")
    elif query.data in vip_options:
        query.edit_message_text(vip_options[query.data], reply_markup=vip_keyboard, parse_mode="Markdown")
    elif query.data == "lanjut_transfer":
        user_transfer_state.add(user_id)
        query.edit_message_text(transfer_message, parse_mode="Markdown")

# === JALANKAN BOT ===
keep_alive()
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.all, handle_message))
dp.add_handler(CallbackQueryHandler(button_handler))
print("🤖 Bot juragan aktif dan berjalan...")
updater.start_polling()
updater.idle()
