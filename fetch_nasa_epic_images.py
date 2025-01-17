from datetime import datetime
import os

from dotenv import load_dotenv
import requests

from file_utils import download_files


def get_nasa_epic(nasa_api_key: str) -> list:
    """Gets urls of photos from the NASA EPIC.

    Args:
        nasa_api_key (str): NASA API key.

    Returns:
        list: List of urls to download images.

    Raises:
        requests.exceptions.RequestException: If a network error occurs.
    """
    params = {'api_key': nasa_api_key}
    
    response = requests.get('https://api.nasa.gov/EPIC/api/natural/images', params=params)
    response.raise_for_status()

    urls = [f"https://epic.gsfc.nasa.gov/archive/natural/{datetime.strptime(image_data['date'], '%Y-%m-%d %H:%M:%S').year}/{str(datetime.strptime(image_data['date'], '%Y-%m-%d %H:%M:%S').month).zfill(2)}/{str(datetime.strptime(image_data['date'], '%Y-%m-%d %H:%M:%S').day).zfill(2)}/png/{image_data['image']}.png" for image_data in response.json()]
    return urls
   

def main():
    """Main function to download images from NASA EPIC.

    Fetches the latest available images from the NASA EPIC API and saves them in the 'images' folder.
    """
    load_dotenv()
    nasa_api_key = os.environ['NASA_API_KEY']
    
    try:
        download_files(get_nasa_epic(nasa_api_key), 'images', 'nasa_epic')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching NASA EPIC images: {e}")


if __name__ == '__main__':
    main()