import argparse

from fetch_all_space_images import download_files, get_nasa_apod


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