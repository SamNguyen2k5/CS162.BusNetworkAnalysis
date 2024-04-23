"""
Module network.shortest_paths.a_star
"""
import math

from queue import PriorityQueue
from typing import Dict
from network import Network

class NetworkSpatialAStar:
    """
    Implementation of the A* algorithm.
    """
    _net:       Network
    _INFINITY:  float
    _f:         Dict[int, float]
    _g:         Dict[int, float]
    _pars:      Dict[int, int]
    _pq:        PriorityQueue
    _src:       int

    @property
    def _is_terminated(self):
        return False

    def _update_per_iteration(self):
        return

    def _from_net(self, net: Network, INFINITY: float = float('inf')):
        self._net = net
        self._INFINITY = INFINITY
        return self

    @classmethod
    def from_net(cls, net: Network, **kwargs):
        """
        Initialise from the network.
        """
        return cls()._from_net(net, **kwargs)
    
    def _reverse_path_from(self, dest: int):
        if self._g.get(dest) is None:
            return

        while dest != self._src:
            connector = self._pars[dest]
            yield connector
            dest = connector.src

    def _path_to(self, dest: int):
        return reversed(list(self._reverse_path_from(dest=dest)))

    def path(self, src: int, dest: int) -> None:
        """
        Returns the shortest path from source src to destination dest.
        """
        def _h(node: int):
            return math.dist(self._net.nodes[node].coord, self._net.nodes[dest].coord)

        self._g = {}
        self._f = {}
        self._pars = {}
        self._src = src

        self._g[src] = 0
        self._f[src] = _h(src)

        self._pq = PriorityQueue()
        self._pq.put((self._f[src], src))

        while not self._pq.empty():
            f_u, u = self._pq.get()
            if f_u != self._f.get(u, self._INFINITY):
                continue

            print(u, self._g[u], _h(u))

            if u == dest:
                return self._g[u], list(self._path_to(dest))

            for connector in self._net.adjs[u]:
                v, w = connector.dest, connector.weight
                if self._g.get(v, self._INFINITY) > self._g.get(u, self._INFINITY) + w:
                    self._g[v] = self._g[u] + w
                    self._f[v] = self._g[v] + _h(v)
                    self._pars[v] = connector
                    self._pq.put((self._f[v], v))

        return self._INFINITY, []

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
        return self._f

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
            for (node, d_node) in self._f.items()
            if d_node != self._INFINITY
        }