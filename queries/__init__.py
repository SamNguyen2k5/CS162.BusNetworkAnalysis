"""
Module queries.
Contains:
- Generic ObjectQuery class supporting querying a list of objects with certain criteria.
- Implementation of StopQuery, VariantQuery and PathQuery that inherits from ObjectQuery.
"""
from queries.object_query import ObjectQuery
from queries.stop_query import StopQuery
from queries.variant_query import VariantQuery
from queries.path_query import PathQuery