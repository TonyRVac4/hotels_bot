from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['helloworld'])
def hello_world(message: Message):
    bot.reply_to(message, f"Миру мир и безопасность!")

