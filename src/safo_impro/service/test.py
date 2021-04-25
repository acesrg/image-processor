#from normalized_indexes import NormalizedDifferenceIndex
import rasterio
from rasterio.mask import mask
import numpy as np
#source = '/Volumes/MM/2020/2020_01/Sentinel-2/unzipped/MSIL1C_20200105.SAFE/GRANULE/MSIL1C_20200105/IMG_DATA'
#ndvi = NormalizedDifferenceIndex(source, 'sentinel')
#ndvi.write_new_raster('ndvi')

import geopandas as gpd
import shapefile as sf

images_path = "src/"
ndvirep_raster = rasterio.open(images_path + 'ndvi-reprojected.tif')
graticules = gpd.read_file(images_path + 'custom_coordinates.shp')
graticules = graticules[["gid", "geometry"]]

def derive_stats(geom, data, **mask_kw):    
    masked, mask_transform = mask(dataset=data, shapes=(geom,),crop=True, all_touched=True, filled=True)
    return masked

graticules['mean_ndvi'] = graticules.geometry.apply(derive_stats, data=ndvirep_raster).apply(np.mean)
graticules['max_ndvi'] = graticules.geometry.apply(derive_stats, data=ndvirep_raster).apply(np.max)
graticules['min_ndvi'] = graticules.geometry.apply(derive_stats, data=ndvirep_raster).apply(np.min)
graticules['median_ndvi'] = graticules.geometry.apply(derive_stats, data=ndvirep_raster).apply(np.median)

r = sf.Reader(images_path + 'custom_coordinates.shp', encoding="ISO8859-1")

coordinates = []
for shaperec in r.iterShapeRecords():
    #shapes = test.shapes()
    bbox = shaperec.shape.bbox #devuelve un objeto determinado
    coordinates.append(bbox)
    
graticules['coordinates'] = coordinates

graticules = graticules[["gid", "coordinates", "mean_ndvi", "max_ndvi", "min_ndvi", "median_ndvi"]]
graticules.to_csv(images_path + "processing_results.csv")
