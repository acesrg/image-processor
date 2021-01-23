class NormalizedIndexes:
    """
    Represent the normalized difference indexes
    """
    def __init__(self, ndvi, ndwi):
        self.ndvi = ndvi
        self.ndwi = ndwi


class GeographicInformation:
    """
    Represents the geographic information of a given satellite image
    """
    def __init__(self, tag_name, coordinates):
        self.tag_name = tag_name
        self.coordinates = coordinates


class SatelliteImageProcessed:
    """
    Represents the object <Satellite Image> after it is processed
    """
    def __init__(self, file_name, geographic_information, date_time, normalized_indexes):
        self.file_name = file_name
        self.geographic_information = geographic_information
        self.date_time = date_time
        self.normalized_indexes = normalized_indexes
