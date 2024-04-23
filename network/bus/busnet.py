"""
Module network.bus.busnet
Contains 
- BusNetwork class, an implementation of the Network class with specific inputting methods.
- BusNetworkDijkstra class, an implementation of the NetworkDijkstra class with specific outputting methods.
"""
from dataclasses import dataclass
import math

import json
import ndjson
from tqdm import tqdm
from rtree import Index
from helper import line_dist, proj_vector

from elements import Stop, Path
from queries import StopQuery, VariantQuery, PathQuery
from network.network import NetworkConnector, Network
from network.shortest_paths import NetworkDijkstra

@dataclass
class BusNetworkConnector(NetworkConnector):
    """
    Defines an edge on a bus network.
    Arguments:
        - route_ids:        Tuple of RouteId and RouteVarId
        - time:             Travelling time of the path
        - length:           Travelling distance of the path
        - real_path:        LineString representing the actual path in Cartesian coordinates.
    """
    route_ids:  tuple[int, int]
    time:       float
    length:     float
    real_path:  list[tuple[float, float]]

    @property
    def weight(self) -> float:
        """
        Defines the weight function of an edge.
        In this case, the weight is set to be the travelling time.
        """
        return self.time
    
    def __hash__(self):
        return id(self)

    @classmethod
    def from_dict(cls, obj: dict):
        """
        Converts to a Python dictionary.
        """
        return BusNetworkConnector(
            route_ids=(int(obj['RouteId']), int(obj['RouteVarId'])),
            src=obj['Src'],
            dest=obj['Dest'],
            time=obj['Time'],
            length=obj['Length'],
            real_path=obj['Path']
        )

    def to_dict(self) -> dict:
        """
        Exports to a Python dictionary.
        """
        return {
            "RouteId":      self.route_ids[0],
            "RouteVarId":   self.route_ids[1],
            "Src":          self.src,
            "Dest":         self.dest,
            "Time":         self.time,
            "Length":       self.length,
            "Path":         self.real_path
        }
    
    def __repr__(self) -> str:
        return 'BusNetworkConnector(src={}, dest={}, weight={})'.format(self.src, self.dest, self.weight)

