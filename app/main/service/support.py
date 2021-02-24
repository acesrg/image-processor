from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.mask import mask
from shapely.geometry import box
from fiona.crs import from_epsg
from pyproj import Transformer
import geopandas as gpd
from pycrs import parse


class Support:
    """
    Clase que tiene todos los métodos de soporte para manipular las imágenes
    """

    def __init__(self):
        pass

    @staticmethod
    def _load_image(path):
        return rasterio.open(path)

    def show_image_coordinates(self, src_path):
        """
        Devuelve las coordenadas en formato estándar (WS-84), apartir de la matriz de afinidad original.
        VORSICHT: Revisar si sigue haciendo falta porque mepa que no
        """
        src = self._load_image(src_path)

        transform_matrix = src.transform

        transformer = Transformer.from_crs("epsg:32720", "epsg:4326")
        return transformer.transform(transform_matrix[2], transform_matrix[5])

    def reprojection(self, src_path, final_crs, final_path):
        """
        Reproyecta una imagen al sistema de coordenadas que se le indique
        """
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

    def crop_raster(self, coordinates, src_path, final_path):
        """
        Recorta la imagen a partir de un par de coordenadas (x,y) determinado.
        VORSICHT: quizás debería agregar el sistema de coordenadas como parámetro.
        Actualmente no está de esa manera porque todas las coordenadas con las que se trabajan son ws84 pero nunca se sabe...
        """
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
