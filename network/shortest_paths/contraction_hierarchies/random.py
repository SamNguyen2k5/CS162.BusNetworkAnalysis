"""
Module network.shortest_paths.contraction_hierarchies.random
"""
from __future__ import annotations
import random
from tqdm import tqdm

from network.network import Network
from network.shortest_paths.contraction_hierarchies.contraction_hierarchies import NetworkContractionHierarchies
        
class NetworkContractionHierarchiesRandom(NetworkContractionHierarchies):
    """
    Implementation of the NetworkContractionHierarchies class.
    Builds the network using a random node contraction order.
    """
    
    def _to_adjs_fwd_bkd(self):
        self._adjs_fwd = {node: [] for node in self._net.nodes}
        self._adjs_bkd = {node: [] for node in self._net.nodes}
        for subnet in (self._net, self._overlay_net):
            for connectors in subnet.adjs.values():
                for connector in connectors:
                    src, dest = connector.ends
                    adjs_list = (self._adjs_fwd[src] 
                        if self._level[src] < self._level[dest] \
                        else self._adjs_bkd[dest])

                    adjs_list.append(connector)

    def _build_contraction_net(self, net: Network, local_steps: int = 50, INFINITY: float = float('inf'), **kwargs):
        self._init_vars(net, INFINITY)

        contracted_nodes = list(net.nodes.keys())
        random.shuffle(contracted_nodes)

        # Contraction
        for lvl, node in enumerate(tqdm(contracted_nodes)):
            self._level[node] = lvl
            self._contract(node, self._shortcuts_added_at(node, local_steps=local_steps))

        self._to_adjs_fwd_bkd()