"""
Module queries.stop_query
"""
from typing import Callable, Any

from elements.stop import Stop

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
    
    # Aliases
    search_by_abc = search
