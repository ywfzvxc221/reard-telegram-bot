import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("BOT_TOKEN")  # توكن البوت من متغيرات البيئة
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # معرف الأدمن من متغيرات البيئة
CHANNEL_USERNAME = '@qqwweerrttqqyyyy'  # معرف القناة الجديد

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("📝 طلب تمويل إعلان", callback_data='order'),
        InlineKeyboardButton("💵 الأسعار", callback_data='prices'),
        InlineKeyboardButton("📊 إحصائيات القناة", callback_data='stats'),
        InlineKeyboardButton("📩 تواصل معنا", url="https://t.me/your_username")  # ← يمكنك تعديله لاحقًا
    )
    bot.send_message(
        message.chat.id,
        "مرحباً بك في بوت تمويل القنوات 💡\nاختر أحد الخيارات التالية:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "order":
        msg = bot.send_message(call.message.chat.id, "📝 اكتب تفاصيل إعلانك (رابط القناة + النص)...")
        bot.register_next_step_handler(msg, receive_ad)
    elif call.data == "prices":
        bot.send_message(call.message.chat.id, "💵 قائمة الأسعار:\n\n- تمويل 100 عضو: 5$\n- تمويل 200 عضو: 10$\n- تمويل 500 عضو: 20$")
    elif call.data == "stats":
        try:
            members = bot.get_chat_member_count(CHANNEL_USERNAME)
            bot.send_message(call.message.chat.id, f"📊 عدد أعضاء القناة: {members}")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"⚠️ لم أتمكن من جلب الإحصائيات: {e}")

def receive_ad(message):
    ad_info = f"📢 إعلان جديد من {message.from_user.first_name} (@{message.from_user.username}):\n\n"
    if message.text:
        ad_info += message.text
    elif message.caption:
        ad_info += message.caption

    bot.send_message(ADMIN_ID, ad_info)

    if message.content_type != 'text':
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

    bot.send_message(message.chat.id, "✅ تم استلام طلبك، سيتم التواصل معك قريبًا لإتمام العملية.")

print("🚀 البوت يعمل الآن...")
bot.infinity_polling()
