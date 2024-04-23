import random, math, copy

import pandas as pd
import plotly.express as px
from tqdm import tqdm

from elements import Stop
from queries import StopQuery

from network import BusNetwork
from network.shortest_paths import NetworkBidirectionalDijkstra
from network.shortest_paths import NetworkAnalysisBetweenness
from network.shortest_paths import NetworkSpatialAStar
from network.shortest_paths.contraction_hierarchies \
    import NetworkContractionHierarchiesPeriodicED, NetworkContractionHierarchiesLazyED

if __name__ == '__main__':
    stops = StopQuery.from_ndjson()
    net = BusNetwork.from_json()
    analysis = NetworkAnalysisBetweenness()

    SRC, DEST = 2889, 2330

    dijkstra = NetworkBidirectionalDijkstra.from_net(net=net)
    dist, path = dijkstra.path(SRC, DEST)

    a_star = NetworkSpatialAStar.from_net(net=net)
    dist2, path2 = a_star.path(SRC, DEST)

    # ch = NetworkContractionHierarchiesPeriodicED.from_net(net, update_every_after = 250, local_steps = 50)
    ch = NetworkContractionHierarchiesLazyED.from_net(net, local_steps = 10)
    print('# of shortcuts: {}'.format(ch.no_shortcuts))

    dist3, path3 = ch.path(SRC, DEST)
    print(dist)
    print(dist2)
    print(dist3)