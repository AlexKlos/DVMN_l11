from datetime import datetime
import os
from os.path import splitext
from urllib.parse import urlparse, unquote

from dotenv import load_dotenv
import requests


def download_files(urls: list, folder: str = 'images', filename: str = 'space') -> bool:
    """Downloads the files at the specified URLs and saves them in the specified location.
    
    Args:
        urls (list): List of file URLs to download.
        folder (str, optional): Folder to save the files. Defaults to 'images'.
        filename (str, optional): Base filename for saving files. Defaults to 'space'.

    Returns:
        bool: True if all files were successfully downloaded, otherwise False.

    Raises:
        requests.exceptions.RequestException: If a network error occurs.
    """
    if not urls:
        print('No urls for dowload!')
        return False
    
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
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    

def get_extension_from_url(url: str) -> str:
    '''Parses the file extension from the download link

    Args:
        url (str): Download link.

    Returns:
        str: Returns extension.
    '''
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = unquote(path.split('/')[-1])
    extension = splitext(filename)[1]

    return extension


def get_spacex_launch_image(launch_id: str = 'latest') -> list:
    """Gets urls of photos from the SpaceX launch.
    
    Args:
        launch_id (str, optional): ID of the launch. Defaults to 'latest'.

    Returns:
        list: List of urls to download images.

    Raises:
        requests.exceptions.RequestException: If a network error occurs.
    """
    try:
        response = requests.get(f'https://api.spacexdata.com/v5/launches/{launch_id}')
        response.raise_for_status()
        urls = response.json()['links']['flickr']['original']
        if not urls:
            print('No images found for this iaunch.')
            return []
        
        return urls
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SpaceX launch images: {e}")
        return []
    

def get_nasa_apod(count: int) -> list:
    """Gets urls of photos from the NASA APOD.

    Args:
        count (int): Number of random photos to fetch from the APOD collection.

    Returns:
        list: List of urls to download images.

    Raises:
        requests.exceptions.RequestException: If a network error occurs.
    """
    try:
        load_dotenv()
        nasa_api_key = os.environ['NASA_API_KEY']
        params = {
            'count': count,
            'api_key': nasa_api_key
        }
        urls = []

        response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
        response.raise_for_status()
    
        for image_data in response.json():
            url = image_data['hdurl']
            urls.append(url)

        return urls
    except KeyError as e:
        print(f"Missing key in NASA APOD response: {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching NASA APOD images: {e}")
        return []
    

def get_nasa_epic() -> list:
    """Gets urls of photos from the NASA EPIC.

    Returns:
        list: List of urls to download images.

    Raises:
        requests.exceptions.RequestException: If a network error occurs.
    """
    try:
        load_dotenv()
        nasa_api_key = os.environ['NASA_API_KEY']
        params = {'api_key': nasa_api_key}
        
        response = requests.get('https://api.nasa.gov/EPIC/api/natural/images', params=params)
        response.raise_for_status()
    
        urls = []
        for image_data in response.json():
            image_name = image_data['image']
            image_date = image_data['date']
            image_parsed_date = datetime.strptime(image_date, '%Y-%m-%d %H:%M:%S')
            image_year = image_parsed_date.year
            image_month = str(image_parsed_date.month).zfill(2)
            image_day = str(image_parsed_date.day).zfill(2)
            urls.append(f'https://epic.gsfc.nasa.gov/archive/natural/{image_year}/{image_month}/{image_day}/png/{image_name}.png')

        return urls
    except requests.exceptions.RequestException as e:
        print(f"Error fetching NASA EPIC images: {e}")
        return []
    

def main():
    launch_id = input('SpaceX launch ID (default: latest): ')
    if launch_id == '':
        launch_id = 'latest'
    if download_files(get_spacex_launch_image(launch_id), folder='images'):
        print('SpaceX launch images downloaded correctly')
    else:
        print('SpaceX launch images downloaded not correctly')

    try:
        count = int(input('NASA APOD count: ') or 1)
    except Exception as e:
        print(f'Error: {e}')
        count = 1
    if download_files(get_nasa_apod(count), filename='nasa_apod'):
        print('NASA APOD images downloaded correctly')
    else:
        print('NASA APOD images downloaded not correctly')

    if download_files(get_nasa_epic(), 'images', 'nasa_epic'):
        print('NASA EPIC images downloaded correctly')
    else:
        print('NASA EPIC images downloaded not correctly')


if __name__ == '__main__':
    main()