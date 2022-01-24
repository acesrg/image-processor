import argparse
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

args = parser.parse_args()

IP = ImageProcessor(args.path, args.operation)
IP.statistics_calculation()
