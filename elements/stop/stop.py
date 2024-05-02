"""
Module elements.stop
"""

from elements.stop.__mixins__.input import StopInputMixin
from elements.stop.__mixins__.output import StopOutputMixin
from helper import wgs84_to_vn2000

class Stop(StopInputMixin, StopOutputMixin):
    """
    Defines places where buses stop temporarily to let passengers get on or off the bus.
    Basic element of a bus network. 
    """

    _stop_id               : int
    _code                  : str
    _name                  : str
    _stop_type             : str
    _zone                  : str 
    _ward                  : str 
    _address_no            : str
    _street                : str 
    _support_disability    : bool
    _status                : str
    _latitude              : float 
    _longtitude            : float 
    _coord                 : tuple[int, int]
    _search                : list[str]
    _routes                : list[str] 

    def __init__(self, StopId, Code, Name, StopType, Zone, Ward, AddressNo, Street, SupportDisability, Status, Lng, Lat, Search, Routes):
        self._stop_id              = StopId
        self._code                 = Code
        self._name                 = Name
        self._stop_type            = StopType
        self._zone                 = Zone
        self._ward                 = Ward
        self._address_no           = AddressNo
        self._street               = Street
        self._support_disability   = (SupportDisability == 'Có')
        self._status               = Status
        self._latitude             = Lat
        self._longtitude           = Lng
        self._coord                = wgs84_to_vn2000(Lat, Lng)
        self._search               = list(map(lambda token: token.strip(), Search.split(' ')))
        self._routes               = list(map(lambda token: token.strip(), Routes.split(',')))

    def __repr__(self):
        return StopOutputMixin.to_string(self)

    @property
    def stop_id(self) -> int:
        """
        Returns StopId
        """
        return self._stop_id

    @stop_id.setter
    def stop_id(self, value):
        self._stop_id = value

    @property
    def code(self) -> str:
        """
        Returns Code
        """
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def name(self) -> str:
        """
        Returns Name
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def stop_type(self) -> str:
        """
        Returns StopType
        """
        return self._stop_type

    @stop_type.setter
    def stop_type(self, value):
        self._stop_type = value

    @property
    def zone(self) -> str:
        """
        Returns Zone
        """
        return self._zone

    @zone.setter
    def zone(self, value):
        self._zone = value

    @property
    def ward(self) -> str:
        """
        Returns Ward
        """
        return self._ward

    @ward.setter
    def ward(self, value):
        self._ward = value

    @property
    def address_no(self) -> str:
        """
        Returns AddressNo
        """
        return self._address_no

    @address_no.setter
    def address_no(self, value):
        self._address_no = value

    @property
    def street(self) -> str:
        """
        Returns Street
        """
        return self._street

    @street.setter
    def street(self, value):
        self._street = value

    @property
    def support_disability(self) -> bool:
        """
        Returns SupportDisability
        """
        return self._support_disability

    @support_disability.setter
    def support_disability(self, value):
        self._support_disability = value

    @property
    def status(self) -> str:
        """
        Returns Status
        """
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def latitude(self) -> float:
        """
        Returns Latitude
        """
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = value

    @property
    def longtitude(self) -> float:
        """
        Returns Longtitude
        """
        return self._longtitude

    @longtitude.setter
    def longtitude(self, value):
        self._longtitude = value

    @property
    def coord(self) -> tuple[int, int]:
        """
        Returns the Cartesian coordinates of the Stop in WGS84 CRS.
        """
        return self._coord
    
    @coord.setter
    def coord(self, value):
        self._coord = value

    @property
    def search(self) -> list[str]:
        """
        Returns Search tokens
        """
        return self._search

    @search.setter
    def search(self, value):
        self._search = value

    @property
    def routes(self):
        """
        Returns the list of routes passing the Stop
        """
        return self._routes

    @routes.setter
    def routes(self, value):
        self._routes = value

