"""
Output mixins for the Variant class
"""
from typing import Any
import json

from helper import wrapping_box

class VariantOutputMixin:
    """
    Output mixins for the Variant class
    """
    def to_string(self) -> str:
        """
        Display information of a Variant in a string format.
        This function is called by __repr__().
        """
        return wrapping_box(
            title='Route {}, {} -> {}'.format(self._number, self._start_stop, self._end_stop),
            obj=self.to_dict(),
            MAX_LENGTH=100
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert Variant to a Python dictionary.
        """
        obj = {
            'RouteNo': self._number,
            'StartStop': self._start_stop,
            'EndStop': self._end_stop,
            'Name': self._name,
            'ShortName': self._short_name,
            'Distance':  self._distance,
            'RunningTime':  self._running_time,
            'RouteIds': self._route_ids
        }

        return obj

    def to_json(self, file: str):
        """
        Export Variant information to JSON file. 
        The function calls to_dict() to convert Variant to a dictionary, then dumps it into a JSON file.
        """
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False)
