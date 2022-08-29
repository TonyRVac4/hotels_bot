from loader import bot
from telebot.types import Message
from keyboards.inline import lowprice
from keyboards.inline import lowprice_calldata
from telebot.types import CallbackQuery
from states.contact_info import UserInfoState
from requests_to_api.searchers import city_founding, hotel_founding
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from utils.misc.sorters import lowprice_sort
import re


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message):
    chat_id = message.chat.id

    bot.send_message(text="Введите Город, где хотите найти отель:",
                     chat_id=chat_id)
    bot.register_next_step_handler(message, get_city)


@bot.message_handler(content_types="text")
def get_city(message: Message):
    chat_id = message.chat.id
    text = message.text

    cities = city_founding(city=text)
    if cities:
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.city, chat_id=chat_id)
        bot.send_message(text=f"Уточните, пожалуйста: {text}",
                         chat_id=chat_id,
                         reply_markup=lowprice.city_markup(cities))
    else:
        bot.send_message(text="Город не найден!\nВведите Город, где хотите найти отель:",
                         chat_id=chat_id)


@bot.callback_query_handler(func=lambda call: call.data in lowprice_calldata.city_markup_callback_data)
def clarification_city(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        pattern = r"([а-яА-Яa-zA-Z].+[а-яА-Яa-zA-Z])(\d{6,8})"
        call_data = re.search(pattern, call.data)
        data["city"] = call_data.group(1)
        data["dest_id"] = call_data.group(2)
        bot.set_state(user_id=user_id, state=UserInfoState.checkIn, chat_id=chat_id)

    bot.edit_message_text(text=f"Город: {call_data.group(1)}",
                          chat_id=chat_id,
                          message_id=call.message.id)

    calendar, step = DetailedTelegramCalendar(calendar_id=1).build()
    bot.send_message(text=f"Выберите дату въезда: {LSTEP[step]}",
                     chat_id=chat_id,
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def first_calendar_date(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    result, key, step = DetailedTelegramCalendar(calendar_id=1, locale='ru').process(call.data)
    if not result and key:
        bot.edit_message_text(text=f"Выберите дату въезда: {LSTEP[step]}",
                              chat_id=chat_id,
                              message_id=call.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
            data["checkIn"] = result
            bot.set_state(user_id=user_id, state=UserInfoState.checkOut, chat_id=chat_id)

        bot.edit_message_text(text=f"Дата въезда: {result}",
                              chat_id=chat_id,
                              message_id=call.message.message_id)

        calendar, step = DetailedTelegramCalendar(calendar_id=2).build()
        bot.send_message(text=f"Выберите дату выезда: {LSTEP[step]}",
                         chat_id=chat_id,
                         reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def second_calendar_date(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    result, key, step = DetailedTelegramCalendar(calendar_id=2, locale='ru').process(call.data)
    if not result and key:
        bot.edit_message_text(text=f"Выберите дату выезда: {LSTEP[step]}",
                              chat_id=chat_id,
                              message_id=call.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
            data["checkOut"] = result
            bot.set_state(user_id=user_id, state=UserInfoState.quan_hotels, chat_id=chat_id)

        bot.edit_message_text(text=f"Дата выезда: {result}",
                              chat_id=chat_id,
                              message_id=call.message.message_id)
        bot.send_message(text=f"Введите кол-во отелей, которые необходимо вывести: ",
                         chat_id=chat_id,
                         reply_markup=lowprice.quan_hotels_keyboard())


@bot.callback_query_handler(func=lambda call: call.data in lowprice_calldata.quan_hotels_callback_data())
def get_num_hotels(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    with bot.retrieve_data(user_id, chat_id) as data:
        data["quan_hotels"] = int(call.data[1])
        bot.set_state(user_id, UserInfoState.need_photo, chat_id)

    bot.edit_message_text(text="Нужно-ли выводить фотографий для каждого отеля («Да/Нет»)",
                          chat_id=chat_id,
                          message_id=call.message.message_id,
                          reply_markup=lowprice.is_need_photos_keyboard())


@bot.callback_query_handler(func=lambda call: call.data in lowprice_calldata.is_need_photos_callback_data())
def need_photos(call: CallbackQuery):
    chat_id = call.message.chat.id
    text = call.data

    if text == "yes":
        with bot.retrieve_data(call.from_user.id, chat_id) as data:
            data["need_photos"] = True
            bot.set_state(call.from_user.id, UserInfoState.quan_photo, chat_id)

        bot.edit_message_text(text="Сколько фото нужно?",
                              chat_id=chat_id,
                              message_id=call.message.message_id,
                              reply_markup=lowprice.quan_photos_keyboard())
    elif text == "no":
        with bot.retrieve_data(call.from_user.id, chat_id) as data:
            data["need_photos"] = False
            data["quan_photo"] = 0
        bot.register_next_step_handler(call.message, find_hotels)


@bot.callback_query_handler(func=lambda call: call.data in lowprice_calldata.quan_photos_callback_data())
def quan_photos(call: CallbackQuery):
    chat_id = call.message.chat.id

    with bot.retrieve_data(call.from_user.id, chat_id) as data:
        data["quan_photo"] = int(call.data[1])
    # не переходит дальше


@bot.message_handler(content_types="text")
def find_hotels(message):
    print(124)
    chat_id = message.chat.id
    with bot.retrieve_data(message.from_user.id, chat_id) as data:
        bot.edit_message_text(text="Вы завершили регистрацию",
                              chat_id=chat_id,
                              message_id=message.message_id,
                              reply_markup=None)
        bot.send_message(text="Ожидайте, подбираем отели...", chat_id=chat_id)

        hotels = hotel_founding(id=data["dest_id"],
                                checkIn=data["checkIn"],
                                checkOut=data["checkOut"],
                                quan_hotels=data["quan_hotels"],
                                sorting=lowprice_sort)

    if hotels:
        bot.edit_message_text(text="Вот что удалось найти:",
                              chat_id=chat_id,
                              message_id=message.message_id,
                              reply_markup=None)
    else:
        bot.send_message(text="Отели не найдены",
                         chat_id=chat_id)