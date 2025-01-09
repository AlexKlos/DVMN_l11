import os

import telegram
from dotenv import load_dotenv


def main():
    load_dotenv()
    bot = telegram.Bot(token=os.environ['TELEGRAM_API_TOKEN'])

    # Получение обновлений
    # updates = bot.get_updates()
    # for update in updates:
    #     if update.message:  # Проверяем, есть ли message
    #         print(update.message.chat.id)
    #     else:
    #         print("Обновление не содержит сообщения:", update)

    # Пример отправки сообщения, замените chat_id на корректный
    bot.send_message(chat_id=-1002461230862, text="Bupa-Bopa_Bipa")


if __name__ == '__main__':
    main()