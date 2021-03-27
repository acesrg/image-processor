import rasterio
from rasterio import plot
import numpy as np
import os

satellite_extensions = {
    'sentinel': '.jp2',
    'landsat8a': '.tif',
}


class NormalizedDifferenceIndex:
    def __init__(self, image_path, satellite):
        self.red_path = image_path + 'red_665_10' + satellite_extensions[satellite]
        self.green_path = image_path + 'green_560_10' + satellite_extensions[satellite]
        self.nir10_path = image_path + 'nir4_832_10' + satellite_extensions[satellite]

        self.nir20_path = image_path + 'nir4a_865_20' + satellite_extensions[satellite]
        self.swir_path = image_path + 'swir3_1614_20' + satellite_extensions[satellite]

        self.ndvi_path = image_path + 'ndvi.tif'
        self.ndwi_vegetation_path = image_path + 'ndwi_vegetation.tif'
        self.ndwi_water_path = image_path + 'ndwi_water_bodies.tif'

    @staticmethod
    def _load_image(src_path):
        if os.path.isfile(src_path) is True:
            return rasterio.open(src_path)
        else:
            print("no such file " + src_path)

    def calculate_ndvi(self):
        try:
            red_frequency = self._load_image(self.red_path)
            nir_frequency = self._load_image(self.nir10_path)
        except rasterio.errors.RasterioError:
            print("something went wrong :(")
            return

        red = red_frequency.read(1).astype(float)
        nir = nir_frequency.read(1).astype(float)

        np.seterr(divide='ignore', invalid='ignore')
        ndvi = np.where((nir - red) == 0., 0, (nir - red) / (nir + red))

        metadata = red_frequency.meta
        metadata.update(dtype=rasterio.float32, count=1, driver="GTiff")

        red_frequency.close()
        nir_frequency.close()

        print("ndvi correctly calculated")
        return ndvi, metadata

    def calculate_ndwi_vegetation(self):
        try:
            swir_frequency = self._load_image(self.swir_path)
            nir_frequency = self._load_image(self.nir20_path)
        except rasterio.errors.RasterioError:
            print("something went wrong :(")
            return

        swir = swir_frequency.read().astype('float64')
        nir = nir_frequency.read().astype('float64')

        np.seterr(divide='ignore', invalid='ignore')
        ndwi_vegetation = np.where((nir - swir) == 0., 0, (nir - swir) / (nir + swir))  # water content in vegetation

        metadata = swir_frequency.meta
        metadata.update(dtype=rasterio.float32, count=1, driver="GTiff")

        swir_frequency.close()
        nir_frequency.close()

        print("ndwi for vegetation correctly calculated")
        return ndwi_vegetation, metadata

    def write_new_raster(self, type):
        if type == "ndvi":
            output, metadata = self.calculate_ndvi()
        elif type == "ndwi_vegetation":
            output, metadata = self.calculate_ndwi_vegetation()
        else:
            print("invalid operation, try again")
            return

        output_path = self.image_path + type + ".tif"

        with rasterio.open(output_path, 'w', **metadata) as temp:
            temp.write_band(1, output.astype(rasterio.float32))

        print("image correctly written: " + output_path)

    def plot_ndvi_image(self, plot_name):
        ndviImage = self._load_image(self.ndvi_path)

        plot.show(ndviImage, ' ')
        rasterio.plot.show_hist(ndviImage, bins=1000, masked=True, title=plot_name, ax=None)
        ndviImage.close()

    def plot_ndwi_image(self):
        ndwiImage = self._load_image(self.ndwi_path)
        plot.show(ndwiImage, ' ')
