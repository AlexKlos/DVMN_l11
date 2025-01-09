from datetime import datetime
import os
from os.path import splitext
from urllib.parse import urlparse, unquote

from dotenv import load_dotenv
import requests


def download_files(urls: list, folder: str = 'images', filename: str = 'space') -> bool:
    '''Downloads the files at the specified URLs and saves it in the specified location.
    
    Args:
        urls (list): Link to the file.
        folder (str): Folder for save.
        filename (str): Filename for save.

    Returns:
        bool: Returns True if the files has been successfully downloaded and saved, 
            otherwise False.
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        os.makedirs(folder, exist_ok=True)
        for i, url in enumerate(urls):
            extension = get_extension_from_url(url)
            assembled_filename = f'{filename}_{i}{extension}'
            filepath = os.path.join(folder, assembled_filename)
    
            response = requests.get(url, headers=headers)
            response.raise_for_status()
    
            with open(filepath, 'wb') as file:
                file.write(response.content)

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


def get_spacex_launch_image(launch_id: str = 'latest') -> list:
    '''Get urls of photos from the SpaceX launch
    
    Args:
        launch_id (str): ID of the launch. If the value is not passed, 
            photos of the last launch will be downloaded.

    Returns:
        list: Returns List of urls to dowload images.
    '''
    try:
        response = requests.get(f'https://api.spacexdata.com/v5/launches/{launch_id}')
        response.raise_for_status()
        urls = response.json()['links']['flickr']['original']
    except Exception as e:
        print(f'Ошибка скачивания: {e}')

    return urls
    

def get_nasa_apod(count: int) -> list:
    '''Get urls of photos from the NASA APOD

    Args:
        count (int): Number of random photos to get links from the APOD collection.

    Returns:
        list: Returns List of urls to dowload images.
    '''
    load_dotenv()
    NASA_API_KEY = os.environ['NASA_API_KEY']
    params = {
        'count': count,
        'api_key': NASA_API_KEY
    }
    urls = []

    try:
        response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
        response.raise_for_status()
    
        for i, image_data in enumerate(response.json()):
            url = image_data['hdurl']
            urls.append(url)
    except Exception as e:
        print(f'Ошибка скачивания: {e}')

    return urls
    

def get_nasa_epic() -> list:
    '''Get urls of photos from the NASA EPIC

    Returns:
        list: Returns List of urls to dowload images.
    '''
    load_dotenv()
    NASA_API_KEY = os.environ['NASA_API_KEY']
    params = {
        'api_key': NASA_API_KEY
    }
    urls = []

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
            urls.append(url)
    except Exception as e:
        print(f'Ошибка скачивания: {e}')

    return urls
    

def main():
    id = input('SpaceX launch ID: ')
    if id == '':
        id = 'latest'
    print('SpaceX - ', download_files(get_spacex_launch_image(id), folder='images'))

    count = input('NASA APOD count: ')
    if count == '':
        count = 1
    else:
        count = int(count)
    print('APOD - ', download_files(get_nasa_apod(count), filename='nasa_apod'))

    print('EPIC - ', download_files(get_nasa_epic(), 'images', 'nasa_epic'))


if __name__ == '__main__':
    main()