from loader import bot
from telebot.types import Message
from keyboards.inline import lowprice
from keyboards.inline import lowprice_calldata
from telebot.types import CallbackQuery
from states.contact_info import UserInfoState
from utils.misc.searchers import city_founding
import re


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message):
    chat_id = message.chat.id

    bot.send_message(chat_id, "Введите Город, где хотите найти отель:")
    bot.register_next_step_handler(message, get_city)


@bot.message_handler(content_types="text")
def get_city(message: Message):
    chat_id = message.chat.id
    text = message.text

    cities = city_founding(city=text)
    if cities:
        # bot.delete_message(chat_id=id, message_id=message.message_id)
        # bot.delete_message(chat_id=id, message_id=message.message_id - 1)

        bot.set_state(message.from_user.id, UserInfoState.city, chat_id)
        bot.send_message(chat_id=chat_id, text=f"Уточните, пожалуйста: {text}",
                         reply_markup=lowprice.city_markup(cities=cities))
        bot.register_next_step_handler(message, clarification_city)
    else:
        bot.send_message(chat_id, "Город не найден!\n"
                                  "Введите Город, где хотите найти отель:")


@bot.callback_query_handler(func=lambda call: call.data in lowprice_calldata.city_markup_callback_data)
def clarification_city(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    with bot.retrieve_data(user_id, chat_id) as data:
        print(call.data)

        call_data = re.search(r"([a-zA-Z].+)(\d{7})", call.data)
        data["city"] = call_data.group(1)
        data["dest_id"] = int(call_data.group(2))
        print(data)
        bot.set_state(user_id, UserInfoState.quan_hotels, chat_id)

    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id,
                          text="Введите кол-во отелей, которые необходимо вывести: ")
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.id,
                                  reply_markup=lowprice.quan_hotels_keyboard())


@bot.callback_query_handler(func=lambda call: call.data in lowprice_calldata.quan_hotels_callback_data())
def get_num_hotels(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    with bot.retrieve_data(user_id, chat_id) as data:
        data["quan_hotels"] = int(call.data[1])
        bot.set_state(user_id, UserInfoState.need_photo, chat_id)

    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id,
                          text="Нужно-ли выводить фотографий для каждого отеля («Да/Нет»)")
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.id,
                                  reply_markup=lowprice.is_need_photos_keyboard())


@bot.callback_query_handler(func=lambda call: call.data in lowprice_calldata.is_need_photos_callback_data())
def need_photos(call: CallbackQuery):
    chat_id = call.message.chat.id
    text = call.data

    if text == "yes":
        with bot.retrieve_data(call.from_user.id, chat_id) as data:
            data["need_photos"] = True
            bot.set_state(call.from_user.id, UserInfoState.quan_photo, chat_id)

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.id,
                              text="Сколько фото нужно?")
        bot.edit_message_reply_markup(chat_id=chat_id, message_id=call.message.id,
                                      reply_markup=lowprice.quan_photos_keyboard())
    elif text == "no":
        with bot.retrieve_data(call.from_user.id, chat_id) as data:
            data["need_photos"] = False
            data["quan_photo"] = 0

        bot.edit_message_text(chat_id=chat_id, message_id=call.message.id,
                              text="Вы завершили регистрацию")
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id,
                                      reply_markup=None)


@bot.callback_query_handler(func=lambda call: call.data in lowprice_calldata.quan_photos_callback_data())
def quan_photos(call: CallbackQuery):
    chat_id = call.message.chat.id

    with bot.retrieve_data(call.from_user.id, chat_id) as data:
        data["quan_photo"] = int(call.data[1])

    bot.edit_message_text(chat_id=chat_id, message_id=call.message.id,
                          text="Вы завершили регистрацию")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id,
                                  reply_markup=None)