class BusNetwork(Network[Stop, BusNetworkConnector]):
    """
    Implementation of Network that contains information of bus Stops and Variants.
    """
    class SidesSet:
        """
        A set of segments (or "sides"). 
        Supports finding the segment with closest distance to a given point.
        """

        class Default:
            """
            Naive implementation of SidesSet.
            """
            _sides: list[tuple[tuple[float, float], tuple[float, float]]]

            def __init__(self, sides: list[tuple[tuple[float, float], tuple[float, float]]]):
                self._sides = sides

            def best_side(self, coord: tuple[float, float]) -> list[tuple[float, int]]:
                """
                Returns the segment with closest distance to a given point given coordinates.
                """
                return min([
                    (line_dist(coord, p1, p2), idx) 
                    for idx, (p1, p2) in enumerate(self._sides)
                ])
            
            def best_side_candidates_count(self, coord: tuple[float, float]) -> int:
                # pylint: disable=unused-argument
                """
                Counts the number of candidating segment with distance possibly 
                closest to a given point given coordinates.

                In this naive implementation, every segment is a possible candidate.
                """
                return len(self._sides)
            
            def close(self):
                """
                End of usage.
                """
                self._sides = []
            
        class Spatial:
            """
            A more advanced implementation of SidesSet using R-Tree.
            """
            _idx_tree: Index
            _BOX_SIZE: float

            def __init__(self, sides: list[tuple[tuple[float, float], tuple[float, float]]], BOX_SIZE: float = 150.0):
                self._BOX_SIZE = BOX_SIZE
                self._idx_tree = Index()
                
                def minmax(x, y):
                    return (min(x, y), max(x, y))
                
                for idx, side in enumerate(sides):
                    (x1, y1), (x2, y2) = side
                    x1, x2 = minmax(x1, x2)
                    y1, y2 = minmax(y1, y2)
                    self._idx_tree.insert(id=idx, coordinates=(x1, y1, x2, y2), obj=(idx, side))

            # pylint: disable=not-an-iterable
            def best_side(self, coord: tuple[float, float]) -> list[tuple[float, int]]:
                """
                Returns the segment with closest distance to a given point given coordinates.
                """
                x0, y0 = coord
                test_box = (x0 - self._BOX_SIZE, y0 - self._BOX_SIZE, x0 + self._BOX_SIZE, y0 + self._BOX_SIZE)
                candidates = self._idx_tree.intersection(test_box, objects='raw') 

                return min((
                    (line_dist(coord, p1, p2), idx) 
                    for idx, (p1, p2) in candidates
                ))
            
            def best_side_candidates_count(self, coord: tuple[float, float]) -> list[tuple[float, int]]:
                """
                Counts the number of candidating segment with distance possibly 
                closest to a given point given coordinates.

                In this advanced implementation, only segments within the minimal 
                rectangular bound (MBR) are candidates.
                """
                x0, y0 = coord
                test_box = (x0 - self._BOX_SIZE, y0 - self._BOX_SIZE, x0 + self._BOX_SIZE, y0 + self._BOX_SIZE)
                return self._idx_tree.count(test_box)            
            
            def close(self):
                """
                End of usage.
                """
                self._idx_tree.close()

        _sides_set: Default | Spatial
        def __init__(
            self, 
            sides: list[tuple[tuple[float, float], tuple[float, float]]], 
            sides_set_type: str = 'default', **kwargs
        ):
            if sides_set_type == 'default':
                self._sides_set = self.Default(sides, **kwargs)
            if sides_set_type == 'spatial':
                self._sides_set = self.Spatial(sides, **kwargs)

        @classmethod
        def from_path(cls, path: Path):
            """
            Creates a SideSet object.
            """
            return cls(path.polysides())

        def best_side(self, coord: tuple[float, float]) -> list[tuple[float, int]]:
            """
            Returns the segment with closest distance to a given point given coordinates.
            """
            return self._sides_set.best_side(coord)
        
        def best_side_candidates_count(self, coord: tuple[float, float]) -> int:
            """
            Counts the number of candidating segment with distance possibly 
            closest to a given point given coordinates.
            """
            return self._sides_set.best_side_candidates_count(coord)
        
        def close(self):
            """
            End of usage.
            """
            self._sides_set.close()

    @classmethod
    def from_json(cls, file: str = 'net.json'):
        """
        Input the network from a pre-exported JSON file.
        """
        with open(file, 'r', encoding='utf-8') as f:
            obj = json.load(f)

        stops = { int(stop_id): Stop.from_dict(obj[stop_id]['Data']) for stop_id in obj.keys() }
        adjs  = { int(stop_id): [BusNetworkConnector.from_dict(connector) for connector in obj[stop_id]['Adjacent']] for stop_id in obj.keys() }
        return cls(stops, adjs)

    @classmethod
    def _analyse_sides_set(
        cls,
        stops_json_file: str = 'stops.json', 
        # vars_json_file: str = 'vars.json', 
        paths_json_file: str = 'paths.json',
        sides_set_type: str = 'spatial'
    ):
        """
        Analyse the network built from 3 JSON files describing a list of Stops, Variants and Paths.
        Parameters:
            - stops_json_file: JSON file describing a list of Stops.
            - vars_json_file: JSON file describing a list of Variants.
            - paths_json_file: JSON file describing a list of Paths.
            - sides_set_type = 'default' | 'spatial':
                + If sides_set_type = 'default': 
                    Analyse the Graph construction algorithm I algorithm (naive).
                + If sides_set_type = 'spatial': 
                    Analyse the Graph construction algorithm II algorithm (advanced using R-Tree).
        """

        stops = StopQuery.from_ndjson(stops_json_file)
        # vars = VariantQuery.from_ndjson(vars_json_file)
        paths = PathQuery.from_ndjson(paths_json_file)

        with open(stops_json_file, 'r', encoding='utf-8') as f:
            obj = ndjson.load(f)
            stops_id_en_routes = {
                (int(route['RouteId']), int(route['RouteVarId'])): [stop['StopId'] for stop in route['Stops']]
                for route in obj
            }

        print('sides_set_type = ', sides_set_type)

        for route_ids, stops_en_route in tqdm(stops_id_en_routes.items()):
            path = paths[route_ids]
            sides = list(path.polysides())
            sides_set = cls.SidesSet(sides, sides_set_type)

            counts = []
            for stop_id in stops_en_route:
                counts.append(sides_set.best_side_candidates_count(stops[stop_id].coord))
            yield route_ids, len(sides), counts

        sides_set.close()

    @classmethod
    def from_ndjsons(
        cls,
        stops_json_file: str = 'stops.json', 
        vars_json_file: str = 'vars.json', 
        paths_json_file: str = 'paths.json',
        sides_set_type: str = 'spatial'
    ):
        """
        Input the network from 3 JSON files describing a list of Stops, Variants and Paths.
        Parameters:
            - stops_json_file: JSON file describing a list of Stops.
            - vars_json_file: JSON file describing a list of Variants.
            - paths_json_file: JSON file describing a list of Paths.
            - sides_set_type = 'default' | 'spatial':
                + If sides_set_type = 'default': 
                    Construct the graph using the Graph construction algorithm I algorithm (naive).
                + If sides_set_type = 'spatial': 
                    Construct the graph using the Graph construction algorithm II algorithm (advanced using R-Tree).
        """
        stops = StopQuery.from_ndjson(stops_json_file)
        variants = VariantQuery.from_ndjson(vars_json_file)
        paths = PathQuery.from_ndjson(paths_json_file)

        with open(stops_json_file, 'r', encoding='utf-8') as f:
            obj = ndjson.load(f)
            stops_id_en_routes = {
                (int(route['RouteId']), int(route['RouteVarId'])): [stop['StopId'] for stop in route['Stops']]
                for route in obj
            }

        print('sides_set_type = ', sides_set_type)

        net = cls(nodes=stops.to_dict(), adjs={})

        for route_ids, stops_en_route in tqdm(stops_id_en_routes.items()):
            speed = variants[route_ids].distance / variants[route_ids].running_time
            path = paths[route_ids]
            sides = list(path.polysides())
            sides_set = cls.SidesSet(sides, sides_set_type)

            side_on_stops = [
                (stop_id, sides_set.best_side(stops[stop_id].coord)[1])
                for stop_id in stops_en_route  
            ]

            for ((stop1, idx1), (stop2, idx2)) in zip(side_on_stops, side_on_stops[1:]):        
                START_PATH = tuple(proj_vector(stops[stop1].coord, sides[idx1][0], sides[idx1][1]))
                END_PATH   = tuple(proj_vector(stops[stop2].coord, sides[idx2][0], sides[idx2][1]))

                length = sum(math.dist(path.coords[idx], path.coords[idx + 1]) for idx in range(idx1 + 1, idx2))
                length += math.dist(START_PATH, path.coords[idx1])
                length += math.dist(  END_PATH, path.coords[idx2])

                net.add_edge(BusNetworkConnector(
                    src = stop1, dest = stop2, route_ids = route_ids, length = length, time = length / speed,
                    real_path = [stops[stop1].coord, START_PATH] + path.coords[idx1 + 1 : idx2] + [END_PATH, stops[stop2].coord]
                ))

        sides_set.close()
        return net

    def to_dict(self):
        """
        Converts the bus network to a Python dictionary.
        """
        return {
            node_id: {
                "Data": node.to_dict(),
                "Adjacent": [connector.to_dict() for connector in self.adjs[node_id]]
            }
            for node_id, node in self.nodes.items()
        }

    def to_json(self, file: str):
        """
        Exports BusNetwork information to JSON file. 
        The function calls to_dict() to convert BusNetwork to a dictionary, then dumps it into a JSON file.
        """
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False)

