from collections import defaultdict
from copy import deepcopy
from typing import Callable, Dict, Generic, Optional, Set, TypeVar, List, Tuple

A = TypeVar("A")


class Graph(Generic[A]):
    """
    A graph data structure.
    
    Supports:
    - Adding nodes and edges
    - Activating and deactivating edges
    - Union find ("networks", only works on undirected graphs)
    - Autojoin (adds an edge between all nodes)
    - Directed and undirected graphs
    - Weighted and unweighted graphs
    - Minimum and maximum distances between all nodes
    """
    def __init__(
        self,
        nodes: List[A],
        edges: List[Tuple[A, A]]
        | List[Tuple[A, A, int]]
        | List[Tuple[A, A, int, bool]],
        weight: Callable[[A, A], int],
        autojoin: bool = False,
        union_find: bool = False,
        default_active: bool = False,
        directed: bool = False,
    ):
        self.__autojoin: bool = autojoin
        self.__union_find: bool = union_find
        self.__default_active: bool = default_active
        self.__directed: bool = directed
        self.__weight: Callable[[A, A], int] = weight
        self.__sort_dirty: bool = True

        self.__nodes: List[A] = deepcopy(nodes)
        self.__edges: Dict[A, Dict[A, int]] = defaultdict(dict)

        for edge in edges:
            if len(edge) == 2:
                self.__edges[edge[0]][edge[1]] = (
                    weight(edge[0], edge[1]),
                    default_active,
                )
            elif len(edge) == 3:
                self.__edges[edge[0]][edge[1]] = (edge[2], default_active)
            else:
                self.__edges[edge[0]][edge[1]] = (edge[2], edge[3])

        self.__min_distances: List[Tuple[A, A, int]] = list()
        self.__max_distances: List[Tuple[A, A, int]] = list()
        self.__network_contents: List[Set[A]] = list()
        self.__networks: Dict[A, int] = dict()
        if autojoin:
            for node1 in nodes:
                for node2 in nodes:
                    if node1 == node2:
                        continue
                    self.add_edge(node1, node2, weight(node1, node2))

    def add_node(self, node: A):
        """
        Adds a node to the graph.
        If autojoin is enabled, adds an edge between the new node and all other nodes.
        """
        self.__nodes.append(node)
        self.__networks[node] = len(self.__network_contents)
        self.__network_contents.append(set([node]))
        if self.__autojoin:
            for node1 in self.__nodes:
                if node1 == node:
                    continue
                self.add_edge(node1, node, self.__weight(node1, node))

    def add_edge(
        self,
        node1: A,
        node2: A,
        weight: Optional[int] = None,
        active: Optional[bool] = None,
    ):
        """
        Adds an edge between two nodes. Overwrites the edge if it already exists.

        If active is None, uses the default active state.
        If weight is None, uses the weight function.
        """
        if active is None:
            active = self.__default_active
        if weight is None:
            weight = self.__weight(node1, node2)
        self.__edges[node1][node2] = (weight, active)
        if not self.__directed:
            self.__edges[node2][node1] = (weight, active)
        if active:
            self.activate_edge(node1, node2)
        self.__min_distances.append((node1, node2, weight))
        self.__max_distances.append((node1, node2, weight))
        self.__sort_dirty = True

    def has_edge(self, node1: A, node2: A) -> bool:
        """
        Returns True if there is an edge between two nodes.
        """
        return node1 in self.__edges and node2 in self.__edges[node1]

    def edge_weight(self, node1: A, node2: A) -> int:
        """
        Returns the weight of an edge between two nodes.
        """
        return self.__edges[node1][node2][0]

    def edge_active(self, node1: A, node2: A) -> bool:
        """
        Returns True if an edge between two nodes is active.
        """
        return self.__edges[node1][node2][1]

    def distance_pairs(self, min=True):
        """
        Returns a list of distance pairs between all nodes.
        If min is True, returns the list of minimum distances between all nodes.
        If min is False, returns the list of maximum distances between all nodes.
        """
        if self.__sort_dirty:
            self.__min_distances.sort(key=lambda x: x[2])
            self.__max_distances.sort(key=lambda x: x[2])
            self.__sort_dirty = False
        if min:
            return deepcopy(self.__min_distances)
        return deepcopy(self.__max_distances)

    def activate_edge(self, node1: A, node2: A):
        """
        Activates an edge between two nodes.
        If union find is enabled, merges the networks of the two nodes if they are in the same network.
        """
        self.__edges[node1][node2] = (self.__edges[node1][node2][0], True)
        if not self.__directed:
            self.__edges[node2][node1] = (self.__edges[node2][node1][0], True)

        # update networks
        if self.__union_find and not self.__directed:
            if node1 in self.__networks and node2 in self.__networks:
                if self.__networks[node1] == self.__networks[node2]:
                    # same network, do nothing
                    return
                else:
                    # merge networks
                    old_network_idx = self.__networks[node2]
                    self.__network_contents[self.__networks[node1]].update(
                        self.__network_contents[self.__networks[node2]]
                    )
                    for node in self.__network_contents[self.__networks[node2]]:
                        self.__networks[node] = self.__networks[node1]
                    # Use a none value to mark the network as deleted
                    self.__network_contents[old_network_idx] = None
            elif node1 in self.__networks:
                # add node2 to network of node1
                self.__networks[node2] = self.__networks[node1]
                self.__network_contents[self.__networks[node1]].add(node2)
            else:  # node2 in self.__networks
                # add node1 to network of node2
                self.__networks[node1] = self.__networks[node2]
                self.__network_contents[self.__networks[node2]].add(node1)

    def deactivate_edge(self, node1: A, node2: A):
        """
        Deactivates an edge between two nodes.

        If union find is enabled, verifies which nodes are reachable from node1
        and node2 and splits the network if necessary.
        """
        self.__edges[node1][node2] = (self.__edges[node1][node2][0], False)
        if not self.__directed:
            self.__edges[node2][node1] = (self.__edges[node2][node1][0], False)
        # update networks
        if self.__union_find and not self.__directed:
            if node1 not in self.__networks or node2 not in self.__networks:
                return
            if self.__networks[node1] != self.__networks[node2]:
                return
            # BFS from node1 to find reachable component and check if node2 is in it
            node1_component: Set[A] = {node1}
            queue: List[A] = [node1]
            while queue:
                current = queue.pop(0)
                for neighbor, (_, active) in self.__edges.get(current, {}).items():
                    if active and neighbor not in node1_component:
                        node1_component.add(neighbor)
                        queue.append(neighbor)
            if node2 in node1_component:
                return
            # Split the network
            old_network_idx = self.__networks[node1]
            node2_component = self.__network_contents[old_network_idx] - node1_component
            self.__network_contents[old_network_idx] = node1_component
            new_network_idx = len(self.__network_contents)
            self.__network_contents.append(node2_component)
            for node in node2_component:
                self.__networks[node] = new_network_idx

    def networks_contents(self, node: A) -> List[Set[A]]:
        """
        Returns the contents of the network of a node.
        """
        if self.__union_find and not self.__directed:
            return self.__network_contents[self.__networks[node]]
        else:
            raise ValueError("Union find is not enabled")

    def networks_count(self) -> int:
        """
        Returns the number of networks in the graph.
        """
        if self.__union_find and not self.__directed:
            return len(list(filter(lambda x: x is not None, self.__network_contents)))
        else:
            raise ValueError("Union find is not enabled")

    def networks_count_of(self, node: A) -> int:
        """
        Returns the size of the network of a node.
        """
        if self.__union_find and not self.__directed:
            return len(self.__network_contents[self.__networks[node]])
        else:
            raise ValueError("Union find is not enabled")
        
    def network_sizes(self) -> List[int]:
        """
        Returns the sizes of all networks in the graph.
        """
        if self.__union_find and not self.__directed:
            return list(map(len, list(filter(lambda x: x is not None, self.__network_contents))))
        else:
            raise ValueError("Union find is not enabled")
        
    def clone(self) -> "Graph[A]":
        """
        Returns a clone of the graph.
        """
        g = Graph(
            self.__nodes,
            self.__edges,
            self.__weight,
            False,
            False,
            False,
            False
        )
        g.__autojoin = self.__autojoin
        g.__union_find = self.__union_find
        g.__default_active = self.__default_active
        g.__directed = self.__directed
        g.__weight = self.__weight
        g.__sort_dirty = self.__sort_dirty
        g.__nodes = deepcopy(self.__nodes)
        g.__edges = deepcopy(self.__edges)
        g.__min_distances = deepcopy(self.__min_distances)
        g.__max_distances = deepcopy(self.__max_distances)
        g.__network_contents = deepcopy(self.__network_contents)
        g.__networks = deepcopy(self.__networks)
        return g