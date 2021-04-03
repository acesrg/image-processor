#
# Copyright (c) 2021 PAULA B. OLMEDO.
#
# This file is part of IMAGE_PROCESSOR
# (see https://github.com/paulaolmedo/image-processor).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.#
import rasterio
from rasterio import plot
import numpy as np
import os
from cloud_filter import CloudFilter

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
        self.cloud_filter = CloudFilter(image_path)
        self.image_path = image_path

    @staticmethod
    def _load_image(src_path):
        if os.path.isfile(src_path) is True:
            return rasterio.open(src_path)
        else:
            print("no such file " + src_path)

    @staticmethod
    def _calculate_ndvi(self):
        try:
            red_frequency = self._load_image(self.red_path)
            nir_frequency = self._load_image(self.nir10_path)
        except rasterio.errors.RasterioError:
            print("something went wrong :(")
            return

        red = red_frequency.read(1).astype(float)
        nir = nir_frequency.read(1).astype(float)

        cloud_mask = self.cloud_filter.calculate_cloud_mask()

        red_masked = np.multiply(cloud_mask, red)
        nir_masked = np.multiply(cloud_mask, nir)

        np.seterr(divide='ignore', invalid='ignore')
        ndvi = np.where((nir_masked - red_masked) == 0., 0, (nir_masked - red_masked) / (nir_masked + red_masked))

        metadata = red_frequency.meta
        metadata.update(dtype=rasterio.float32, count=1, driver="GTiff")

        red_frequency.close()
        nir_frequency.close()

        print("ndvi correctly calculated")
        return ndvi, metadata

    @staticmethod
    def _calculate_ndwi_vegetation(self):
        try:
            swir_frequency = self._load_image(self.swir_path)
            nir_frequency = self._load_image(self.nir20_path)
        except rasterio.errors.RasterioError:
            print("something went wrong :(")
            return

        swir = swir_frequency.read().astype('float64')
        nir = nir_frequency.read().astype('float64')

        cloud_mask = self.cloud_filter.calculate_cloud_mask()

        swir_masked = np.multiply(cloud_mask, swir)
        nir_masked = np.multiply(cloud_mask, nir)

        np.seterr(divide='ignore', invalid='ignore')
        ndwi_vegetation = np.where((nir - swir) == 0., 0, (nir - swir) / (nir + swir))  # water content in vegetation

        metadata = swir_frequency.meta
        metadata.update(dtype=rasterio.float32, count=1, driver="GTiff")

        swir_frequency.close()
        nir_frequency.close()

        print("ndwi for vegetation correctly calculated")
        return ndwi_vegetation, metadata

    def write_new_raster(self, operation_type):
        if operation_type == "ndvi":
            output, metadata = self._calculate_ndvi()
        elif operation_type == "ndwi_vegetation":
            output, metadata = self._calculate_ndwi_vegetation()
        else:
            print("invalid operation, try again")
            return

        output_path = self.image_path + operation_type + ".tif"

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
