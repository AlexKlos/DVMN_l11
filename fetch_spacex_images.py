import argparse

from fetch_all_space_images import download_files, get_spacex_launch_image


parser = argparse.ArgumentParser(description='Download photos from the SpaceX launch')
parser.add_argument('id', type=str, nargs='?', help='SpaceX launch ID')
args = parser.parse_args()
id = args.id if args.id else 'latest'

download_files(get_spacex_launch_image(id), 'images', 'spacex')