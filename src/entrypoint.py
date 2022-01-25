import argparse
import logging
from safo_impro.service.image_processor import ImageProcessor

parser = argparse.ArgumentParser(description="Image processor")

parser.add_argument(
    '-p', '--path', type=str, required=True,
    help='Folder location of the raster.',
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
if args.log_level == None:
    level = 'INFO'
else:
    level = args.log_level

level_dict = {
    'CRITICAL' : logging.CRITICAL,
    'ERROR' : logging.ERROR,
    'WARNING' : logging.WARNING,
    'DEBUG': logging.DEBUG,
    'INFO' : logging.INFO,
}

IP = ImageProcessor(args.path, args.operation, level_dict[level])
IP.statistics_calculation()
