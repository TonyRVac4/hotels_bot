from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    city = State()
    dest_id = State()
    checkIn = State()
    checkOut = State()
    quan_hotels = State()
    need_photo = State()
    quan_photo = State()


