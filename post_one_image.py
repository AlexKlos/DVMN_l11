import argparse
import os
import random

from dotenv import load_dotenv
import telegram

from post_all_images import get_file_list


def main():
    """Posts an image to a Telegram chat.

    If a filename is provided as an argument, that image is posted. 
    Otherwise, a random image from the 'images' folder is posted.

    Raises:
        FileNotFoundError: If the specified image file or folder does not exist.
        telegram.error.TelegramError: If there is an issue sending the photo to Telegram.
    """
    load_dotenv()
    bot = telegram.Bot(token=os.environ['TELEGRAM_API_TOKEN'])
    chat_id = os.environ['TELEGRAM_CHAT_ID']

    parser = argparse.ArgumentParser(description='Post one image to telegram')
    parser.add_argument('file', type=str, nargs='?', help='filename')
    args = parser.parse_args()

    folder = 'images'
    if args.file:
        file = os.path.join(folder, args.file)
    else:
        try:
            file = random.choice(get_file_list(folder))
        except FileNotFoundError as e:
            print(f"Error: The folder '{folder}' was not found. {e}")

    with open(file, 'rb') as image:
        try:
            bot.send_photo(chat_id, photo=image)
        except telegram.error.TelegramError as e:
            print(f"Telegram error while sending file: {e}")
            

if __name__ == '__main__':
    main()