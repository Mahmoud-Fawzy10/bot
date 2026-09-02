import os
import requests
import telebot
from flask import Flask, request

BOT_TOKEN = os.environ.get('BOT_TOKEN')
EASYORDERS_API_KEY = os.environ.get('EASYORDERS_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك في MF Foods! كيف يمكنني مساعدتك اليوم؟")

@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # يتم استبدال URL_PROJECT برابط الدالة الخاص بك من Firebase لاحقاً
    bot.set_webhook(url='HTTPS_PROJECT_URL/' + BOT_TOKEN)
    return "Webhook set successfully!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
