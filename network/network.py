import copy
from dataclasses import dataclass
from typing import TypeVar, Generic, Iterable

@dataclass
class NetworkConnector:
    src:        int
    dest:       int

    # def reverse(self) -> 'NetworkConnector':
    #     rev_connector = deepcopy(self)
    #     rev_connector.src, rev_connector.dest = rev_connector.dest, rev_connector.src
    #     return rev_connector
    
    @property
    def ends(self) -> tuple[int, int]:
        return self.src, self.dest

    @property
    def weight(self) -> float:
        raise NotImplementedError

    def unpack(self):
        yield self

    def __hash__(self):
        return id(self)

TNode = TypeVar('TNode')
TConnector = TypeVar('TConnector')

class Network(Generic[TNode, TConnector]):
    _nodes:     dict
    _adjs:      dict
    _adjs_rev:  dict

    def __init__(self, nodes = {}, adjs = {}, adjs_rev = None) -> None:
        self._nodes = nodes
        self._adjs = adjs

        if adjs_rev == None:
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
        return len(self._adjs[node_id])
        
    def degree_rev(self, node_id):
        return len(self._adjs_rev[node_id])

    def degrees(self):
        return (self.degree(node) for node in self._adjs.keys())
        
    @property
    def nodes(self):
        return self._nodes

    @property
    def adjs(self):
        return self._adjs

    @property
    def adjs_rev(self):
        return self._adjs_rev
    
    @property
    def reverse(self):
        return Network(
            nodes = self._nodes,
            adjs = self._adjs_rev,
            adjs_rev = self._adjs
        )
    
    def add_edge(self, connector: NetworkConnector):
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
        return Network(
            nodes = copy.copy(self._nodes),
            adjs = copy.copy(self._adjs)
        )
    
@dataclass
class HideableAdjacencyList:
    obj:        dict[int, Iterable[NetworkConnector]]
    hidden:     set[int]

    def __getitem__(self, key):
        if key not in self.obj:
            return ()

        return filter(
            (lambda connector: (connector.src not in self.hidden) and (connector.dest not in self.hidden)), 
            self.obj[key]
        )

class RemovableNetwork(Network):
    _hidden:    set[int]

    def __init__(self, nodes = {}, adjs = {}) -> None:
        super().__init__(nodes, adjs)
        for node in self._adjs:
            self._adjs[node] = set(self._adjs[node])
        for node in self._adjs_rev:
            self._adjs_rev[node] = set(self._adjs_rev[node])

        self._hidden = set()

    @classmethod
    def from_net(cls, net: Network):
        return cls(
            nodes = copy.copy(net.nodes),
            adjs = copy.copy(net.adjs)
        )
    
    def add_edge(self, connector: NetworkConnector):
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
        self._hidden.add(node)

    def unhide_node(self, node: int):
        self._hidden.remove(node)
    
    def is_hidden(self, node: int):
        return node in self._hidden

    def remove_node(self, node: int):
        connectors = self._adjs.pop(node, {})
        connectors_rev = self._adjs_rev.pop(node, {})

        for connector in connectors:
            self._adjs_rev[connector.dest].remove(connector)
        for connector_rev in connectors_rev:
            self._adjs[connector_rev.src].remove(connector_rev)

        self._nodes.pop(node)

    def is_removed(self, node: int):
        return node in self._nodes

    def degree(self, node):
        return sum(
            1 
            for connector in self._adjs.get(node, [])
            if (connector.src not in self._hidden) and (connector.dest not in self._hidden)
        )
        
    def degree_rev(self, node):
        return sum(
            1 
            for connector in self._adjs_rev.get(node, [])
            if (connector.src not in self._hidden) and (connector.dest not in self._hidden)
        )

    @property
    def adjs(self):
        return HideableAdjacencyList(obj=self._adjs, hidden=self._hidden)

    @property
    def adjs_rev(self):
        return HideableAdjacencyList(obj=self._adjs_rev, hidden=self._hidden)