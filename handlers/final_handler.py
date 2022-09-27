from telebot import types
from loader import bot
from requests_to_api.searchers import find_hotels, find_photos
from database.models import Users, Hotels, db


def final_data_handler(call, sorting, command=None):
    chat_id = call.message.chat.id

    with bot.retrieve_data(call.from_user.id, chat_id) as data:
        bot.edit_message_text(text="Ожидайте, подбираем отели...",
                              chat_id=chat_id,
                              message_id=call.message.message_id,
                              reply_markup=None)

        if command == "/bestdeal":
            hotels = find_hotels(id=data["dest_id"],
                                 checkIn=data["checkIn"],
                                 checkOut=data["checkOut"],
                                 quan_hotels=data["quan_hotels"],
                                 sorting=sorting,
                                 command=command,
                                 price_range=data["price_range"],
                                 distance_range=data["distance_range"])
        else:
            hotels = find_hotels(id=data["dest_id"],
                                 checkIn=data["checkIn"],
                                 checkOut=data["checkOut"],
                                 quan_hotels=data["quan_hotels"],
                                 sorting=sorting,
                                 command=command)

        if hotels:
            with db:
                Hotels.create(user_id='Null', hotel_info=command)

            bot.edit_message_text(text=f"Вот что удалось найти:",
                                  chat_id=chat_id,
                                  message_id=call.message.message_id)

            for hotel in hotels:
                hotel_url = 'https://hotels.com/ho{}'.format(str(hotel["destination_id"]))

                message = "🏨Отель: {hotel_name}\n🏠Адрес: {address}\n" \
                          "💵Стоимость за сутки: {day_price}\n" \
                          "💰Стоимость за {quan_day} суток: {full_price} RUB\n" \
                          "📏Расстояние до центра: {center_location}\n"\
                          "🌐Ссылка на сайт: {site}".format(hotel_name=hotel["hotel_name"],
                                                           address=hotel["address"],
                                                           day_price=hotel["price_per_day"],
                                                           quan_day=hotel["quan_day"],
                                                           full_price="{:,}".format(hotel["full_price"]),
                                                           center_location=hotel["center_location"],
                                                           site=hotel_url)
                with db:
                    Hotels.create(user_id=call.from_user.id, hotel_info=f"Город: {data['city']}\n{message}")

                if data["need_photo"]:
                    photos = find_photos(hotel=hotel, quan_photo=data["quan_photo"])
                    if photos:
                        if len(photos) >= 2:
                            photos_for_send = [types.InputMediaPhoto(media=path) for path in photos]
                            bot.send_media_group(chat_id=chat_id, media=photos_for_send)
                            bot.send_message(text=message, chat_id=chat_id, disable_web_page_preview=True)
                        else:
                            bot.send_photo(chat_id=chat_id, photo=photos[0], caption=message)
                    else:
                        bot.send_message(text="Фотографии не найдены\n{}".format(message), chat_id=chat_id, disable_web_page_preview=True)
                else:
                    bot.send_message(text=message, chat_id=chat_id, disable_web_page_preview=True)
        else:
            bot.send_message(text="Отели не найдены",
                             chat_id=chat_id)
