import os
import telebot
from telebot import types
# Получаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Ассалому алайкум! Я бот для тегов. Используй /all чтобы отметить всех участников чата.")
@bot.message_handler(commands=['all'])
def tag_all(message):
    if message.chat.type not in ['group', 'supergroup']:
        bot.reply_to(message, "❗ Команда работает только в группе.")
        return

    members = []
    try:
        chat_members = bot.get_chat_administrators(message.chat.id)
        for admin in chat_members:
            members.append(admin.user)
    except Exception:
        pass
    # Получаем список упоминаний
    tagged_users = ""
    try:
        chat_info = bot.get_chat(message.chat.id)
        title = chat_info.title
    except Exception:
        title = "группе"
    try:
        # Если бот имеет права, собираем список участников (до 200)
        chat_members = bot.get_chat_administrators(message.chat.id)
        for m in chat_members:
            tagged_users += f"@{m.user.username or m.user.first_name} "
    except Exception:
        tagged_users = "⚠️ Не удалось получить список пользователей."
    # Отправляем сообщение
    text = f"{message.from_user.first_name} тегнул всех участников {title}!\n\n{tagged_users}"
    bot.send_message(message.chat.id, text)
print("✅ Бот запущен...")
bot.polling(none_stop=True)