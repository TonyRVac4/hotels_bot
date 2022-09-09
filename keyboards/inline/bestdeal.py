from telebot import types
from telebot.types import InlineKeyboardMarkup
from keyboards.inline.bestdeal_calldata import city_callback_data


def quan_hotels_keyboard() -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton(text='1', callback_data='e1')
    two = types.InlineKeyboardButton(text='2', callback_data='e2')
    three = types.InlineKeyboardButton(text='3', callback_data='e3')
    four = types.InlineKeyboardButton(text='4', callback_data='e4')
    five = types.InlineKeyboardButton(text='5', callback_data='e5')
    six = types.InlineKeyboardButton(text='6', callback_data='e6')
    seven = types.InlineKeyboardButton(text='7', callback_data='e7')
    eight = types.InlineKeyboardButton(text='8', callback_data='e8')
    nine = types.InlineKeyboardButton(text='9', callback_data='e9')
    ten = types.InlineKeyboardButton(text='10', callback_data='e10')
    keyboard.add(one, two, three, four, five, six, seven, eight, nine, ten)
    return keyboard


def quan_photos_keyboard() -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton(text='1', callback_data='f1')
    two = types.InlineKeyboardButton(text='2', callback_data='f2')
    three = types.InlineKeyboardButton(text='3', callback_data='f3')
    four = types.InlineKeyboardButton(text='4', callback_data='f4')
    five = types.InlineKeyboardButton(text='5', callback_data='f5')
    six = types.InlineKeyboardButton(text='6', callback_data='f6')
    seven = types.InlineKeyboardButton(text='7', callback_data='f7')
    eight = types.InlineKeyboardButton(text='8', callback_data='f8')
    nine = types.InlineKeyboardButton(text='9', callback_data='f9')
    ten = types.InlineKeyboardButton(text='10', callback_data='f10')
    keyboard.add(one, two, three, four, five, six, seven, eight, nine, ten)
    return keyboard


def is_need_photos_keyboard() -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text='Да', callback_data='yes3')
    no = types.InlineKeyboardButton(text='Нет', callback_data='no3')
    keyboard.add(yes, no)
    return keyboard


def city_markup(cities) -> InlineKeyboardMarkup:  # : List[Dict[str: str]]
    destinations = InlineKeyboardMarkup()

    city_callback_data.clear()
    for city in cities:
        call_data = f'2{city["city_name"]}{city["destination_id"]}'
        city_callback_data.append(call_data)
        destinations.add(types.InlineKeyboardButton(text=city['city_name'],
                                                    callback_data=call_data))
    return destinations
