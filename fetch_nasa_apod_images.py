import argparse
import os

from dotenv import load_dotenv
import requests

from file_utils import download_files


def get_nasa_apod(count: int, nasa_api_key: str) -> list:
    """Gets urls of photos from the NASA APOD.

    Args:
        count (int, optional): Number of random photos to fetch from the APOD 
        collection. Default to 1.
        nasa_api_key (str): NASA API key.

    Returns:
        list: List of urls to download images.

    Raises:
        requests.exceptions.RequestException: If a network error occurs.
    """
    params = {
        'count': count,
        'api_key': nasa_api_key
    }
    response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
    response.raise_for_status()

    urls = [image_data['hdurl'] for image_data in response.json()]
    return urls

 
def main():
    """Main function to download images from NASA APOD.

    Uses argparse to parse the command-line argument for the number of images to download.
    Downloads the specified number of images and saves them in the 'images' folder.
    """
    load_dotenv()
    nasa_api_key = os.environ['NASA_API_KEY']
    
    parser = argparse.ArgumentParser(description='Download images from the NASA APOD')
    parser.add_argument('count', 
                        type=int, 
                        nargs='?',
                        default=1,
                        help='Number of images to download (default: 1).')
    args = parser.parse_args()
    count = args.count
    
    try:
        download_files(get_nasa_apod(count, nasa_api_key), 'images', 'nasa_apod')
    except KeyError as e:
        print(f"Missing key in NASA APOD response: {e}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching NASA APOD images: {e}")
        return []


if __name__ == '__main__':
    main()