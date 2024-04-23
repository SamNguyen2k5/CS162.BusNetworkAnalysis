from __future__ import annotations
import itertools as iters
from tqdm import tqdm

from network.network import Network
from network.shortest_paths.contraction_hierarchies.contraction_hierarchies import NetworkContractionHierarchies

class NetworkContractionHierarchiesPeriodicED(NetworkContractionHierarchies):
    """
    Implementation of the NetworkContractionHierarchies class.
    Builds the network using the periodic edge-difference assignment heuristic.
    """
    
    def _build_contraction_net(self, net: Network, update_every_after = 100, local_steps: int = 50, INFINITY: float = float('inf'), **kwargs):
        self._init_vars(net, INFINITY)

        def all_costs_of(nodes):
            return {
                node: self._edge_difference(node, local_steps=local_steps)
                for node in nodes
            }

        costs_of = all_costs_of(net.nodes)

        lvl = 0
        pbar = tqdm(total=len(net.nodes))

        while costs_of:
            contracted_nodes = sorted(list(costs_of.keys()), key=lambda x: costs_of[x])
        
            for node in iters.islice(contracted_nodes, update_every_after):
                self._level[node] = lvl
                self._contract(node, self._shortcuts_added_at(node, local_steps=local_steps))
                costs_of.pop(node, 0)

                lvl += 1
                pbar.update(1)

            left_over_nodes = list(costs_of.keys())
            costs_of = all_costs_of(left_over_nodes)

        self._to_adjs_fwd_bkd()