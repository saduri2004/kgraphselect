from typing import Dict, List, Tuple
from node import Node

class Graph:
    def __init__(self):
        """
        Initializes the graph with both an edge list and an adjacency list.
        """
        self.nodes: Dict[int, Node] = {}  # Map node_id -> Node
        self.edges: List[Tuple[int, int]] = []  # List of (from_id, to_id) tuples
        self.adjacency_list: Dict[int, List[int]] = {}  # Map node_id -> list of neighbor node_ids
        self.start_node: int = None  # ID of the start node
        self.end_node: int = None  # ID of the end node

    def add_node(self, node_id: int, content: str = None, is_start=False, is_end=False):
        """
        Adds a new node to the graph.
        :param node_id: Unique identifier for the node.
        :param content: The content of the node.
        :param is_start: Indicates if the node is the start node.
        :param is_end: Indicates if the node is the end node.
        """
        if node_id in self.nodes:
            raise ValueError(f"Node with id {node_id} already exists.")
        self.nodes[node_id] = Node(node_id, content)
        self.adjacency_list[node_id] = []  # Initialize empty adjacency list for the node

        if is_start:
            if self.start_node is not None:
                raise ValueError("Start node is already defined.")
            self.start_node = node_id
        if is_end:
            if self.end_node is not None:
                raise ValueError("End node is already defined.")
            self.end_node = node_id

    def add_edge(self, from_id: int, to_id: int):
        """
        Adds a directed edge between two nodes.
        :param from_id: ID of the source node.
        :param to_id: ID of the destination node.
        """
        if from_id not in self.nodes or to_id not in self.nodes:
            raise ValueError("Both nodes must exist to create an edge.")
        self.edges.append((from_id, to_id))
        self.adjacency_list[from_id].append(to_id)

    def get_neighbors(self, node_id: int) -> List[Node]:
        """
        Returns a list of neighbor nodes connected to the given node.
        :param node_id: ID of the node whose neighbors are to be retrieved.
        :return: List of Node objects that are neighbors of the given node.
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node with id {node_id} does not exist.")
        neighbor_ids = self.adjacency_list.get(node_id, [])
        return [self.nodes[n_id] for n_id in neighbor_ids]

    def get_all_edges_from_to(self, from_id: int, to_id: int) -> List[Tuple[int, int]]:
        """
        Returns all edges that go from a specific node to another node.
        :param from_id: ID of the source node.
        :param to_id: ID of the destination node.
        :return: List of edges (tuples) that match the criteria.
        """
        return [(f, t) for f, t in self.edges if f == from_id and t == to_id]

    def get_start_node(self) -> Node:
        """
        Retrieves the start node.
        :return: The start node object.
        """
        if self.start_node is None:
            raise ValueError("Start node is not defined.")
        return self.nodes[self.start_node]

    def get_end_node(self) -> Node:
        """
        Retrieves the end node.
        :return: The end node object.
        """
        if self.end_node is None:
            raise ValueError("End node is not defined.")
        return self.nodes[self.end_node]

    def display_structure(self):
        """
        Prints the structure of the graph, showing nodes and edges.
        """
        print(f"Start Node: {self.start_node}")
        print(f"End Node: {self.end_node}")
        print("Edges:")
        for from_id, to_id in self.edges:
            print(f"Node {from_id} -> Node {to_id}")

    def display_adjacency_list(self):
        """
        Prints the adjacency list representation of the graph.
        """
        print("Adjacency List:")
        for node_id, neighbors in self.adjacency_list.items():
            print(f"Node {node_id}: {neighbors}")
