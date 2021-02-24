from ..model import models
import json


class InitInformation:
    """
    Representa toda la información de la imagen una vez procesada. Es lo que deberí­a devolver el POST CalculateNDVI.
    """
    def __init__(self, file_name):
        self.file_name = file_name

    def _init_ndvi(self):
        """
        Returns a NormalizedDifferenceIndex instance
        """
        # TODO paramentrizar el nombre del sate como se hizo en la clase Norm indexes
        return NormalizedDifferenceIndex(self.file_name, 'sentinel')

    def _init_satellite_image(self):
        ndvi_instance = self._init_ndvi()

        # TODO parametrizar fecha, tag, etc (estos sÃ³lo son datos de prueba)
        date_time = '2012-04-23T18:25:43.511Z'
        geographicInformation = models.GeographicInformation('test_tag', ndvi_instance.show_image_coordinates(self.file_name + 'red.jp2'))

        ndvi, dimensions = ndvi_instance.calculate_ndvi()
        # normalizedIndexes = models.NormalizedIndexes(ndvi.tolist(), 0)

        # temporalmente no muestro los índices porque es un array desastroso
        satelliteImageProcessed = models.SatelliteImageProcessed(self.file_name, json.dumps(geographicInformation.__dict__), date_time, 0)

        return satelliteImageProcessed.__dict__
