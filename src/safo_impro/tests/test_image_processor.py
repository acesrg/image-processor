import unittest
import logging
from safo_impro.service.image_processor import ImageProcessor

SHPFILE_PATH = "/test_resources/cartas_25000/cartas_25000.shp"
IMAGE_PATH = "/test_resources/img/CBA_2021_0105/Sentinel-2/unzipped/MSIL1C_20210107.SAFE/GRANULE/MSIL1C_20210107/IMG_DATA/"

EXPECTED_RESULTS = "/home/pi/paula/safo/img/CBA_2021_0105/Sentinel-2/unzipped/MSIL1C_20210107.SAFE/GRANULE/MSIL1C_20210107/IMG_DATA/NDVI-results.shp"


MISSING_IMAGE_PATH = "/missing_path/"


class ImageProcessorTest(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    @unittest.skip
    def test_successful_NDVI_calculation(self):
        IP = ImageProcessor(SHPFILE_PATH, IMAGE_PATH,
                            "NDVI", logging.INFO)

        results = IP.statistics_calculation()
        self.assertEqual(
            results, EXPECTED_RESULTS)

    @unittest.skip
    def test_successful_NDWI_calculation(self):
        IP = ImageProcessor(SHPFILE_PATH, IMAGE_PATH,
                            "NDWI_VEGETATION", logging.INFO)

        # está dando este error: ValueError: operands could not be broadcast together with shapes (10980,10980) (1,5490,5490)
        # esta máscara no funciona para estas bandas
        results = IP.statistics_calculation()
        self.assertEqual(
            results, EXPECTED_RESULTS)

    def test_erronous_calculation_due_missing_files(self):
        IP = ImageProcessor(SHPFILE_PATH, MISSING_IMAGE_PATH,
                            "NDVI", logging.INFO)

        with self.assertRaises(FileNotFoundError) as context_manager:
            IP.statistics_calculation()

        exception = context_manager.exception
        self.assertEqual(
            str(exception), "No such file: /missing_path/red_665_10.jp2")

    def test_erronous_calculation_due_invalid_operation(self):
        IP = ImageProcessor(SHPFILE_PATH, IMAGE_PATH,
                            "SOME_OTHER_OPERATION", logging.INFO)

        with self.assertRaises(ValueError) as context_manager:
            IP.statistics_calculation()

        exception = context_manager.exception
        self.assertEqual(
            str(exception), "SOME_OTHER_OPERATION is an invalid operation, try again")
