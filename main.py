import os
import telebot
import requests

BOT_TOKEN = os.environ.get("BOT_TOKEN")
EASYORDERS_API_KEY = os.environ.get("EASYORDERS_API_KEY", "2bd4726a-f80f-447d-9379-5e2083912e91")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك في رفيق | MF Foods 🤝\nكيف يمكنني مساعدتك اليوم؟\n/products - عرض المنتجات")

@bot.message_handler(commands=['products'])
def get_products(message):
    url = "https://api.easy-orders.net/api/v1/external-apps/products"
    headers = {"Api-Key": EASYORDERS_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            products = response.json()
            text = "🛒 **قائمة المنتجات والأسعار:**\n\n"
            for p in products:
                text += f"• **{p['name'].strip()}**: {p['price']} جنيه\n"
            bot.reply_to(message, text, parse_mode="Markdown")
        else:
            bot.reply_to(message, "عذراً، تعذر جلب البيانات حالياً.")
    except Exception as e:
        bot.reply_to(message, "حدث خطأ أثناء الاتصال بالخادم.")

bot.infinity_polling()
