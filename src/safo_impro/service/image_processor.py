from safo_impro.service.normalized_indexes import NormalizedDifferenceIndex
from safo_impro.service.manage_raster_data import ManageRasterData
import os


class ImageProcessor:
    def __init__(self, image_path, operation):
        self.image_path = image_path
        self.operation = operation
        self.NI = NormalizedDifferenceIndex(self.image_path, 'sentinel')
        self.MRD = ManageRasterData()

    def normalized_indexes_calculation(self):
        """
        calculates the corresponding normalized indexes, and reprojects them
        @WIP: parameters to add: filename, coordinate system (nice to have)
        """
        self.NI.write_new_raster(self.operation)

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
            primero calcula el ndvi en general
            y luego le saca las estadísticas

            @WIP
            habría que agregar un paso al medio para que enmascare lo que no tiene que calcular
            eso por un lado sería mas fácil rápido? para hacer los calculos
            pero por el otro lado sería más fácil agarrarlo al final una vez que está calculado el ndvi porque es una sola capa...
        """
        self.normalized_indexes_calculation()  # que haga el calculo que tiene que hacer
        output = self.MRD.statistics_process(self.image_path, self.image_path, self.operation)

        return output
