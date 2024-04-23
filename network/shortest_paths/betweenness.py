"""
Module network.shortest_paths.betweenness
"""

from typing import Dict
from tqdm import tqdm

from network.network import Network
from network.shortest_paths.dijkstra import NetworkDijkstra, NetworkDijkstraDescendantsCount

class NetworkAnalysisBetweenness:
    """
    Analyse a network using Betweenness Centrality.
    """
    _scores:     Dict[int, int]
    
    def _from_net_brute_force(self, net: Network, dijkstra_engine: NetworkDijkstra = None):
        if dijkstra_engine is None:
            dijkstra_engine = NetworkDijkstra()

        raw_scores = { node_id: 0 for node_id in net.nodes }

        for src in tqdm(net.nodes):
            dijkstra_engine.from_src(src=src, net=net)
            for dest in net.nodes:
                for connector in dijkstra_engine.reverse_path_from(dest=dest):
                    raw_scores[connector.dest] += 1
                    if connector.src == src:
                        raw_scores[src] += 1

        self._scores = dict(sorted(raw_scores.items(), key=lambda x: x[1], reverse=True))

    def _from_net_shortest_tree(self, net: Network, dijkstra_engine: NetworkDijkstra = None):
        if dijkstra_engine is None:
            dijkstra_engine = NetworkDijkstra()
        dijkstra_counter_engine = NetworkDijkstraDescendantsCount()

        raw_scores = {}
        for src in tqdm(net.nodes):
            dijkstra_engine.from_src(src=src, net=net)
            dijkstra_counter_engine.from_engine(engine=dijkstra_engine)
            for (node_id, added_score) in dijkstra_counter_engine.count_paths.items():
                raw_scores[node_id] = raw_scores.get(node_id, 0) + added_score

        self._scores = dict(sorted(raw_scores.items(), key=lambda x: x[1], reverse=True))

    def from_net(self, net: Network, dijkstra_engine: NetworkDijkstra = None, alg: str = 'tree'):
        """
        Compute the betweenness scores of every node.
            - If alg == ’tree’:
                Run the An improvement to O(V^2 + VElogV) using Shortest-path tree algorithm.
            - Otherwise:
                Run the Naive O(V^2ElogV) algorithm algorithm.
        """
        if alg == 'tree':
            self._from_net_shortest_tree(net=net, dijkstra_engine=dijkstra_engine)
        else:
            self._from_net_brute_force(net=net, dijkstra_engine=dijkstra_engine)

    def top_scores(self, k: int = 10):
        """
        Returns k nodes with largest betweenness score.
        Arguments:
            - k:        the number of returning nodes (default = 10)
        """
        if k < 0:
            raise ValueError('Negative size.')
        if k > len(self._scores):
            raise ValueError('Size larger than original.')

        it = iter(self._scores)
        return [next(it) for _ in range(k)]

    @property
    def scores(self):
        """
        Returns the scores mapping
        """
        return self._scores

    @scores.setter
    def scores(self, value):
        self._scores = value
