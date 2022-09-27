from database.models import Users, Hotels
from datetime import date


message = "🏨Отель: {hotel_name}\n🏠Адрес: {address}\n" \
                          "💵Стоимость за сутки: {day_price}\n" \
                          "💰Стоимость за {quan_day} суток: {full_price} RUB\n" \
                          "📏Расстояние до центра: {center_location}\n"\
                          "🌐Ссылка на сайт: {site}"


a = Users.select().where(Users.user_id == 11881 and Users.name == 'Вася')
b = Users.select().where(Users.user_id == 24124 and Users.name == 'Вася')
print(a, "\n", b)