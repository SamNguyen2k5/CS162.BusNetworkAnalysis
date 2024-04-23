from queue import PriorityQueue
from typing import Dict
from network import Network

class NetworkDijkstra:
    """
    Implementation of the Dijkstra algorithm.
    """
    _net:       Network
    _src:       int
    _dists:     Dict[int, float]
    _pars:      Dict[int, int]
    _INFINITY:  float
    _pq:        PriorityQueue

    @property
    def _is_terminated(self):
        return False

    def _update_per_iteration(self):
        return

    def from_src(self, net: Network, src: int, INITIAL: float = 0, INFINITY: float = float('inf')):
        """
        Runs Dijkstra from source src.
        """
        self._net = net
        self._src = src
        self._INFINITY = INFINITY

        self._dists = {}
        self._pars = {}

        self._dists[src] = INITIAL
        self._pq = PriorityQueue()
        self._pq.put((0, src))

        while not self._pq.empty():
            if self._is_terminated:
                break
            self._update_per_iteration()

            dist_u, u = self._pq.get()
            if dist_u != self._dists.get(u, self._INFINITY):
                continue

            for connector in net.adjs[u]:
                v, w = connector.dest, connector.weight
                if self._dists.get(v, self._INFINITY) > dist_u + w:
                    self._dists[v] = dist_u + w
                    self._pars[v] = connector
                    self._pq.put((self._dists[v], v))

        return self

    def reverse_path_from(self, dest: int):
        """
        Returns the reversed shortest path to destination dest.
        """
        if self._dists.get(dest) is None:
            return

        while dest != self._src:
            connector = self._pars[dest]
            yield connector
            dest = connector.src

    def path_to(self, dest: int):
        """
        Returns the shortest path to destination dest.
        """
        return reversed(list(self.reverse_path_from(dest=dest)))

    @property
    def INFINITY(self):
        """
        Returns the INFINITY constant used in the algorithm.
        """
        return self._INFINITY

    @property
    def src(self):
        """
        Returns the source from which the algorithm runs.
        """
        return self._src

    @property
    def dists(self):
        """
        Returns the distance array after the algorithm execution.
        """
        return self._dists

    @property
    def pars(self):
        """
        Returns the parents array after the algorithm execution.
        """
        return self._pars

    @property
    def search_space(self) -> Dict[int, float]:
        """
        Returns the search space after the algorithm execution.
        """
        return {
            node: d_node
            for (node, d_node) in self._dists.items()
            if d_node != self._INFINITY
        }
    
class NetworkDijkstraSingleDestination(NetworkDijkstra):
    """
    Augmentation of the Dijkstra algorithm.
    Termination after destination reached.
    """
    _dest:              int

    def __init__(self, dest: int):
        self._dest = dest

    @property
    def _is_terminated(self):
        return self._pq.queue[0][1] == self._dest
    
    def _update_per_iteration(self):
        return
    
class NetworkDijkstraLocalSteps(NetworkDijkstra):
    """
    Augmentation of the Dijkstra algorithm.
    Termination after a specified number of iterations reached.
    """
    _counter:           int
    _steps_limit:       int

    def __init__(self, limit: int):
        self._counter = 0
        self._steps_limit = limit

    @property
    def _is_terminated(self):
        return self._counter >= self._steps_limit
    
    def _update_per_iteration(self):
        self._counter += 1
    
class NetworkDijkstraLocalDistance(NetworkDijkstra):
    """
    Augmentation of the Dijkstra algorithm.
    Search only for local nodes within a specified radius.
    """
    _distance_limit:     int

    def __init__(self, limit: float):
        self._distance_limit = limit

    @property
    def _is_terminated(self):
        return self._pq.queue[0][0] >= self._distance_limit
    
class NetworkDijkstraDescendantsCount:
    """
    Implementation of the Shortest-path Tree.
    Supports counting the descendants of any node.
    """
    _cnt_c:     Dict[int, int]
    
    def from_engine(self, engine: NetworkDijkstra):
        """
        Build the Shortest-path Tree from a precomputed Dijkstra engine.
        """
        self._cnt_c = {}

        for u, dist_u in sorted(engine.dists.items(), key=lambda elem: elem[1], reverse=True):
            if dist_u >= engine.INFINITY:
                continue

            self._cnt_c[u] = self._cnt_c.get(u, 0) + 1
            if u != engine.src:
                v = engine.pars[u].src
                self._cnt_c[v] = self._cnt_c.get(v, 0) + self._cnt_c[u]

        return self

    @property
    def count_paths(self):
        """
        Returns the mapping from a node to its descendants count.
        """
        return self._cnt_c