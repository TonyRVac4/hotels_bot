from telebot.types import Message, CallbackQuery
from loader import bot
from database.models import db, Hotels
from keyboards.inline.del_history import del_history, del_history_call_data


@bot.message_handler(commands=['history'])
def history(message: Message):
    chat_id = message.chat.id

    bot.send_message(chat_id, text="Выберите действие?", reply_markup=del_history())


@bot.callback_query_handler(func=lambda call: call.data in del_history_call_data)
def check_command(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    text = call.data

    counter = 0
    if text == "output":

        with db:
            for hotel in Hotels.select().where(Hotels.user_id == user_id):
                counter += 1
                if counter == 1:
                    bot.edit_message_text(text=hotel.hotel_info,
                                          chat_id=chat_id,
                                          disable_web_page_preview=True,
                                          message_id=call.message.id)
                bot.send_message(text=hotel.hotel_info,
                                 chat_id=chat_id,
                                 disable_web_page_preview=True,
                                 reply_markup=None)
    elif text == "del":
        with db:
            for hotel in Hotels.select().where(Hotels.user_id == user_id or Hotels.user_id == 0):
                counter += 1
                hotel.delete_instance()
            bot.edit_message_text(text="История очищена",
                                  chat_id=chat_id,
                                  message_id=call.message.id)

    if counter == 0:
        bot.edit_message_text(text="История пуста",
                              chat_id=chat_id,
                              message_id=call.message.id)
