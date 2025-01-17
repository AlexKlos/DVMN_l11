import os
import random
import time

from dotenv import load_dotenv
import telegram


def get_file_list(folder: str = 'images') -> list:
    '''Gets a list of file paths for all files in the specified folder and its subfolders.

    Args:
        folder (str, optional): Path to the folder to scan. Defaults to 'images'.

    Returns:
        list: A list of full file paths for all files in the folder and its subfolders. 
              Returns an empty list if an error occurs.
    '''
    paths = [os.path.join(curent_folder, file) for curent_folder, folders, files in os.walk(folder) for file in files]
    return paths


def post_images_from_folder(bot: telegram.Bot, 
                            chat_id: str, 
                            folder: str, 
                            pause: int, 
                            shuffle: bool=False) -> bool:
    '''Posts all images from folder to a Telegram chat.

    Args:
        bot (telegram.Bot): Instance of the Telegram bot.
        chat_id (str): ID of the chat where images will be posted.
        folder (str): Path to the folder containing images.
        pause (int): Pause between posts in seconds.
        shuffle (bool, optional): Determines the order of image posting. 
            If False, images are posted in order; 
            if True, the order is randomized. Defaults to False.

    Returns:
        bool: True if all images are successfully read and posted, otherwise False.
    '''
    files = get_file_list(folder)
    if shuffle:
        shuffle_list(files)
    for file in files:
        with open(file, 'rb') as image:
            bot.send_photo(chat_id, photo=image)
        time.sleep(pause)
    return True


def shuffle_list(list: list) -> list:
    '''Shuffles rndomly elements in list

    Args:
        list (list): List of objects

    Returns:
       list: List of shuffled elements
    '''
    return random.shuffle(list)


def main():
    load_dotenv()
    bot = telegram.Bot(token=os.environ['TELEGRAM_API_TOKEN'])
    chat_id = os.environ['TELEGRAM_CHAT_ID']
    pause = int(os.environ.get('PAUSE_BETWEEN_POSTS', 14400))
    folder = 'images'

    shuffle = False
    while True:
        try:
            post_images_from_folder(bot, chat_id, folder, pause, shuffle)
            shuffle = True
        except FileNotFoundError as e:
            print(f"Error: The folder '{folder}' was not found. {e}")
        except PermissionError as e:
            print(f"Error: Insufficient permissions to access the folder '{folder}' or its contents. {e}")
        except telegram.error.TelegramError as e:
            print(f"Telegram error while sending file: {e}")
        except OSError as e:
            print(f"OS error while accessing file: {e}")


if __name__ == '__main__':
    main()