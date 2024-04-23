"""
Module elements.variant
"""

from elements.variant.__mixins__.input import VariantInputMixin
from elements.variant.__mixins__.output import VariantOutputMixin

class Variant(VariantInputMixin, VariantOutputMixin):
    """
    Representing bus routes in a specific direction. 
    A bus route has two variants, outbound and inbound. Some bus routes may only have one variant.
    """
    _number: str = ""
    _start_stop: str = ""
    _end_stop: str = ""
    _outbound: bool

    _name: str
    _short_name: str
    _distance: int
    _running_time: int
    _route_ids: tuple[int, int]

    def __init__(
        self, RouteId, RouteVarId, RouteVarName, RouteVarShortName, RouteNo, 
        StartStop, EndStop, Distance, Outbound, RunningTime
    ) -> None:
        self._number                = RouteNo
        self._start_stop            = StartStop
        self._end_stop              = EndStop
        self._outbound              = Outbound

        self._name                  = RouteVarName
        self._short_name            = RouteVarShortName
        self._distance              = Distance
        self._running_time          = RunningTime
        self._route_ids             = (int(RouteId), int(RouteVarId))

    def __repr__(self) -> str:
        return VariantOutputMixin.to_string(self)

    # ------------- Getters & Setters --------------
    
    @property
    def number(self) -> str:
        """
        Returns the number of the bus variant. Must be of str type to store values such as '61-1', 'D2'.
        """
        return self._number

    @number.setter
    def number(self, value):
        self._number = value

    @property
    def start_stop(self) -> str:
        """
        Returns the starting stop of the variant
        """
        return self._start_stop

    @start_stop.setter
    def start_stop(self, value):
        self._start_stop = value

    @property
    def end_stop(self) -> str:
        """
        Returns the ending stop of the variant
        """
        return self._end_stop

    @end_stop.setter
    def end_stop(self, value):
        self._end_stop = value

    @property
    def name(self) -> str:
        """
        Returns the name of the variant
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def short_name(self) -> str:
        """
        Returns the shortened name of the variant
        """
        return self._short_name

    @short_name.setter
    def short_name(self, value):
        self._short_name = value

    @property
    def distance(self) -> float:
        """
        Returns the total travelling distance of the variant
        """
        return self._distance

    @distance.setter
    def distance(self, value):
        self._distance = value

    @property
    def running_time(self) -> float:
        """
        Returns the total travelling time of the variant
        """
        return self._running_time

    @running_time.setter
    def running_time(self, value):
        self._running_time = value

    @property
    def route_ids(self) -> int:
        """
        Returns a tuple of RouteId and RouteVarId.
        """
        return self._route_ids

    @route_ids.setter
    def route_ids(self, value):
        self._route_ids = value
    
    @property
    def route_id(self) -> int:
        """
        Returns RouteId.
        """
        return self._route_ids[0]

    @property
    def route_var_id(self):
        """
        Returns RouteVarId.
        """
        return self._route_ids[1]
