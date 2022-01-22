from safo_impro.service.normalized_indexes import NormalizedDifferenceIndex
from safo_impro.service.manage_raster_data import ManageRasterData
import os


class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.NI = NormalizedDifferenceIndex(self.image_path, 'sentinel')
        self.MRD = ManageRasterData()

    def normalized_indexes_calculation(self):
        """
        @WIP
        calculates the corresponding normalized indexes, and reprojects them
        parameters to add: type of index (++), filename, coordinate system (-)
        """

        self.NI.write_new_raster('ndvi')  # parametrizar

        input = self.image_path + 'ndvi.tif'  # parametrizar
        output = self.image_path + 'ndvi-reprojected.tif'  # parametrizar

        self.MRD.reprojection('EPSG:4326', input, output)

        masked = self.image_path + 'ndvi-masked.tif'
        self.MRD.calculate_specifics_mask(output, masked)

        os.remove(input)
        return output

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
        output = self.MRD.statistics_process(self.image_path, self.image_path)

        return output
