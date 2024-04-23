"""
Module elements.path
"""

from elements.path.__mixins__.input import PathInputMixin
from elements.path.__mixins__.output import PathOutputMixin

from helper import wgs84_to_vn2000

class Path(PathInputMixin, PathOutputMixin):
    """
    Representing a specific path of a bus variant in the form of a LineString.
    """
    _route_ids: tuple[int, int]
    _coords: list[tuple[float, float]]

    def __init__(self, lat: list[float], lng: list[float], RouteId, RouteVarId) -> None: 
        self._coords = list(wgs84_to_vn2000(lat0, lng0) for (lat0, lng0) in zip(lat, lng))
        self._route_ids = (int(RouteId), int(RouteVarId))

    def __repr__(self) -> str:
        return PathOutputMixin.to_string(self)
   
    def polysides(self):
        """
        Return an Iterable of tuples of coordinates, representing each segments of the LineString.
        """
        return zip(self._coords, self._coords[1:])
 
    @property
    def route_ids(self) -> tuple[int, int]:
        """
        Returns a tuple of RouteId and RouteVarId.
        """
        return self._route_ids

    @route_ids.setter
    def route_ids(self, value):
        self._route_ids = value

    @property
    def coords(self) -> tuple:
        """
        Returns the Cartesian coordinates of the points on the LineString.
        """
        return self._coords

    @coords.setter
    def coords(self, value):
        self._coords = value

    @property
    def route_id(self):
        """
        Returns RouteId
        """
        return self._route_ids[0]

    @property
    def route_var_id(self):
        """
        Returns RouteVarId.
        """
        return self._route_ids[1]