class BusNetworkDijkstra(NetworkDijkstra):
    """
    Implementation of NetworkDijkstra that supports inclusion of bus network information into outputting.
    """

    def path_to_json(self, dest: int, file: str = None, write_mode: str = 'w'):
        """
        Exports the shortest path to a JSON file from a precomputed Dijkstra engine.
        """

        connectors = list(self.path_to(dest))
        node_ids = [connector.src for connector in connectors] + [dest]
        
        obj = {
            "Src": self.src,
            "Dest": dest,
            "PathTime": sum(connector.time for connector in connectors),
            "PathLength": sum(connector.length for connector in connectors),
            "Path": [connector.to_dict() for connector in connectors],
            "Stops": [self._net.nodes[node_id].to_dict() for node_id in node_ids]
        }

        if file is None:
            return json.dumps(obj, ensure_ascii=False)

        with open(file, write_mode, encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False)

    def shortest_path_to_json(self, net: Network, src: int, dest: int, file: str = None):
        """
        Exports the shortest path to a JSON file from a blank Dijkstra engine.
        """

        self.from_src(net=net, src=src)
        return self.path_to_json(dest=dest, file=file)
    
    def all_shortest_path_to_json(self, net: Network, file: str):
        """
        Exports all shortest paths to a JSON file from a blank Dijkstra engine.
        WARNING: outputted data may be up to gigabytes.
        """

        with open(file, 'w', encoding='utf-8') as f:
            f.close()

        print(file)

        for src in tqdm(net.nodes):
            self.from_src(net=net, src=src)
            for dest in tqdm(net.nodes):
                self.path_to_json(dest=dest, file=file, write_mode='a')