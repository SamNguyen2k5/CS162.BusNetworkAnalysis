"""
Module queries.stop_query
"""
from typing import Callable, Any

import pandas as pd
from elements.stop import Stop

from helper import wgs84_to_vn2000
from queries.object_query import ObjectQuery
from queries.stop_query.__mixins__.input import StopQueryInputMixin

class StopQuery(ObjectQuery, StopQueryInputMixin):
    """
    Implementation of StopQuery that supports querying Stops. 
    """
    def __init__(self, objs):
        super().__init__(objs=objs, ObjectType=Stop)

    def query(self, pred: Callable[[Stop], bool]) -> 'StopQuery':
        """
        Queries all Stops satisfying the predicate pred, return as a dictionary.
        """
        return StopQuery(self.query_to_dict(pred))
    
    def search(self, attr: str, value: Any) -> 'StopQuery':
        """
        Searches for all Stops with attributes matching value, return as a dictionary.
        """
        return StopQuery(self.search_to_dict(attr, value))
    
    def to_pandas(self, has_cartesian: bool = False, **kwargs) -> pd.DataFrame:
        def mod_row(row: pd.Series) -> pd.Series:
            # pylint: disable=unpacking-non-sequence
            if has_cartesian:
                row['coord_x'], row['coord_y'] = wgs84_to_vn2000(row['Lat'], row['Lng'])

            return row

        return super().to_pandas().apply(mod_row, axis=1)
    
    # Aliases
    search_by_abc = search
