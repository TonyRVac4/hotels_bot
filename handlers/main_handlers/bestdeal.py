import re
import datetime
from telebot.types import Message
from telebot.types import CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from loader import bot
from keyboards.inline import bestdeal, bestdeal_calldata
from states.contact_info import UserInfoState
from requests_to_api.searchers import find_cites
from handlers.final_handler import final_data_handler


@bot.message_handler(commands=['bestdeal'])
def best_deal(message: Message):
    print("bestdeal")
    chat_id = message.chat.id

    bot.send_message(text="Введите на русском Город, где хотите найти отель:",
                     chat_id=chat_id)
    bot.register_next_step_handler(message, bestdeal_get_city)


@bot.message_handler(commands=['8675396858'])
def bestdeal_get_city(message: Message):
    chat_id = message.chat.id
    text = message.text

    cities = find_cites(city=text)
    if cities:
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.city, chat_id=chat_id)
        bot.send_message(text=f"Уточните, пожалуйста: {text}",
                         chat_id=chat_id,
                         reply_markup=bestdeal.city_markup(cities))
    else:
        bot.send_message(text="Город не найден!\nВведите на русском Город, где хотите найти отель:",
                         chat_id=chat_id)
        bot.register_next_step_handler(message, bestdeal_get_city)


@bot.callback_query_handler(func=lambda call: call.data in bestdeal_calldata.city_callback_data)
def bestdeal_clarification_city(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        pattern = r"([а-яА-Яa-zA-Z].+[а-яА-Яa-zA-Z])(\d{1,10})"
        call_data = re.search(pattern, call.data)
        data["city"] = call_data.group(1)
        data["dest_id"] = call_data.group(2)
        bot.set_state(user_id=user_id, state=UserInfoState.price_range, chat_id=chat_id)

    bot.edit_message_text(text=f"Район: {call_data.group(1)}",
                          chat_id=chat_id,
                          message_id=call.message.message_id)
    bot.send_message(chat_id, text="Уточни диапазон цен(RUB):\n(Пример: 5000-15000, 5000 15000)")
    bot.register_next_step_handler(call.message, price_range)


@bot.message_handler(content_types=['text'])
def price_range(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        pattern = r"(\d{1,8})[- ](\d{1,8})"
        call_data = re.search(pattern, message.text)

        if call_data:
            data["price_range"] = f"{call_data.group(1)}-{call_data.group(2)}"
            bot.set_state(user_id=user_id, state=UserInfoState.distance_range, chat_id=chat_id)

            bot.send_message(chat_id, text="Уточни диапазон расстояний от центра(км):\n(Пример: 1-10, 1 10)")
            bot.register_next_step_handler(message, distance_range)
        else:
            bot.send_message(text=f"Ошибка! Неправильный формат диапазона цен!\n"
                                  f"(Пример: 5000-15000, 5000 15000)\n"
                                  f"Введите диапазон цен(RUB):",
                             chat_id=chat_id)
            bot.register_next_step_handler(message, price_range)


@bot.message_handler(content_types=['text'])
def distance_range(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        pattern = r"(\d{1,3})[- ](\d{1,3})"
        call_data = re.search(pattern, message.text)

        if call_data:
            data["distance_range"] = f"{call_data.group(1)}-{call_data.group(2)}"
            bot.set_state(user_id=user_id, state=UserInfoState.checkIn, chat_id=chat_id)

            cur_date = datetime.date.today() + datetime.timedelta(days=1)
            calendar, step = DetailedTelegramCalendar(calendar_id=5, min_date=cur_date).build()
            bot.send_message(text=f"📅️↙️Выберите дату въезда: {LSTEP[step]}",
                             chat_id=chat_id,
                             reply_markup=calendar)
        else:
            bot.send_message(text=f"Ошибка! Неправильный формат диапазона расстояний!\n"
                                  f"(Пример: 1-10, 1 10)\n"
                                  f"Введите диапазон расстояний(км):",
                             chat_id=chat_id)
            bot.register_next_step_handler(message, distance_range)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=5))
def bestdeal_first_calendar_date(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    cur_date = datetime.date.today() + datetime.timedelta(days=1)
    result, key, step = DetailedTelegramCalendar(calendar_id=5, locale='ru', min_date=cur_date).process(call.data)
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
            calendar, step = DetailedTelegramCalendar(calendar_id=6, min_date=date).build()
            bot.send_message(text=f"📅️↗️Выберите дату выезда: {LSTEP[step]}",
                             chat_id=chat_id,
                             reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=6))
def bestdeal_second_calendar_date(call):
    chat_id = call.message.chat.id
    user_id = call.from_user.id

    with bot.retrieve_data(user_id=user_id, chat_id=chat_id) as data:
        year, mouth, day = map(int, str(data["checkIn"]).split("-"))
        date = datetime.date(year, mouth, day) + datetime.timedelta(days=1)
        result, key, step = DetailedTelegramCalendar(calendar_id=6, locale='ru', min_date=date).process(call.data)
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
                         reply_markup=bestdeal.quan_hotels_keyboard())


@bot.callback_query_handler(func=lambda call: call.data in bestdeal_calldata.quan_hotels_callback_data())
def bestdeal_get_num_hotels(call: CallbackQuery):
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
                          reply_markup=bestdeal.is_need_photos_keyboard())


@bot.callback_query_handler(func=lambda call: call.data in bestdeal_calldata.is_need_photos_callback_data())
def bestdeal_need_photos(call: CallbackQuery):
    chat_id = call.message.chat.id
    text = call.data

    if text == "yes3":
        with bot.retrieve_data(call.from_user.id, chat_id) as data:
            data["need_photo"] = True
            bot.set_state(call.from_user.id, UserInfoState.quan_photo, chat_id)

        bot.edit_message_text(text="Сколько фото нужно?",
                              chat_id=chat_id,
                              message_id=call.message.message_id,
                              reply_markup=bestdeal.quan_photos_keyboard())
    elif text == "no3":
        with bot.retrieve_data(call.from_user.id, chat_id) as data:
            data["need_photo"] = False
            data["quan_photo"] = 0
        final_data_handler(call, sorting="DISTANCE_FROM_LANDMARK", command="/bestdeal")


@bot.callback_query_handler(func=lambda call: call.data in bestdeal_calldata.quan_photos_callback_data())
def bestdeal_quan_photos(call: CallbackQuery):
    chat_id = call.message.chat.id

    with bot.retrieve_data(call.from_user.id, chat_id) as data:
        if len(call.data) == 3:
            data["quan_photo"] = int(call.data[1] + call.data[2])
        else:
            data["quan_photo"] = int(call.data[1])
    final_data_handler(call, sorting="DISTANCE_FROM_LANDMARK", command="/bestdeal")
