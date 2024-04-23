"""
Module queries.path_query
"""
from typing import Callable, Any

from elements.path import Path

from queries.object_query import ObjectQuery
from queries.path_query.__mixins__.input import PathQueryInputMixin

class PathQuery(ObjectQuery, PathQueryInputMixin):
    """
    Implementation of ObjectQuery that supports querying Paths. 
    """
    def __init__(self, objs):
        super().__init__(objs=objs, ObjectType=Path)

    def query(self, pred: Callable[[Path], bool]) -> 'PathQuery':
        """
        Queries all Paths satisfying the predicate pred, return as a dictionary.
        """
        return PathQuery(self.query_to_dict(pred))
    
    def search(self, attr: str, value: Any) -> 'PathQuery':
        """
        Searches for all Paths with attributes matching value, return as a dictionary.
        """
        return PathQuery(self.search_to_dict(attr, value))
    
    # Aliases
    search_by_abc = search