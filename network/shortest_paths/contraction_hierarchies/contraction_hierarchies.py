"""
Module network.shortest_paths.contraction_hierarchies.contraction_hierarchies
"""
from typing import Iterable
from network.network import Network, NetworkConnector, RemovableNetwork
from network.shortest_paths import NetworkBidirectionalDijkstra, NetworkDijkstraLocalSteps

class NetworkConnectorTreeNode(NetworkConnector):
    """
    A sequence of network edges stored in a binary-tree style.
    """
    def __init__(self, left, right):
        super().__init__(
            src = left.src,
            dest = right.dest
        )
        self._left = left
        self._right = right
        self._weight = left.weight + right.weight

    @property
    def left(self):
        """
        Returns the left node of the binary tree.
        """
        return self._left

    @property
    def right(self):
        """
        Returns the right node of the binary tree.
        """
        return self._right

    @property
    def weight(self):
        """
        Returns the total weight of the edge sequence.
        """
        return self._weight
    
    def __repr__(self) -> str:
        return 'NetworkConnectorTreeNode(src={}, dest={}, weight={}, childtypes={}, {})' \
            .format(self.src, self.dest, self.weight, type(self._left), type(self._right))
    
    def unpack(self) -> Iterable[NetworkConnector]:
        """
        Unpacking the binary tree into a sequence of edges.
        """
        for connector in self._left.unpack():
            yield connector
        for connector in self._right.unpack():
            yield connector

class NetworkContractionHierarchies(NetworkBidirectionalDijkstra):
    """
    Generic implementation of the Contraction Hierarchies algorithm.
    """
    _level:         dict[int, int]
    _rem_net:       RemovableNetwork
    _net:           Network
    _overlay_net:   Network
    _no_shortcuts:  int

    def _shortcuts_added_at(self, node: int, local_steps: int = 50):
        def group_connectors_by_min_weight(node_select, adjs):
            group = {}
            for connector in adjs:
                node = node_select(connector)
                if node not in group:
                    group[node] = connector
                elif group[node].weight > connector.weight:
                    group[node] = connector
            return group

        lefts  = group_connectors_by_min_weight(lambda connector: connector.src,  self._rem_net.adjs_rev[node])
        rights = group_connectors_by_min_weight(lambda connector: connector.dest, self._rem_net.adjs[node])
        
        shortcuts = []
        self._rem_net.hide_node(node)

        for left, left_connector in lefts.items():
            engine = NetworkDijkstraLocalSteps(limit=local_steps).from_src(net=self._rem_net, src=left)
            for right, right_connector in rights.items():
                dist = engine.dists.get(right, self._INFINITY)
                if dist > left_connector.weight + right_connector.weight:
                    # Contraction (may) leads to change in shortest path
                    shortcuts.append((left_connector, right_connector))

        self._rem_net.unhide_node(node)

        return shortcuts

    def _contract(self, node: int, shortcuts: list[tuple[int, int]]):
        self._rem_net.remove_node(node)
        for shortcut in shortcuts:
            connector = NetworkConnectorTreeNode(*shortcut)
            self._rem_net.add_edge(connector)
            self._overlay_net.add_edge(connector)
        
        self._no_shortcuts += len(shortcuts)

    def _to_adjs_fwd_bkd(self):
        self._adjs_fwd = {node: [] for node in self._net.nodes}
        self._adjs_bkd = {node: [] for node in self._net.nodes}
        for subnet in (self._net, self._overlay_net):
            for connectors in subnet.adjs.values():
                for connector in connectors:
                    src, dest = connector.ends
                    adjs_list = (self._adjs_fwd[src] if self._level[src] < self._level[dest] else self._adjs_bkd[dest])
                    adjs_list.append(connector)

    def _init_vars(self, net: Network, INFINITY: float = float('inf')):
        self._rem_net = RemovableNetwork.from_net(net=net)
        self._net = net
        self._overlay_net = Network()

        self._INFINITY = INFINITY
        self._nodes = net.nodes
        self._level = {}
        self._no_shortcuts = 0
        
        self._early_stop = False

    def _edge_difference(self, node: int, shortcuts: list[tuple[int, int]] = None, local_steps: int = 50) -> int:
        if not shortcuts:
            shortcuts = self._shortcuts_added_at(node, local_steps)
        return len(shortcuts) - self._rem_net.degree(node) - self._rem_net.degree_rev(node)

    def _build_contraction_net(self, net: Network, **kwargs):
        raise NotImplementedError()

    @classmethod
    def from_net(cls, net: Network, **kwargs):
        obj = cls()
        obj._build_contraction_net(net, **kwargs)
        return obj

    def dist(self, src: int, dest: int, **kwargs):
        """
        Returns the length of the shortest path from source src to destination dest.
        """
        return super().path(src, dest, **kwargs)[0]

    def raw_path(self, src: int, dest: int, **kwargs):
        """
        Returns the "raw" shortest path from source src to destination dest.
        Some continuous edges in the path may be compressed into a single NetworkConnectorTreeNode.
        """
        return super().path(src, dest, **kwargs)

    def path(self, src: int, dest: int, **kwargs):
        """
        Returns the shortest path from source src to destination dest.
        """
        super_path = super().path(src, dest, **kwargs)
        return super_path[0], sum([list(connector_tree_node.unpack()) for connector_tree_node in super_path[1]], [])

    @property
    def no_shortcuts(self):
        """
        Returns the number of shortcuts in the overlaying network.
        """
        return self._no_shortcuts

    @property
    def level(self):
        """
        Returns the mapping of a node to its level.
        """
        return self._level