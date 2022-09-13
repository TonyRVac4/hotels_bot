import re
from telebot import types
from loader import bot
from requests_to_api.searchers import find_hotels, find_photos


def final_data_handler(call):
    chat_id = call.message.chat.id

    with bot.retrieve_data(call.from_user.id, chat_id) as data:
        bot.edit_message_text(text="Ожидайте, подбираем отели...",
                              chat_id=chat_id,
                              message_id=call.message.message_id,
                              reply_markup=None)
        hotels = find_hotels(id=data["dest_id"],
                             checkIn=data["checkIn"],
                             checkOut=data["checkOut"],
                             quan_hotels=data["quan_hotels"],
                             sorting="PRICE")

        if hotels:
            bot.edit_message_text(text=f"Вот что удалось найти:",
                                  chat_id=chat_id,
                                  message_id=call.message.message_id)

            for hotel in hotels:
                hotel_url = 'https://hotels.com/ho{}'.format(str(hotel["destination_id"]))

                full_price = hotel["full_price"].split(" ")
                quan_day = re.match(r"\d+", full_price[3])
                quan_day = quan_day.group()
                message = "🏨Отель: {hotel_name}\n🏠Адрес: {address}\n" \
                          "💵Стоимость за сутки: {day_price}\n" \
                          "💰Стоимость за {quan_day} суток: {full_price}\n" \
                          "🌐Ссылка на сайт: {site}".format(hotel_name=hotel["hotel_name"],
                                                           address=hotel["address"],
                                                           day_price=hotel["price_per_day"],
                                                           quan_day=quan_day,
                                                           full_price=full_price[1],
                                                           site=hotel_url)
                if data["need_photo"]:
                    photos = find_photos(hotel=hotel, quan_photo=data["quan_photo"])
                    if len(photos) >= 2:
                        photos_for_send = [types.InputMediaPhoto(media=path) for path in photos]
                        bot.send_media_group(chat_id=chat_id, media=photos_for_send)
                        bot.send_message(text=message, chat_id=chat_id, disable_web_page_preview=True)
                    else:
                        bot.send_photo(chat_id=chat_id, photo=photos[0], caption=message, disable_web_page_preview=True)
                else:
                    bot.send_message(text=message, chat_id=chat_id, disable_web_page_preview=True)
        else:
            bot.send_message(text="Отели не найдены",
                             chat_id=chat_id)
