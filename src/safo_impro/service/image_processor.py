from safo_impro.service.normalized_indexes import NormalizedDifferenceIndex
from safo_impro.service.manage_raster_data import ManageRasterData
import os
import logging


class ImageProcessor:
    def __init__(self, shp_path, image_path, operation, logging_level):
        self.shp_path = shp_path
        self.image_path = image_path
        self.operation = operation
        self.NI = NormalizedDifferenceIndex(self.image_path, 'sentinel')
        self.MRD = ManageRasterData()
        self.logger = self.set_logging_level(logging_level)

    def normalized_indexes_calculation(self):
        """
        calculates the corresponding normalized indexes, and reprojects them
        @WIP: parameters to add: coordinate system (nice to have)
        """
        try:
            self.NI.write_new_raster(self.operation)
        except Exception:
            self.logger.error("Exception occurred", exc_info=True)
            raise

        input = "{image_path}{operation}.tif".format(image_path=self.image_path, operation=self.operation)
        reprojected = "{image_path}{operation}-REPROJECTED.tif".format(image_path=self.image_path, operation=self.operation)
        masked = "{image_path}{operation}-MASKED.tif".format(image_path=self.image_path, operation=self.operation)

        self.MRD.reprojection('EPSG:4326', input, reprojected)
        self.MRD.calculate_specifics_mask(reprojected, masked)

        # por ahora me quedo con la reproyectada y con la enmascarada (pero no sé si conviene quedarme sólo con la enmascarada)
        os.remove(input)
        return masked

    def statistics_calculation(self):
        """
            este es el primer paso
            primero calcula el índice que corresponda
            y luego le saca las estadísticas
        """
        raster_name = self.normalized_indexes_calculation()
        self.MRD.parse_coordinates_from_shapefile(self.shp_path, self.image_path, raster_name, "ISO8859-1")
        output = self.MRD.statistics_process(self.image_path, self.operation)

        return output

    def set_logging_level(self, logging_level):
        logger = logging.getLogger()
        logger.setLevel(logging_level)

        return logger
