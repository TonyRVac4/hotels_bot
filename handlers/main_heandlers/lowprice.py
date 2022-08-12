from loader import bot
from telebot.types import Message
from keyboards.inline.lowprice import quan_hotels_keyboard, quan_photos_keyboard, is_need_photos_keyboard
from keyboards.inline.lowprice import quan_hotels_callback_data, quan_photos_callback_data, is_need_photos_callback_data
from telebot.types import CallbackQuery


@bot.message_handler(commands=['lowprice'])
def low_price(message: Message):
    id = message.chat.id

    bot.send_message(id, "Введите Город, где хотите найти отель:")
    bot.register_next_step_handler(message, get_city)


@bot.message_handler(content_types="text")
def get_city(message: Message):
    id = message.chat.id

    if message.text.isalpha():
        bot.send_message(id, text="Введите кол-во отелей, которые необходимо вывести: ", reply_markup=quan_hotels_keyboard())
        bot.register_next_step_handler(message, get_num_hotels)
    else:
        bot.send_message(id, "Название города должно быть только из букв\nВведите Город, где хотите найти отель:")


@bot.callback_query_handler(func=lambda call: call.data in quan_hotels_callback_data())
def get_num_hotels(call: CallbackQuery):
    id = call.message.chat.id

    bot.send_message(id, "Нужно-ли выводить фотографий для каждого отеля («Да/Нет»)", reply_markup=is_need_photos_keyboard())


@bot.callback_query_handler(func=lambda call: call.data in is_need_photos_callback_data())
def need_photos(call: CallbackQuery):
    id = call.message.chat.id
    text = call.data

    if text == "yes":
        bot.send_message(id, "Сколько фото нужно?", reply_markup=quan_photos_keyboard())
        # пользователь также вводит количество необходимых фотографий
    elif text == "no":
        pass


@bot.callback_query_handler(func=lambda call: call.data in quan_photos_callback_data())
def quan_photos(call: CallbackQuery):
    id = call.message.chat.id

    bot.send_message(id, "Вы завершили регистрацию")
