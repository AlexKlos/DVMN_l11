import os
from os.path import splitext
from urllib.parse import urlparse, unquote

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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        os.makedirs(folder, exist_ok=True)
        for index, url in enumerate(urls):
            extension = get_extension_from_url(url)
            assembled_filename = f'{filename}_{index}{extension}'
            filepath = os.path.join(folder, assembled_filename)
    
            response = requests.get(url, headers=headers)
            response.raise_for_status()
    
            with open(filepath, 'wb') as file:
                file.write(response.content)

        return True
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
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