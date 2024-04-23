"""
Module queries.variant_query
"""
from typing import Callable, Any

from elements.variant import Variant

from queries.object_query import ObjectQuery
from queries.variant_query.__mixins__.input import VariantQueryInputMixin

class VariantQuery(ObjectQuery, VariantQueryInputMixin):
    """
    Implementation of ObjectQuery that supports querying Variants. 
    """
    def __init__(self, objs):
        super().__init__(objs=objs, ObjectType=Variant)

    def query(self, pred: Callable[[Variant], bool]) -> 'VariantQuery':
        """
        Queries all Paths satisfying the predicate pred, return as a dictionary.
        """
        return VariantQuery(self.query_to_dict(pred))
    
    def search(self, attr: str, value: Any) -> 'VariantQuery':
        """
        Searches for all Paths with attributes matching value, return as a dictionary.
        """
        return VariantQuery(self.search_to_dict(attr, value))
    
    # Aliases
    search_by_abc = search
