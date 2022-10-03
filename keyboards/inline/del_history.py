from telebot import types
from telebot.types import InlineKeyboardMarkup


def del_history() -> InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Вывести историю поиска", callback_data="output")
    button2 = types.InlineKeyboardButton(text="Удалить историю", callback_data="del")

    keyboard.add(button1, button2)
    return keyboard


del_history_call_data = ["output", "del"]
