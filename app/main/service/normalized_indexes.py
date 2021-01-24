import rasterio
from rasterio import plot
import numpy as np
from pyproj import Transformer

from rasterio.warp import calculate_default_transform, reproject, Resampling

from rasterio.mask import mask
from shapely.geometry import box

import geopandas as gpd
from fiona.crs import from_epsg
from pycrs import parse

import json

from ..model import models

satellite_extensions = {
    'sentinel': '.jp2',
    'landsat8a': '.tif',
}


class NormalizedDifferenceIndex:
    def __init__(self, image_path, satellite):
        self.red_path = image_path + 'red' + satellite_extensions[satellite]
        self.nir10_path = image_path + 'nir_4' + satellite_extensions[satellite]
        self.nir20_path = image_path + 'nir_3' + satellite_extensions[satellite]
        self.swir_path = image_path + 'swir' + satellite_extensions[satellite]

        self.ndvi_path = image_path + 'ndvi.tif'
        self.ndwi_path = image_path + 'ndwi.tif'
        # self.red_path = image_path + 'B4' + satellite_extensions[satellite]

    @staticmethod
    def _load_image(path):
        return rasterio.open(path)

    def calculate_ndvi(self):
        red_frequency = self._load_image(self.red_path)
        nir_frequency = self._load_image(self.nir10_path)

        red = red_frequency.read(1).astype(float)
        nir = nir_frequency.read(1).astype(float)

        np.seterr(divide='ignore', invalid='ignore')
        # ndvi = 65536 * np.divide((nir-red),(nir+red)) -> ¿? revisar
        ndvi = np.where((nir - red) == 0., 0, (nir - red) / (nir + red))

        metadata = red_frequency.meta
        metadata.update(dtype=rasterio.float32, count=1, driver="GTiff")

        red_frequency.close()
        nir_frequency.close()

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

    def write_ndvi_image(self, src_path):

        ndvi, metadata = self.calculate_ndvi()

        with rasterio.open(src_path, 'w', metadata) as temp:
            temp.write_band(1, ndvi.astype(rasterio.float32))

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

    def show_image_coordinates(self, src_path):
        src = self._load_image(src_path)

        # devuelve la matriz de afinidad con las coordenadas correspondientes
        transform_matrix = src.transform

        transformer = Transformer.from_crs("epsg:32720", "epsg:4326")
        return transformer.transform(transform_matrix[2], transform_matrix[5])

    def reprojection(self, src_path, final_crs, final_path):
        src = self._load_image(src_path)

        original_width = src.width
        original_height = src.height

        transform, width, height = calculate_default_transform(src.crs, final_crs, original_width, original_height, *src.bounds)

        kwargs = src.meta.copy()
        kwargs.update({
            'crs': final_crs,
            'transform': transform,
            'width': width,
            'height': height})

        transformed_src = rasterio.open(final_path, 'w', **kwargs)
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(transformed_src, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=final_crs,
                resampling=Resampling.nearest)

    def parse_features(self, geo_dataframe):
        return json.loads(geo_dataframe)

    # el objeto de coordenadas se supone que estÃ¡ escrito en coordenadas ws84 ... creo que no vale la pena parametrizarlo
    def crop_raster(self, coordinates, src_path, final_path):
        src = self._load_image(src_path)

        polygon = box(coordinates[0], coordinates[1], coordinates[2], coordinates[3])
        geo_dataframe = gpd.GeoDataFrame({'geometry': polygon}, index=[0], crs=from_epsg(4326))
        geo_dataframe = geo_dataframe.to_crs(crs=src.crs.data)  # ponele

        polygon_coordinates = [json.loads(geo_dataframe.to_json())['features'][0]['geometry']]

        epsg_code = int(src.crs.data['init'][5:])

        out_img, out_transform = mask(src, shapes=polygon_coordinates, crop=True)

        metadata = src.meta.copy()

        cropped_crs = parse.from_epsg_code(epsg_code).to_proj4()

        metadata.update({"driver": "GTiff",
                         "height": out_img.shape[1],
                         "width": out_img.shape[2],
                         "transform": out_transform,
                         "crs": cropped_crs,
                         "dtype": rasterio.float32})

        with rasterio.open(final_path, "w", **metadata) as dest:
            dest.write(out_img)


class InitInformation:
    """
    Representa toda la informaciÃ³n de la imagen una vez procesada. Es lo que deberÃ­a devolver el POST CalculateNDVI.
    """
    def __init__(self, file_name):
        self.file_name = file_name

    def _init_ndvi(self):
        """
        Returns a NormalizedDifferenceIndex instance
        """
        # TODO paramentrizar el nombre del sate como se hizo en la clase de arriba
        return NormalizedDifferenceIndex(self.file_name, 'sentinel')

    def _init_satellite_image(self):
        ndvi_instance = self._init_ndvi()

        # TODO parametrizar fecha, tag, etc (estos sÃ³lo son datos de prueba)
        date_time = '2012-04-23T18:25:43.511Z'
        geographicInformation = models.GeographicInformation('test_tag', ndvi_instance.show_image_coordinates(self.file_name + 'red.jp2'))

        ndvi, dimensions = ndvi_instance.calculate_ndvi()
        # normalizedIndexes = models.NormalizedIndexes(ndvi.tolist(), 0)

        # temporalmente no muestro los Ã­ndices porque es un array desastroso
        satelliteImageProcessed = models.SatelliteImageProcessed(self.file_name, json.dumps(geographicInformation.__dict__), date_time, 0)

        return satelliteImageProcessed.__dict__
