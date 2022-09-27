from telebot.custom_filters import StateFilter
from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
from database.models import create_tables, db


if __name__ == '__main__':
    create_tables()
    bot.add_custom_filter(StateFilter(bot))
    set_default_commands(bot)
    bot.infinity_polling()
