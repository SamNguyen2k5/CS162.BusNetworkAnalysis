"""
Helper functions to convert from one coordinate reference system (CRS) to another.
"""
import pyproj

wgs84_to_vn2000_transformer = pyproj.Transformer.from_crs('epsg:4326', 'epsg:3405')
vn2000_to_wgs84_transformer = pyproj.Transformer.from_crs('epsg:3405', 'epsg:4326')

def wgs84_to_vn2000(lat: float, lng: float) -> tuple[float, float]:
    """
    Returns the converted Cartesian coordinates in the VN2000 CRS.
    """
    return wgs84_to_vn2000_transformer.transform(lat, lng)

def vn2000_to_wgs84(x: float, y: float) -> tuple[float, float]:
    """
    Returns the converted geographic coordinates in the WGS84 CRS.
    """
    return vn2000_to_wgs84_transformer.transform(x, y)

print(wgs84_to_vn2000_transformer)