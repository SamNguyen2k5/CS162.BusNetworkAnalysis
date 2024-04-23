"""
Input mixins for the StopQuery class
"""
import ndjson
from elements.stop import Stop

class StopQueryInputMixin:
    """
    Input mixins for the StopQuery class
    """
    @classmethod
    def from_ndjson(cls, file: str = 'stops.json'):
        """
        Import a list of Stops into a StopQuery object.
        """
        stops = {}
        with open(file, 'r', encoding='utf-8') as f:
            obj = ndjson.load(f)
            for route in obj:
                for stop in route['Stops']:
                    stop_id = int(stop['StopId'])
                    if stops.get(stop_id) == None:
                        stops[stop_id] = Stop.from_dict(stop)

            return cls(stops)