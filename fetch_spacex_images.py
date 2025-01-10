import argparse

from fetch_all_space_images import download_files, get_spacex_launch_image


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