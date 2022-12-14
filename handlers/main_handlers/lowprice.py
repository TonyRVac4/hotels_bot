import re
import datetime
from telebot.types import Message
from telebot.types import CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from loader import bot
from keyboards.inline import lowprice, lowprice_calldata
from states.contact_info import UserInfoState
from requests_to_api.searchers import find_cites
from handlers.final_handler import final_data_handler


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message):
    chat_id = message.chat.id

    bot.send_message(text="Введите на русском Город, где хотите найти отель:",
                     chat_id=chat_id)
    bot.register_next_step_handler(message, get_city)


@bot.message_handler(commands=['871306398239'])
def get_city(message: Message):
    chat_id = message.chat.id
    text = message.text

    cities = find_cites(city=text)
    if cities:
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.city, chat_id=chat_id)
        bot.send_message(text=f"Уточните, пожалуйста: {text}",
                         chat_id=chat_id,
                         reply_markup=lowprice.city_markup(cities))
    else:
        bot.send_message(text="Город не найден!\nВведите на русском Город, где хотите найти отель:",
                         chat_id=chat_id)
        bot.register_next_step_handler(message, get_city)


@bot.callback_query_handler(func=lambda call: call.data in lowprice_calldata.city_callback_data)
def clarification_city(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        pattern = r"([а-яА-Яa-zA-Z].+[а-яА-Яa-zA-Z])(\d{1,10})"
        call_data = re.search(pattern, call.data)
        data["city"] = call_data.group(1)
        data["dest_id"] = call_data.group(2)

        bot.set_state(user_id=user_id, state=UserInfoState.checkIn, chat_id=chat_id)

    bot.edit_message_text(text=f"Район: {call_data.group(1)}",
                          chat_id=chat_id,
                          message_id=call.message.id)

    cur_date = datetime.date.today() + datetime.timedelta(days=1)
    calendar, step = DetailedTelegramCalendar(calendar_id=1, min_date=cur_date).build()
    bot.send_message(text=f"📅️↙️Выберите дату въезда: {LSTEP[step]}",
                     chat_id=chat_id,
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def first_calendar_date(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    cur_date = datetime.date.today() + datetime.timedelta(days=1)
    result, key, step = DetailedTelegramCalendar(calendar_id=1, locale='ru', min_date=cur_date).process(call.data)
    if not result and key:
        bot.edit_message_text(text=f"📅️↙️Выберите дату въезда: {LSTEP[step]}",
                              chat_id=chat_id,
                              message_id=call.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
            data["checkIn"] = result
            bot.set_state(user_id=user_id, state=UserInfoState.checkOut, chat_id=chat_id)

            bot.edit_message_text(text=f"📅️↙️Дата въезда: {result}",
                                  chat_id=chat_id,
                                  message_id=call.message.message_id)
            year, mouth, day = map(int, str(result).split("-"))
            date = datetime.date(year, mouth, day) + datetime.timedelta(days=1)
            calendar, step = DetailedTelegramCalendar(calendar_id=2, min_date=date).build()
            bot.send_message(text=f"📅️↗️Выберите дату выезда: {LSTEP[step]}",
                             chat_id=chat_id,
                             reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def second_calendar_date(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        year, mouth, day = map(int, str(data["checkIn"]).split("-"))
        date = datetime.date(year, mouth, day) + datetime.timedelta(days=1)
        result, key, step = DetailedTelegramCalendar(calendar_id=2, locale='ru', min_date=date).process(call.data)
    if not result and key:
        bot.edit_message_text(text=f"📅️↗️Выберите дату выезда: {LSTEP[step]}",
                              chat_id=chat_id,
                              message_id=call.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
            data["checkOut"] = result
            bot.set_state(user_id=user_id, state=UserInfoState.quan_hotels, chat_id=chat_id)

        bot.edit_message_text(text=f"📅️↗️Дата выезда: {result}",
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
        if len(call.data) == 3:
            data["quan_hotels"] = int(call.data[1] + call.data[2])
        else:
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

    if text == "yes1":
        with bot.retrieve_data(call.from_user.id, chat_id) as data:
            data["need_photo"] = True
            bot.set_state(call.from_user.id, UserInfoState.quan_photo, chat_id)

        bot.edit_message_text(text="Сколько фото нужно?",
                              chat_id=chat_id,
                              message_id=call.message.message_id,
                              reply_markup=lowprice.quan_photos_keyboard())
    elif text == "no1":
        with bot.retrieve_data(call.from_user.id, chat_id) as data:
            data["need_photo"] = False
            data["quan_photo"] = 0
        final_data_handler(call, sorting="PRICE", command="lowprice")


@bot.callback_query_handler(func=lambda call: call.data in lowprice_calldata.quan_photos_callback_data())
def quan_photos(call: CallbackQuery):
    chat_id = call.message.chat.id

    with bot.retrieve_data(call.from_user.id, chat_id) as data:
        if len(call.data) == 3:
            data["quan_photo"] = int(call.data[1] + call.data[2])
        else:
            data["quan_photo"] = int(call.data[1])
    final_data_handler(call, sorting="PRICE", command="lowprice")
