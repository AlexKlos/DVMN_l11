import argparse

from main import download_files, get_spacex_launch_image


def main():
    parser = argparse.ArgumentParser(description='Download photos from the SpaceX launch')
    parser.add_argument('id', type=str, nargs='?', help='SpaceX launch ID')
    args = parser.parse_args()
    id = args.id if args.id else 'latest'

    download_files(get_spacex_launch_image(id), 'images', 'spacex')


if __name__ == '__main__':
    main()