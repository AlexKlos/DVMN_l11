import os

import telegram
from dotenv import load_dotenv


def main():
    load_dotenv()
    bot = telegram.Bot(token=os.environ['TELEGRAM_API_TOKEN'])
    chat_id = os.environ['TELEGRAM_CHAT_ID']

    image_path = 'images/nasa_apod_0.jpg'
    with open(image_path, 'rb') as image:
        bot.send_photo(chat_id=chat_id, photo=image)


if __name__ == '__main__':
    main()