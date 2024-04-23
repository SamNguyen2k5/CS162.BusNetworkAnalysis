"""
Module network.shortest_paths.bidirectional_dijkstra
"""
from queue import PriorityQueue
from typing import Dict, TypeVar
from network.network import Network, NetworkConnector

TNode = TypeVar('TNode')

class NetworkBidirectionalDijkstra:
    """
    Implementation of the Bidirectional Dijkstra algorithm.
    """
    _INFINITY:  float
    _nodes:     Dict[int, TNode]
    _adjs_fwd:  Dict[int, list[NetworkConnector]]
    _adjs_bkd:  Dict[int, list[NetworkConnector]]

    _dists_fwd: Dict[int, float]
    _dists_bkd: Dict[int, float]
    _pars_fwd:  Dict[int, NetworkConnector]
    _pars_bkd:  Dict[int, NetworkConnector]

    def _from_net(self, net: Network, INFINITY: float = float('inf')):
        self._INFINITY = INFINITY
        self._nodes = net.nodes
        self._adjs_fwd = net.adjs
        self._adjs_bkd = net.adjs_rev
        return self
        
    @classmethod
    def from_net(cls, net: Network, **kwargs):
        """
        Initialise from the network.
        """
        return cls()._from_net(net, **kwargs)

    def path(self, src: int, dest: int):
        """
        Returns the shortest path from source src to destination dest.
        """
        def relax(dists: Dict[int, float], pars: Dict[int, int], pq: PriorityQueue, connector: NetworkConnector, reverse: bool = False):
            u, v = connector.ends
            if reverse:
                u, v = v, u
            w = connector.weight

            dist_u = dists.get(u, self._INFINITY)       
            dist_v = dists.get(v, self._INFINITY)       

            if dist_v > dist_u + w:
                dists[v] = dist_u + w
                pars[v] = connector
                pq.put((dists[v], v))
                return True
            
            return False
        
        self._dists_fwd, self._pars_fwd = {}, {}
        self._dists_bkd, self._pars_bkd = {}, {}

        dist, mid = self._INFINITY, -1
        dist_s = self._dists_fwd[src] = 0
        dist_t = self._dists_bkd[dest] = 0
        s, t = src, dest

        pq_fwd, pq_bkd = PriorityQueue(), PriorityQueue()        
        pq_fwd.put((0, src))
        pq_bkd.put((0, dest))

        is_fwd = False

        while (not pq_fwd.empty()) or (not pq_bkd.empty()):
            is_fwd = not is_fwd
            if is_fwd:
                if pq_fwd.empty():
                    continue
                dist_s, s = pq_fwd.get()
                if dist_s > dist:
                    pq_fwd.queue.clear()
                    continue
                
            else:
                if pq_bkd.empty():
                    continue
                dist_t, t = pq_bkd.get()
                if dist_t > dist:
                    pq_bkd.queue.clear()
                    continue

            (dist, mid) = min(
                (dist, mid), 
                (self._dists_fwd[s] + self._dists_bkd.get(s, self._INFINITY), s),
                (self._dists_bkd[t] + self._dists_fwd.get(t, self._INFINITY), t)
            )

            if is_fwd and dist_s == self._dists_fwd[s]:
                for connector in self._adjs_fwd[s]:
                    relax(self._dists_fwd, self._pars_fwd, pq_fwd, connector)

            if (not is_fwd) and dist_t == self._dists_bkd[t]:
                for connector in self._adjs_bkd[t]:
                    relax(self._dists_bkd, self._pars_bkd, pq_bkd, connector, reverse=True)

        if mid == -1:
            return self._INFINITY, []

        path_fwd, path_bkd = [], []

        node = mid
        while node != src:
            connector = self._pars_fwd[node]
            path_fwd.append(connector)
            node = connector.src

        node = mid
        while node != dest:
            connector = self._pars_bkd[node]
            path_bkd.append(connector)
            node = connector.dest

        return dist, [*reversed(path_fwd), *path_bkd]

    # --------------- Getters and Setters -------------------
    
    @property
    def search_space(self) -> Dict[int, tuple[float, float]]:
        """
        Returns the search space after the algorithm execution.
        """
        nodes = set(self._dists_fwd.keys()) | set(self._dists_bkd.keys())
        return {
            node: (
                self._dists_fwd.get(node, self._INFINITY),
                self._dists_bkd.get(node, self._INFINITY)
            )
            for node in nodes
        }