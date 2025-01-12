import argparse
import os

from dotenv import load_dotenv
import requests

from file_utils import download_files


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

 
def main():
    """Main function to download images from NASA APOD.

    Uses argparse to parse the command-line argument for the number of images to download.
    Downloads the specified number of images and saves them in the 'images' folder.

    Raises:
        requests.exceptions.RequestException: If a network error occurs during API calls.
        Exception: For other unexpected errors.
    """
    parser = argparse.ArgumentParser(description='Download images from the NASA APOD')
    parser.add_argument('count', 
                        type=int, 
                        nargs='?', 
                        help='Number of images to download (default: 1).')
    args = parser.parse_args()
    count = args.count if args.count else 1
    
    download_files(get_nasa_apod(count), 'images', 'nasa_apod')


if __name__ == '__main__':
    main()