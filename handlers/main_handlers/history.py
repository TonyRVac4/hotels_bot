from telebot.types import Message
from loader import bot
from database.models import db, Hotels


@bot.message_handler(commands=['history'])
def history(message: Message):
    chat_id = message.chat.id
    with db:
        for hotel in Hotels.select().where(Hotels.user_id == message.from_user.id):
            bot.send_message(text=hotel.hotel_info, chat_id=chat_id)
