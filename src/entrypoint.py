from safo_impro.service.image_processor import ImageProcessor
import sys

IP = ImageProcessor(sys.argv[2])
IP.statistics_calculation()
# how to execute it: python3 service/entrypoint.py --path $PATH_TO_RASTER_FILES
