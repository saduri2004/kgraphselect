from typing import List
from graph.node import Node
from graph.graph import Graph

def initialize_graph() -> Graph:
    """
    Initialize a new graph with a start and end node.
    """
    graph = Graph()
    graph.add_node(0, content="Start Node", is_start=True)
    graph.add_node(-1, content="End Node", is_end=True)
    return graph

def process_sequences(sequences: List[List[str]], graph: Graph) -> List[List[Node]]:
    """
    Convert a list of sequences (list of strings) into a list of Node objects.
    If a node does not already exist in the graph, add it.
    
    :param sequences: List of sequences, where each sequence is a list of strings (actions).
    :param graph: The Graph object to populate with nodes.
    :return: List of sequences, where each sequence is a list of Node objects.
    """
    processed_sequences = []
    for seq in sequences:
        processed_seq = []
        for action in seq:
            # Check if the action exists in the graph
            if action not in graph.node_actions:
                # Assign a unique ID and add the node to the graph
                graph.node_actions.add(action)
                node_id = len(graph.nodes)  # Unique ID for the new node
                graph.add_node(node_id, content=action)
            node = next(node for node in graph.nodes.values() if node.content == action)
            processed_seq.append(node)
        processed_sequences.append(processed_seq)
    return processed_sequences

def extract_nodes_and_edges(sequences: List[List[Node]], graph: Graph):
    """
    From a list of action sequences, construct a topological action graph with nodes and edges.
    
    :param sequences: List of sequences, where each sequence is a list of Node objects.
    :param graph: The Graph object to update with edges.
    """
    start_node = graph.get_start_node()
    end_node = graph.get_end_node()

    for seq in sequences:
        print(f"Processing sequence: {[node.content for node in seq]}")

        for i, step in enumerate(seq):
            # Connect the first node in the sequence to the start node
            if i == 0:
                graph.add_edge(start_node.node_id, step.node_id)
                print(f"Added edge from '{start_node.node_id}' to '{step.node_id}'")

            # Connect subsequent nodes in the sequence
            if i < len(seq) - 1:
                next_step = seq[i + 1]
                graph.add_edge(step.node_id, next_step.node_id)
                print(f"Added edge from '{step.node_id}' to '{next_step.node_id}'")

            # Connect the last node in the sequence to the end node
            if i == len(seq) - 1:
                graph.add_edge(step.node_id, end_node.node_id)
                print(f"Added edge from '{step.node_id}' to end node '{end_node.node_id}'")

