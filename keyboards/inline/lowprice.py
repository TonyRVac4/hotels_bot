from telebot import types


def quan_hotels_keyboard():
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


def quan_photos_keyboard():
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


def is_need_photos_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(yes, no)
    return keyboard


def is_need_photos_callback_data() -> list:
    data = ["yes", "no"]
    return data


def quan_hotels_callback_data() -> list:
    data = ["a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8", "a9", "a10"]
    return data


def quan_photos_callback_data() -> list:
    data = ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9", "b10"]
    return data
