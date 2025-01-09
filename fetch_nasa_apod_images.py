import argparse

from fetch_all_space_images import download_files, get_nasa_apod


parser = argparse.ArgumentParser(description='Download images from the NASA APOD')
parser.add_argument('count', type=int, nargs='?', help='Images count')
args = parser.parse_args()
count = args.count if args.count else 1

download_files(get_nasa_apod(count), 'images', 'nasa_apod')