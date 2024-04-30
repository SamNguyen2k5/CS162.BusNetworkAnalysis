"""
module chatter
"""

from langchain.tools import tool
from queries import StopQuery, VariantQuery, PathQuery

def load(_stops: StopQuery):
    global stops
    stops = _stops

@tool
def search_stop(attr: str, value: str | int) -> StopQuery:
    """
    Search for stops with attribute attr containing the given value.
    - attr:     Attribute to be queried.
    - value:    Target value for the attribute.
    """
    print('Called search_stops on attr={}, value={}'.format(attr, value))
    return stops.search_approx(attr, value)
    
