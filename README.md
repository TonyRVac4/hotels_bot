<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Hotels Bot">
    <img src="utils/misc/1497618989-3_85123.png" alt="Logo" width="100" height="100">
  </a>
  <h2 align="center">Hotels Bot</h2>
</div>



<!-- ABOUT THE PROJECT -->
## About The Project

Telegram bot for hotel search. [API Hotels](https://rapidapi.com/apidojo/api/hotels4) is used to get data about hotels.


### Built With

* [![PyTelegramBotApi][PyTelegramBotApi.com]][PyTelegramBotApi-url]
* [![PeeWee][peewee.com]][peewee-url]
* [![PyTelegramBotCalendar][PyTelegramBotCalendar.com]][PyTelegramBotCalendar-url]
* [![Loguru][Loguru.com]][Loguru-url]



<!-- GETTING STARTED -->

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.
1. Clone the repo
   ```sh
   git clone https://gitlab.skillbox.ru/alen_koibaev/python_basic_diploma.git
   ```
2. Install All packages
   ```sh
   pip install requirements.txt
   ```
3. Rename `.env.template` to `.env`
4. Get a free TeleBot API Key at [https://t.me/BotFather](https://t.me/BotFather)
5. Get a free Hotels API Key at [https://rapidapi.com/apidojo/api/hotels4](https://rapidapi.com/apidojo/api/hotels4)
6. Create `main_database.db` file in `database` dir
7. Enter your APIs and path to DataBase in `.env`
   ```.dotenv
    BOT_TOKEN="TeleBot Key"
    RAPID_API_KEY="Hotel API Key"
    PATH_TO_DB="ABS path to DataBase"
   ```


<!-- USAGE EXAMPLES -->
## Usage
Run the file `main.py ` to start the bot.

[PyTelegramBotApi.com]: https://img.shields.io/badge/PyTelegramBotApi-0769AD?style=for-the-badge
[PyTelegramBotApi-url]: https://pypi.org/project/pyTelegramBotAPI
[peewee.com]: https://img.shields.io/badge/peewee-c8269a?style=for-the-badge
[peewee-url]: https://docs.peewee-orm.com/en/latest/
[PyTelegramBotCalendar.com]: https://img.shields.io/badge/PyTelegramBotCalendar-000000?style=for-the-badge
[PyTelegramBotCalendar-url]: https://github.com/artembakhanov/python-telegram-bot-calendar
[Loguru.com]: https://img.shields.io/badge/Loguru-ffffff?style=for-the-badge
[Loguru-url]: https://github.com/Delgan/loguru#readme