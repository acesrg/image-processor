from normalized_indexes import NormalizedDifferenceIndex
from manage_raster_data import ManageRasterData
import os
import sys


class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.NI = NormalizedDifferenceIndex(self.image_path, 'sentinel')
        self.MRD = ManageRasterData()

    def normalized_indexes_calculation(self):
        self.NI.write_new_raster('ndvi')  # parametrizar

        input = self.image_path + 'ndvi.tif'  # parametrizar
        output = self.image_path + 'ndvi-reprojected.tif'  # parametrizar

        self.MRD.reprojection('EPSG:4326', input, output)

        os.remove(input)
        return output

    def statistics_calculation(self):
        self.normalized_indexes_calculation()  #  que haga el calculo que tiene que hacer
        output = self.MRD.statistics_process(self.image_path, self.image_path)

        return output


IP = ImageProcessor(sys.argv[2])
IP.statistics_calculation()

# how to execute it: python src/service/image_processor.py --path {path_to_files}
