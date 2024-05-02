"""
module chatter.tools.predicate.zone
"""
from langchain.tools import tool

@tool
def is_stop_in_zone(stop_zone_name: str, target_zone_name: str):
    """
    Compares if a Stop is in the intended zone.
    Arguments:
    - stop_zone_name:       The zone name of the Stop to be tested
    - target_zone_name:     The zone name in query
    """
    return stop_zone_name == target_zone_name