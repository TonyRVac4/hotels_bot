from telebot import types
from telebot.types import InlineKeyboardMarkup
from keyboards.inline.highprice_calldata import city_callback_data


def quan_hotels_keyboard() -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton(text='1', callback_data='c1')
    two = types.InlineKeyboardButton(text='2', callback_data='c2')
    three = types.InlineKeyboardButton(text='3', callback_data='c3')
    four = types.InlineKeyboardButton(text='4', callback_data='c4')
    five = types.InlineKeyboardButton(text='5', callback_data='c5')
    six = types.InlineKeyboardButton(text='6', callback_data='c6')
    seven = types.InlineKeyboardButton(text='7', callback_data='c7')
    eight = types.InlineKeyboardButton(text='8', callback_data='c8')
    nine = types.InlineKeyboardButton(text='9', callback_data='c9')
    ten = types.InlineKeyboardButton(text='10', callback_data='c10')
    keyboard.add(one, two, three, four, five, six, seven, eight, nine, ten)
    return keyboard


def quan_photos_keyboard() -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton(text='1', callback_data='d1')
    two = types.InlineKeyboardButton(text='2', callback_data='d2')
    three = types.InlineKeyboardButton(text='3', callback_data='d3')
    four = types.InlineKeyboardButton(text='4', callback_data='d4')
    five = types.InlineKeyboardButton(text='5', callback_data='d5')
    six = types.InlineKeyboardButton(text='6', callback_data='d6')
    seven = types.InlineKeyboardButton(text='7', callback_data='d7')
    eight = types.InlineKeyboardButton(text='8', callback_data='d8')
    nine = types.InlineKeyboardButton(text='9', callback_data='d9')
    ten = types.InlineKeyboardButton(text='10', callback_data='d10')
    keyboard.add(one, two, three, four, five, six, seven, eight, nine, ten)
    return keyboard


def is_need_photos_keyboard() -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text='Да', callback_data='yes2')
    no = types.InlineKeyboardButton(text='Нет', callback_data='no2')
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
