from datetime import datetime
import os
from os.path import splitext
from urllib.parse import urlparse, unquote

from dotenv import load_dotenv
import requests


def download_file(url: str, filename: str, folder: str) -> bool:
    '''Downloads the file at the specified URL and saves it in the specified location.
    
    Args:
        url (str): Link to the file.
        filename (str): Filename for save.
        folder (str): Folder for save.

    Returns:
        bool: Returns True if the file has been successfully downloaded and saved, 
            otherwise False.
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, filename)

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        with open(filepath, 'wb') as file:
            file.write(response.content)

        return True
    except Exception as e:
        print(f'Ошибка скачивания: {e}')
        return False
    

def fetch_spacex_launch_image(launch_id: str = 'latest') -> bool:
    '''Downloads and saves photos from the SpaceX launch
    
    Args:
        launch_id (str): ID of the launch. If the value is not passed, 
            photos of the last launch will be downloaded.

    Returns:
        bool: Returns True if the files has been successfully 
            downloaded and saved, otherwise False.
    '''
    try:
        response = requests.get(f'https://api.spacexdata.com/v5/launches/{launch_id}')
        response.raise_for_status()
        urls = response.json()['links']['flickr']['original']
    
        for i, url in enumerate(urls):
            download_file(url, f'spacex_{i}.jpg', 'images')

        return True
    except Exception as e:
        print(f'Ошибка скачивания: {e}')
        return False
    

def get_nasa_apod(count: int) -> bool:
    '''Downloads and saves photos from the NASA APOD

    Args:
        count (int): Number of random photos to download from the APOD collection.

    Returns:
        bool: Returns True if the files has been successfully downloaded and saved, 
            otherwise False.
    '''
    load_dotenv()
    NASA_API_KEY = os.environ['NASA_API_KEY']
    params = {
        'count': count,
        'api_key': NASA_API_KEY
    }

    try:
        response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
        response.raise_for_status()
    
        for i, image_data in enumerate(response.json()):
            url = image_data['hdurl']
            extension = get_extension_from_url(url)
            download_file(url, f'nasa_apod_{i}.{extension}', 'images')
        return True
    except Exception as e:
        print(f'Ошибка скачивания: {e}')
        return False
    

def get_nasa_epic() -> bool:
    '''Downloads and saves photos from the NASA EPIC

    Returns:
        bool: Returns True if the files has been successfully downloaded and saved, 
            otherwise False.
    '''
    load_dotenv()
    NASA_API_KEY = os.environ['NASA_API_KEY']
    params = {
        'api_key': NASA_API_KEY
    }

    try:
        response = requests.get('https://api.nasa.gov/EPIC/api/natural/images', params=params)
        response.raise_for_status()
    
        for i, image_data in enumerate(response.json()):
            image_name = image_data['image']
            image_date = image_data['date']
            image_parsed_date = datetime.strptime(image_date, '%Y-%m-%d %H:%M:%S')
            image_year = image_parsed_date.year
            image_month = str(image_parsed_date.month).zfill(2)
            image_day = str(image_parsed_date.day).zfill(2)
            url = f'https://epic.gsfc.nasa.gov/archive/natural/{image_year}/{image_month}/{image_day}/png/{image_name}.png'

            download_file(url, f'nasa_epic_{i}.png', 'images')
        return True
    except Exception as e:
        print(f'Ошибка скачивания: {e}')
        return False
    

def get_extension_from_url(url: str) -> str:
    '''Parses the file extension from the download link

    Args:
        url (str): Download link

    Returns:
        str: Returns extension.
    '''
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = unquote(path.split('/')[-1])
    extension = splitext(filename)[1]

    return extension
    

def main():
    print('SpaceX - ', fetch_spacex_launch_image('5eb87d42ffd86e000604b384'))
    print('APOD - ', get_nasa_apod(5))
    print('EPIC - ', get_nasa_epic())


if __name__ == '__main__':
    main()