from telebot import types
from telebot.types import InlineKeyboardMarkup
from keyboards.inline.lowprice_calldata import lowprice_city_callback_data


def quan_hotels_keyboard() -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton(text='1', callback_data='a1')
    two = types.InlineKeyboardButton(text='2', callback_data='a2')
    three = types.InlineKeyboardButton(text='3', callback_data='a3')
    four = types.InlineKeyboardButton(text='4', callback_data='a4')
    five = types.InlineKeyboardButton(text='5', callback_data='a5')
    six = types.InlineKeyboardButton(text='6', callback_data='a6')
    seven = types.InlineKeyboardButton(text='7', callback_data='a7')
    eight = types.InlineKeyboardButton(text='8', callback_data='a8')
    nine = types.InlineKeyboardButton(text='9', callback_data='a9')
    ten = types.InlineKeyboardButton(text='10', callback_data='a10')
    keyboard.add(one, two, three, four, five, six, seven, eight, nine, ten)
    return keyboard


def quan_photos_keyboard() -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton(text='1', callback_data='b1')
    two = types.InlineKeyboardButton(text='2', callback_data='b2')
    three = types.InlineKeyboardButton(text='3', callback_data='b3')
    four = types.InlineKeyboardButton(text='4', callback_data='b4')
    five = types.InlineKeyboardButton(text='5', callback_data='b5')
    six = types.InlineKeyboardButton(text='6', callback_data='b6')
    seven = types.InlineKeyboardButton(text='7', callback_data='b7')
    eight = types.InlineKeyboardButton(text='8', callback_data='b8')
    nine = types.InlineKeyboardButton(text='9', callback_data='b9')
    ten = types.InlineKeyboardButton(text='10', callback_data='b10')
    keyboard.add(one, two, three, four, five, six, seven, eight, nine, ten)
    return keyboard


def is_need_photos_keyboard() -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text='Да', callback_data='yes1')
    no = types.InlineKeyboardButton(text='Нет', callback_data='no1')
    keyboard.add(yes, no)
    return keyboard


def city_markup(cities) -> InlineKeyboardMarkup:  # : List[Dict[str: str]]
    destinations = InlineKeyboardMarkup()

    lowprice_city_callback_data.clear()
    for city in cities:
        call_data = f'1{city["city_name"]}{city["destination_id"]}'
        lowprice_city_callback_data.append(call_data)
        destinations.add(types.InlineKeyboardButton(text=city['city_name'],
                                                    callback_data=call_data))
    return destinations




