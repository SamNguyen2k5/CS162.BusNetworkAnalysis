"""
module chatter.tools.shortest_path
"""

from typing import Dict

from langchain.tools import tool
from pydantic import BaseModel, Field

from network.bus import BusNetwork
from network.shortest_paths.contraction_hierarchies import NetworkContractionHierarchiesLazyED

net: BusNetwork
ch_model: NetworkContractionHierarchiesLazyED = None

def load_net(_net: BusNetwork):
    """
    Load network.
    """
    global net
    net = _net

    # pylint: disable=E0001, W0603
    global ch_model
    ch_model = NetworkContractionHierarchiesLazyED.from_net(net=net)

# class DistanceToOneInputModel(BaseModel):
#     """
#     Pydantic input model for distance_to_one tool
#     """
#     s:    str = Field(value='0', description='ID of the source node')
#     t:    str = Field(value='0', description='ID of the destination node')

# @tool(args_schema=DistanceToOneInputModel)
@tool
def distance_to_one(s: int, t: int) -> float:
    """
    Find the shortest distance between node src and node dest.
    Arguments:
    * s:    ID of the source node
    * t:    ID of the destination node
    """
    return ch_model.dist(s, t)