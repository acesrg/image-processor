import rasterio
from rasterio import plot
from rasterio import errors as re
import numpy as np
import os

satellite_extensions = {
    'sentinel': '.jp2',
    'landsat8a': '.tif',
}


class NormalizedDifferenceIndex:
    def __init__(self, image_path, satellite):
        self.red_path = image_path + 'red_665_10' + satellite_extensions[satellite]
        self.nir10_path = image_path + 'nir4_832_10' + satellite_extensions[satellite]
        self.nir20_path = image_path + 'nir_3' + satellite_extensions[satellite]
        self.swir_path = image_path + 'swir' + satellite_extensions[satellite]

        self.ndvi_path = image_path + 'ndvi.tif'
        self.ndwi_path = image_path + 'ndwi.tif'
        # self.red_path = image_path + 'B4' + satellite_extensions[satellite]

    @staticmethod
    def _load_image(src_path):
        if os.path.isfile(src_path) == True:
            return rasterio.open(src_path)
        else:
            print("no such file " + src_path)

    def calculate_ndvi(self):
        try:
            red_frequency = self._load_image(self.red_path)
            nir_frequency = self._load_image(self.nir10_path)
        except rasterio.errors.RasterioError as e:
            print("something went wrong :(")
            return

        red = red_frequency.read(1).astype(float)
        nir = nir_frequency.read(1).astype(float)

        np.seterr(divide='ignore', invalid='ignore')
        # ndvi = 65536 * np.divide((nir-red),(nir+red)) -> ¿? revisar
        ndvi = np.where((nir - red) == 0., 0, (nir - red) / (nir + red))

        metadata = red_frequency.meta
        metadata.update(dtype=rasterio.float32, count=1, driver="GTiff")

        red_frequency.close()
        nir_frequency.close()

        print("ndvi correctly calculated")
        return ndvi, metadata

    def calculate_ndwi(self):
        swir_frequency = self._load_image(self.swir_path)
        nir_frequency = self._load_image(self.nir20_path)

        swir = swir_frequency.read(1).astype('float64')
        nir = nir_frequency.read(1).astype('float64')

        np.seterr(divide='ignore', invalid='ignore')
        ndwi = 65536 * np.divide((nir - swir), (nir + swir))
        dimensions = np.array([swir_frequency.width, swir_frequency.height, swir_frequency.crs, swir_frequency.transform])

        swir_frequency.close()
        nir_frequency.close()

        return ndwi, dimensions

    def write_ndvi_image(self):
        ndvi, metadata = self.calculate_ndvi()

        with rasterio.open(self.ndvi_path, 'w', **metadata) as temp:
            temp.write_band(1, ndvi.astype(rasterio.float32))
        
        print("image correctly written")

    def write_ndwi_image(self):
        ndwi, dimensions = self.calculate_ndwi()

        ndviImage = rasterio.open(
            self.ndwi_path,
            'w',
            driver='Gtiff',
            width=dimensions[0],
            height=dimensions[1],
            count=1,
            crs=dimensions[2],
            transform=dimensions[3],
            dtype='float64')
        ndviImage.write(ndwi, 1)
        ndviImage.close()

    def plot_ndvi_image(self, plot_name):
        ndviImage = self._load_image(self.ndvi_path)

        plot.show(ndviImage, ' ')
        rasterio.plot.show_hist(ndviImage, bins=1000, masked=True, title=plot_name, ax=None)
        ndviImage.close()

    def plot_ndwi_image(self):
        ndwiImage = self._load_image(self.ndwi_path)
        plot.show(ndwiImage, ' ')
