from telebot.types import Message
from loader import bot
from database.models import Users, db


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.full_name}!\n"
                                      f"Это бот для поиска отелей\n"
                                      f"Чтобы узнать функционал нажмите на /help\n\n"
                                      f"❗Внимание поиск по России временно не работает❗")

    with db:
        Users.create(name=message.from_user.first_name, user_id=message.from_user.id)
