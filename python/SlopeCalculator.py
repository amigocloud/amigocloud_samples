import math
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.wkb import loads
import requests
from PIL import Image
import os
import numpy as np
from numpy import sqrt, pi, arctan, gradient


class SlopeCalculator:
    """
    Class SlopeCalculator calculates an average slope for a given geometry
    Usage:
        sc = SlopeCalculator(token=<token>)
        slope = sc.get_slope(level=13, wkb_geometry="0106000020E61000000100000001030000000100000005000000000000C0B27D5EC0619D837BD7CA424000000008E47C5EC0B9608A43BFCB4240FFFFFFC77E7C5EC0AB7409088ACA424000000028877D5EC0745B40F0FBC94240000000C0B27D5EC0619D837BD7CA4240")
    """
    def __init__(self, token, url="https://cdnamigocloud.global.ssl.fastly.net/api/v1/base_layers/1/tiles/", temp_data_dir="./data/"):
        """
        :param token: AmigoCloud API token
        :param url: path to elevation tiles: 256x256, uint16 per pixel
        :param temp_data_dir: path where downloaded tiles are placed
        """
        self.geometry = None
        self.baselayer_url = url
        self.token = token
        self.temp_data_dir = temp_data_dir
        if not os.path.exists(self.temp_data_dir):
            os.makedirs(self.temp_data_dir)

    def get_slope(self, level, wkb_geometry):
        """
        Calculates an average slope for geometry, using elevation data for a given level

        :param level: level of the elevation data
        :param wkb_geometry:
        :return: average slope
        """
        self.geometry = loads(wkb_geometry, hex=True)
        bounds = self.geometry.bounds  # geometry's bounding box
        # Calculate row/col for the tiles intersecting the geometry
        tlt = self.deg2num(bounds[1], bounds[0], level)
        trb = self.deg2num(bounds[3], bounds[2], level)
        average_slope = 0.0
        min_r = min(tlt[0], trb[0])
        min_c = min(tlt[1], trb[1])
        max_r = max(tlt[0], trb[0])
        max_c = max(tlt[1], trb[1])
        counter = 0
        # Loop through tiles of bounding box of geometry
        for c in range(min_c, max_c+1):
            for r in range(min_r, max_r+1):
                if self.is_tile_in_polygon(r, c, level):
                    self.download_tile(r, c, level)
                    slope = self.get_tile_slope(r, c, level)
                    average_slope += slope
                    counter += 1
        if counter > 0:
            average_slope = average_slope / counter
        return average_slope

    def download_tile(self, row, col, level):
        """
        Download PNG tile for given row/col/level and save it to a file
        """
        url = self.baselayer_url + str(level) + "/" + str(row) + "/" + str(col) + ".png?srs=3857"
        tile = self.get_tile(url)
        fh = open(self.get_filename(row, col, level) + ".png", 'w')
        fh.write(tile)
        fh.close()

    def get_tile_slope(self, row, col, level):
        """
        Load PNG elevation tile into an array, calculate a slope.
        :param row:
        :param col:
        :param level:
        :return: an average slope for an intersection of tile with geometry
        """
        img = Image.open(self.get_filename(row, col, level) + ".png")
        arr = np.array(img)
        x, y = gradient(arr)
        #  Slope in radians
        slope = arctan(sqrt(x * x + y * y))
        tile_slope = self.traverse_tile(row, col, level, slope)
        return tile_slope

    def traverse_tile(self, row, col, level, slope_array):
        """
        Traverse a tile pixels and calculate an average slope for pixels that are inside a geometry polygon
        :param row:
        :param col:
        :param level:
        :param slope_array:
        :return tile_slope:
        """
        lat0, lng0 = self.num2deg(row, col, level)
        lat1, lng1 = self.num2deg(row+1, col+1, level)
        d_lat = abs(lat1 - lat0) / 256
        d_lng = abs(lng1 - lng0) / 256
        tile_slope = 0.0
        counter = 0
        for x in range(0, 256):
            for y in range(0, 256):
                p = Point(min(lng0, lng1)+x*d_lng, min(lat0, lat1)+y*d_lat)
                if self.geometry.contains(p):
                    tile_slope += slope_array[y, x]
                    counter += 1
        if counter > 0:
            tile_slope = tile_slope / counter
        # Save slope image to tiff file
        im = Image.fromarray(slope_array)
        im.save(self.get_filename(row, col, level) + ".tiff")
        return tile_slope

    def get_filename(self, row, col, level):
        """
        Get a unique file name for a tile
        :param row:
        :param col:
        :param level:
        :return:
        """
        # return self.temp_data_dir + str(level) + "_" + str(row) + "_" + str(col)
        return self.temp_data_dir + "current_tile"

    def get_tile(self, url):
        """
        Download a tile from AmigoCloud backend
        :param url:
        :return:
        """
        params = {}
        if self.token:
            params.setdefault('token', self.token)
        response = requests.get(url, params=params, stream=False)
        self.check_for_errors(response)
        return response.content

    def check_for_errors(self, response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            print(exc.message, exc.response)

    def is_tile_in_polygon(self, row, col, level):
        """
        Check if tile is intersects with geometry polygon
        :param row:
        :param col:
        :param level:
        :return:
        """
        lat0, lng0 = self.num2deg(row, col, level)
        lat1, lng1 = self.num2deg(row+1, col+1, level)
        bb = Polygon([[lng0, lat0], [lng1, lat0], [lng1, lat1], [lng0, lat1]])
        return self.geometry.intersects(bb)

    def deg2num(self, lat_deg, lon_deg, zoom):
        """
        Calculate tile index from lat/lon/ zoom level
        :param lat_deg:
        :param lon_deg:
        :param zoom:
        :return:
        """
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
        return xtile, ytile

    def num2deg(self, xtile, ytile, zoom):
        """
        Calculate tile lat/lon from x/y/level
        :param xtile:
        :param ytile:
        :param zoom:
        :return:
        """
        n = 2.0 ** zoom
        lon_deg = xtile / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
        lat_deg = math.degrees(lat_rad)
        return lat_deg, lon_deg
