"""
Module network.shortest_paths.contraction_hierarchies.lazy_ED
"""
from __future__ import annotations
from queue import PriorityQueue
from tqdm import tqdm

from network.network import Network
from network.shortest_paths.contraction_hierarchies.contraction_hierarchies import NetworkContractionHierarchies

class NetworkContractionHierarchiesLazyED(NetworkContractionHierarchies):
    """
    Implementation of the NetworkContractionHierarchies class.
    Builds the network using the lazy edge-difference assignment heuristic.
    """
    
    def _build_contraction_net(self, net: Network, local_steps: int = 50, INFINITY: float = float('inf'), **kwargs):
        self._init_vars(net, INFINITY)
        
        costs_of = {}
        pq = PriorityQueue()

        for node in tqdm(net.nodes):
            costs_of[node] = self._edge_difference(node, local_steps=local_steps)
            pq.put((costs_of[node], node))

        lvl = 0
        pbar = tqdm(total=len(net.nodes))

        while not pq.empty():
            _, node = pq.get()
            current_shortcuts = self._shortcuts_added_at(node, local_steps)
            current_cost = self._edge_difference(node, shortcuts=current_shortcuts, local_steps=local_steps)
            
            if (not pq.empty()) and current_cost > pq.queue[0][0]:
                costs_of[node] = current_cost
                pq.put((current_cost, node))
                continue

            self._level[node] = lvl
            self._contract(node, current_shortcuts)
            costs_of.pop(node, 0)

            lvl += 1
            pbar.update(1)

        pbar.close()
        self._to_adjs_fwd_bkd()