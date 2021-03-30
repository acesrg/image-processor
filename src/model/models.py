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
