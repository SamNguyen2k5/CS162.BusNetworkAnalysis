"""
Module network.network
"""
import copy
from dataclasses import dataclass
from typing import TypeVar, Generic, Iterable, Dict

@dataclass
class NetworkConnector:
    """
    Defines an directed edge of a generic graph.
    """
    src:        int
    dest:       int

    # def reverse(self) -> 'NetworkConnector':
    #     rev_connector = deepcopy(self)
    #     rev_connector.src, rev_connector.dest = rev_connector.dest, rev_connector.src
    #     return rev_connector
    
    @property
    def ends(self) -> tuple[int, int]:
        """
        Returns the tuple of the ends of the edge
        """
        return self.src, self.dest

    @property
    def weight(self) -> float:
        """
        Virtual weight function of the edge
        """
        raise NotImplementedError

    def unpack(self):
        """
        Returns the edge as a generator.
        """
        yield self

    def __hash__(self):
        return id(self)

TNode = TypeVar('TNode', bound=object)
TConnector = TypeVar('TConnector', bound=NetworkConnector)

class Network(Generic[TNode, TConnector]):
    """
    Implementation of a generic weighted network.
    """
    _nodes:     Dict[int, TNode]
    _adjs:      Dict[int, TConnector]
    _adjs_rev:  Dict[int, TConnector]

    def __init__(self, nodes = None, adjs = None, adjs_rev = None) -> None:
        if nodes is None:
            nodes = {}
        if adjs is None:
            adjs = {}

        self._nodes = nodes
        self._adjs = adjs

        if adjs_rev is None:
            self._adjs_rev = {}
            for connectors in self._adjs.values():
                for connector in connectors:
                    if connector.dest not in self._adjs_rev:
                        self._adjs_rev[connector.dest] = []
                    self._adjs_rev[connector.dest].append(connector)

        for node in self._nodes:
            if node not in self._adjs:
                self._adjs[node] = []
            if node not in self._adjs_rev:
                self._adjs_rev[node] = []

    def __len__(self):
        return len(self._nodes)
        
    def degree(self, node_id):
        """
        Returns the out-degree of a node.
        """
        return len(self._adjs[node_id])
        
    def degree_rev(self, node_id):
        """
        Returns the in-degree of a node.
        """
        return len(self._adjs_rev[node_id])

    def degrees(self):
        """
        Returns the out-degree array.
        """
        return (self.degree(node) for node in self._adjs.keys())
        
    @property
    def nodes(self):
        """
        Returns the set of nodes.
        """
        return self._nodes

    @property
    def adjs(self):
        """
        Returns the adjacency list.
        """
        return self._adjs

    @property
    def adjs_rev(self):
        """
        Returns the transposed adjacency list.
        """
        return self._adjs_rev
    
    @property
    def reverse(self):
        """
        Returns the transposed network.
        """
        return Network(
            nodes = self._nodes,
            adjs = self._adjs_rev,
            adjs_rev = self._adjs
        )
    
    def add_edge(self, connector: NetworkConnector):
        """
        Add an edge to the network.
        """
        src, dest = connector.ends
        if src not in self._nodes:
            self._nodes[src] = None
        if dest not in self._nodes:
            self._nodes[dest] = None

        if src not in self._adjs:
            self._adjs[src] = []
        if dest not in self._adjs_rev:
            self._adjs_rev[dest] = []

        self._adjs[src].append(connector)
        self._adjs_rev[dest].append(connector)

    def shallow_copy(self):
        """
        Copy the structure of the network (does not copy the inner node data).
        """
        return Network(
            nodes = copy.copy(self._nodes),
            adjs = copy.copy(self._adjs)
        )
    
@dataclass
class HideableAdjacencyList(Generic[TConnector]):
    """
    Adjacency list with temporary deletion.
    """
    obj:        Dict[int, Iterable[TConnector]]
    hidden:     set[int]

    def __getitem__(self, key):
        if key not in self.obj:
            return ()

        return filter(
            (lambda connector: (connector.src not in self.hidden) and (connector.dest not in self.hidden)), 
            self.obj[key]
        )

class RemovableNetwork(Network[TNode, TConnector]):
    """
    Implementation of a generic weighted network with node removability / hideability.
    """
    _hidden:    set[int]

    def __init__(self, nodes = None, adjs = None) -> None:
        super().__init__(nodes, adjs)
        for node in self._adjs:
            self._adjs[node] = set(self._adjs[node])
        for node in self._adjs_rev:
            self._adjs_rev[node] = set(self._adjs_rev[node])

        self._hidden = set()

    @classmethod
    def from_net(cls, net: Network[TNode, TConnector]):
        """
        Converts a network to a removable network.
        """
        return cls(
            nodes = copy.copy(net.nodes),
            adjs = copy.copy(net.adjs)
        )
    
    def add_edge(self, connector: TConnector):
        """
        Add an edge to the network.
        """
        src, dest = connector.ends
        if src not in self._nodes:
            self._nodes[src] = None
        if dest not in self._nodes:
            self._nodes[dest] = None

        if src not in self._adjs:
            self._adjs[src] = set()
        if dest not in self._adjs_rev:
            self._adjs_rev[dest] = set()

        self._adjs[src].add(connector)
        self._adjs_rev[dest].add(connector)

    def hide_node(self, node: int):
        """
        Temporarily hide a node.
        """
        self._hidden.add(node)

    def unhide_node(self, node: int):
        """
        Temporarily unhide a node.
        """
        self._hidden.remove(node)
    
    def is_hidden(self, node: int):
        """
        Returns if a node is hidden.
        """
        return node in self._hidden

    def remove_node(self, node: int):
        """
        Permanently remove a node.
        """
        connectors = self._adjs.pop(node, {})
        connectors_rev = self._adjs_rev.pop(node, {})

        for connector in connectors:
            self._adjs_rev[connector.dest].remove(connector)
        for connector_rev in connectors_rev:
            self._adjs[connector_rev.src].remove(connector_rev)

        self._nodes.pop(node)

    def is_removed(self, node: int):
        """
        Returns if a node is removed.
        """
        return node in self._nodes

    def degree(self, node_id: int):
        """
        Returns the out-degree of a node, taking hidden nodes into account.
        """
        return sum(
            1 
            for connector in self._adjs.get(node_id, [])
            if (connector.src not in self._hidden) and (connector.dest not in self._hidden)
        )
        
    def degree_rev(self, node_id: int):
        """
        Returns the in-degree of a node, taking hidden nodes into account.
        """
        return sum(
            1 
            for connector in self._adjs_rev.get(node_id, [])
            if (connector.src not in self._hidden) and (connector.dest not in self._hidden)
        )

    @property
    def adjs(self) -> HideableAdjacencyList:
        """
        Returns the hideable adjacency list.
        """
        return HideableAdjacencyList(obj=self._adjs, hidden=self._hidden)

    @property
    def adjs_rev(self) -> HideableAdjacencyList:
        """
        Returns the transposed hideable adjacency list.
        """
        return HideableAdjacencyList(obj=self._adjs_rev, hidden=self._hidden)