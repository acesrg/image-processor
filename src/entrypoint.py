import argparse
import logging
from os.path import exists
from safo_impro.service.image_processor import ImageProcessor

parser = argparse.ArgumentParser(description="Image processor")

parser.add_argument(
    '-ip', '--image_path', type=str, required=True,
    help='Folder location of the raster.',
)

parser.add_argument(
    '-sp', '--shp_path', type=str, required=True,
    help='Folder location of the polygons file.',
)

parser.add_argument(
    '-o', '--operation', type=str, required=True, choices=['NDVI', 'NDWI'],
    help='Operation to be performed.',
)

parser.add_argument(
    '-l', '--log_level', type=str, choices=['CRITICAL', 'ERROR', 'WARNING', 'DEBUG'],
    help='Logging level. Default set to INFO',
)

args = parser.parse_args()

level = ''
if args.log_level is None:
    level = 'INFO'
else:
    level = args.log_level

level_dict = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
}

shp_path = args.shp_path
image_path = args.image_path

if not exists(shp_path):
    print("No such file: " + shp_path)
    quit()
elif not exists(image_path):
    print("No such file: " + image_path)
    quit()

IP = ImageProcessor(args.shp_path, args.image_path, args.operation, level_dict[level])
IP.statistics_calculation()
