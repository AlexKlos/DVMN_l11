from fetch_all_space_images import download_files, get_nasa_epic


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