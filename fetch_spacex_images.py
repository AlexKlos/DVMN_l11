import argparse

import requests

from file_utils import download_files


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
    

def main():
    """Main function to download photos from a SpaceX launch.

    Uses the SpaceX API to fetch photos from a specific launch 
    and saves them in the 'images' folder.

    Raises:
        requests.exceptions.RequestException: If a network error occurs during API calls.
        Exception: For other unexpected errors.
    """
    parser = argparse.ArgumentParser(description='Download photos from the SpaceX launch')
    parser.add_argument(
        'id', 
        type=str, 
        nargs='?', 
        help='SpaceX launch ID (defaults to the latest launch if not specified)'
    )
    args = parser.parse_args()
    id = args.id if args.id else 'latest'
    
    download_files(get_spacex_launch_image(id), 'images', 'spacex')


if __name__ == '__main__':
    main()