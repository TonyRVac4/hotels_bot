from telebot.types import Message

from loader import bot


@bot.message_handler(content_types=['text'])
def hello(message: Message):
    if message.text in ['привет', 'Привет']:
        bot.reply_to(message, f"Привет, {message.from_user.full_name}✋!")