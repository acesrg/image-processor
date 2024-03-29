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
# You should have received a copy of the GNU General Public Licens
# along with this program. If not, see <http://www.gnu.org/licenses/>.#

from s2cloudless import S2PixelCloudDetector
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
import scipy.ndimage
from safo_impro.logger.log_config import LogConfig


class CloudFilter:
    def __init__(self, images_path):
        self.images_path = images_path
        self.logger = LogConfig().get_logger()

    @staticmethod
    def _calculate_bands_array(self):
        self.logger.info("calculating bands array")

        with rasterio.open(self.images_path + 'blue_coast_443_60.jp2') as scl:
            B01 = scl.read()
            tmparr = np.empty_like(B01)
            aff = scl.transform

        with rasterio.open(self.images_path + 'blue_492_10.jp2') as scl:
            B02 = scl.read()
            reproject(
                B02, tmparr,
                src_transform=scl.transform,
                dst_transform=aff,
                src_crs=scl.crs,
                dst_crs=scl.crs,
                resampling=Resampling.bilinear)
            B02 = tmparr

        with rasterio.open(self.images_path + 'red_665_10.jp2') as scl:
            B04 = scl.read()
            reproject(
                B04, tmparr,
                src_transform=scl.transform,
                dst_transform=aff,
                src_crs=scl.crs,
                dst_crs=scl.crs,
                resampling=Resampling.bilinear)
            B04 = tmparr

        with rasterio.open(self.images_path + 'nir_705_20.jp2') as scl:
            B05 = scl.read()
            reproject(
                B05, tmparr,
                src_transform=scl.transform,
                dst_transform=aff,
                src_crs=scl.crs,
                dst_crs=scl.crs,
                resampling=Resampling.bilinear)
            B05 = tmparr

        with rasterio.open(self.images_path + 'nir4_832_10.jp2') as scl:
            B08 = scl.read()
            reproject(
                B08, tmparr,
                src_transform=scl.transform,
                dst_transform=aff,
                src_crs=scl.crs,
                dst_crs=scl.crs,
                resampling=Resampling.bilinear)
            B08 = tmparr

        with rasterio.open(self.images_path + 'nir4a_865_20.jp2') as scl:
            B8A = scl.read()
            reproject(
                B8A, tmparr,
                src_transform=scl.transform,
                dst_transform=aff,
                src_crs=scl.crs,
                dst_crs=scl.crs,
                resampling=Resampling.bilinear)
            B8A = tmparr

        with rasterio.open(self.images_path + 'swir_945_60.jp2') as scl:
            B09 = scl.read()

        with rasterio.open(self.images_path + 'swir2_1373_60.jp2') as scl:
            B10 = scl.read()

        with rasterio.open(self.images_path + 'swir3_1614_20.jp2') as scl:
            B11 = scl.read()
            reproject(
                B11, tmparr,
                src_transform=scl.transform,
                dst_transform=aff,
                src_crs=scl.crs,
                dst_crs=scl.crs,
                resampling=Resampling.bilinear)
            B11 = tmparr

        with rasterio.open(self.images_path + 'swir4_2202_20.jp2') as scl:
            B12 = scl.read()
            reproject(
                B12, tmparr,
                src_transform=scl.transform,
                dst_transform=aff,
                src_crs=scl.crs,
                dst_crs=scl.crs,
                resampling=Resampling.bilinear)
            B12 = tmparr

        bands = np.array([np.dstack((B01[0] / 10000.0, B02[0] / 10000.0,
                                    B04[0] / 10000.0, B05[0] / 10000.0,
                                    B08[0] / 10000.0, B8A[0] / 10000.0,
                                    B09[0] / 10000.0, B10[0] / 10000.0,
                                    B11[0] / 10000.0, B12[0] / 10000.0))])
        return bands

    def calculate_cloud_mask(self, operation):
        bands_array = self._calculate_bands_array(self)
        cloud_detector = S2PixelCloudDetector(
            threshold=0.4, average_over=4, dilation_size=2, all_bands=False)

        self.logger.info("calculating the cloud mask ")
        # cloud_prob = cloud_detector.get_cloud_probability_maps(bands_array)
        cloud_mask = cloud_detector.get_cloud_masks(bands_array)

        zoom = 6
        if operation == "NDWI":
            zoom = 3

        resized_mask = scipy.ndimage.zoom(cloud_mask[0], zoom, mode='nearest')
        temp = np.multiply(resized_mask, -1)

        resized_mask_invertida = np.add(temp, 1)

        return resized_mask_invertida
