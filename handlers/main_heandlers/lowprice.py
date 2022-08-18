from loader import bot
from telebot.types import Message
from keyboards.inline.lowprice import quan_hotels_keyboard, quan_photos_keyboard, is_need_photos_keyboard
from keyboards.inline.lowprice import quan_hotels_callback_data, quan_photos_callback_data, is_need_photos_callback_data
from telebot.types import CallbackQuery
from states.contact_info import UserInfoState


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message):
    id = message.chat.id

    bot.set_state(message.from_user.id, UserInfoState.city, id)
    bot.send_message(id, "Введите Город, где хотите найти отель:")
    bot.register_next_step_handler(message, get_city)


@bot.message_handler(content_types="text", state=UserInfoState.city)
def get_city(message: Message):
    id = message.chat.id

    if message.text.isalpha():
        with bot.retrieve_data(message.from_user.id, id) as data:
            data["city"] = message.text
            bot.set_state(message.from_user.id, UserInfoState.quan_hotels, id)

        bot.delete_message(chat_id=id, message_id=message.message_id)
        bot.delete_message(chat_id=id, message_id=message.message_id-1)
        bot.send_message(id, text="Введите кол-во отелей, которые необходимо вывести: ",
                         reply_markup=quan_hotels_keyboard())
        bot.register_next_step_handler(message, get_num_hotels)
    else:
        bot.send_message(id, "Название города должно быть только из букв\nВведите Город, где хотите найти отель:")


@bot.callback_query_handler(func=lambda call: call.data in quan_hotels_callback_data())
def get_num_hotels(call: CallbackQuery):
    id = call.message.chat.id

    with bot.retrieve_data(call.from_user.id, id) as data:
        data["quan_hotels"] = int(call.data[1])
        bot.set_state(call.from_user.id, UserInfoState.need_photo, id)

    bot.edit_message_text(chat_id=id, message_id=call.message.id,
                          text="Нужно-ли выводить фотографий для каждого отеля («Да/Нет»)")
    bot.edit_message_reply_markup(chat_id=id, message_id=call.message.id, reply_markup=is_need_photos_keyboard())


@bot.callback_query_handler(func=lambda call: call.data in is_need_photos_callback_data())
def need_photos(call: CallbackQuery):
    id = call.message.chat.id
    text = call.data

    if text == "yes":
        with bot.retrieve_data(call.from_user.id, id) as data:
            data["need_photos"] = True
            bot.set_state(call.from_user.id, UserInfoState.quan_photo, id)

        bot.edit_message_text(chat_id=id, message_id=call.message.id,
                              text="Сколько фото нужно?")
        bot.edit_message_reply_markup(chat_id=id, message_id=call.message.id,
                                      reply_markup=quan_photos_keyboard())
    elif text == "no":
        with bot.retrieve_data(call.from_user.id, id) as data:
            data["need_photos"] = False

        bot.edit_message_text(chat_id=id, message_id=call.message.id,
                              text="Вы завершили регистрацию")
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id,
                                      reply_markup=None)


@bot.callback_query_handler(func=lambda call: call.data in quan_photos_callback_data())
def quan_photos(call: CallbackQuery):
    id = call.message.chat.id

    with bot.retrieve_data(call.from_user.id, id) as data:
        data["quan_photo"] = int(call.data[1])
        print(data)

    bot.edit_message_text(chat_id=id, message_id=call.message.id,
                          text="Вы завершили регистрацию")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id,
                                  reply_markup=None)
