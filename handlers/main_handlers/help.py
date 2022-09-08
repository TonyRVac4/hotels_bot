from telebot.types import Message
from config_data.config import UI_COMMANDS
from loader import bot


@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in UI_COMMANDS]
    bot.send_message(message.chat.id, '\n'.join(text))
