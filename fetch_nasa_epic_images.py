from datetime import datetime
import os

from dotenv import load_dotenv
import requests

from file_utils import download_files


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
    """Main function to download images from NASA EPIC.

    Fetches the latest available images from the NASA EPIC API and saves them in the 'images' folder.

    Raises:
        requests.exceptions.RequestException: If a network error occurs during API calls.
        Exception: For other unexpected errors.
    """
    download_files(get_nasa_epic(), 'images', 'nasa_epic')


if __name__ == '__main__':
    main()