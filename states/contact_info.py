from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    city = State()
    quan_hotels = State()
    need_photo = State()
    quan_photo = State()


