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
    try:
        load_dotenv()
        bot = telegram.Bot(token=os.environ['TELEGRAM_API_TOKEN'])
        CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
    
        parser = argparse.ArgumentParser(description='Post one image to telegram')
        parser.add_argument('file', type=str, nargs='?', help='filename')
        args = parser.parse_args()
    
        folder = 'images'
        if args.file:
            file = os.path.join(folder, args.file)
        else:
            file = random.choice(get_file_list(folder))
    
        with open(file, 'rb') as image:
            bot.send_photo(CHAT_ID, photo=image)
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    main()