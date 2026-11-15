import os
import telebot
import requests
from flask import Flask
from threading import Thread

TOKEN = os.environ.get('TELEGRAM_TOKEN')
OPENROUTER_KEY = os.environ.get('OPENROUTER_KEY')
   
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "xiaomi/mimo-v2.5",
        "messages": [{"role": "user", "content": message.text}]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        answer = response.json()['choices'][0]['message']['content']
        bot.reply_to(message, answer)
    except Exception:
        bot.reply_to(message, "Ошибка при запросе к ИИ. Попробуйте позже.")

if __name__ == "__main__":
    Thread(target=run_web).start()
    bot.infinity_polling()
